import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import openai
from typing import List, Dict, Any, Optional, Tuple
import classification as c

class EmbeddingDatabaseRetriever:
    """Embedding-based retrieval system for CSV database integration with OpenAI"""
    
    def __init__(self, embedding_model_name: str = 'all-mpnet-base-v2', openai_client=None):
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.openai_client = openai_client or openai
        
        # Vector store components
        self.vector_index = None
        self.metadata_store = []
        self.text_chunks = []
        self.dimension = None
        
        # Database state
        self.is_initialized = False


    def initialize_from_csv(self, csv_path: str, text_columns: List[str] = None, 
                          chunk_strategy: str = 'row_based') -> None:
        """
        Initialize the embedding database from CSV file
        
        Args:
            csv_path: Path to CSV file
            text_columns: Specific columns to use for text generation (None = use all)
            chunk_strategy: 'row_based', 'column_based', or 'hybrid'
        """
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()  # Clean column names
        
        if chunk_strategy == 'row_based':
            self._create_row_based_chunks(df, text_columns)
        elif chunk_strategy == 'column_based':
            self._create_column_based_chunks(df, text_columns)
        elif chunk_strategy == 'hybrid':
            self._create_hybrid_chunks(df, text_columns)
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(
            self.text_chunks, 
            batch_size=32, 
            show_progress_bar=False,
            convert_to_tensor=False
        )
        
        # Initialize FAISS index
        self.dimension = embeddings.shape[1]
        self.vector_index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings.astype(np.float32))
        self.vector_index.add(embeddings.astype(np.float32))
        self.is_initialized = True


    def _create_row_based_chunks(self, df: pd.DataFrame, text_columns: Optional[List[str]]) -> None:
        """Create one chunk per row with all relevant information"""
        columns_to_use = text_columns if text_columns else df.columns.tolist()
        
        for idx, row in df.iterrows():
            # Create natural language description of the row
            row_text_parts = []
            
            for col in columns_to_use:
                if col in df.columns and pd.notna(row[col]):
                    value = str(row[col]).strip()
                    if value:
                        row_text_parts.append(f"{col}: {value}")
            
            chunk_text = ". ".join(row_text_parts)
            self.text_chunks.append(chunk_text)
            
            # Store metadata for retrieval
            self.metadata_store.append({
                'chunk_type': 'row',
                'row_index': idx,
                'source_data': row.to_dict(),
                'columns_used': columns_to_use,
                'chunk_text': chunk_text
            })
    

    def _create_column_based_chunks(self, df: pd.DataFrame, text_columns: Optional[List[str]]) -> None:
        """Create focused chunks for specific data relationships"""
        columns_to_use = text_columns if text_columns else df.columns.tolist()
        
        for idx, row in df.iterrows():
            # Create multiple focused chunks per row
            for col in columns_to_use:
                if col in df.columns and pd.notna(row[col]):
                    # Create a focused chunk around this column
                    primary_value = str(row[col]).strip()
                    if not primary_value:
                        continue
                    
                    # Add related context columns
                    context_parts = [f"{col}: {primary_value}"]
                    
                    # Add key identifying information
                    key_columns = ['Employee_Name', 'EmpID', 'Salary', 'Home_Address', 'Email', 'phone_number',
                                   'Credit_Card', 'voterID', 'IP', 'IMEI/MAC address', 'username', 'SSN', 'IBAN',
                                   'Passport', 'State', 'Zip', 'DOB', 'Sex', 'RaceDesc']
                    for key_col in key_columns:
                        if key_col in df.columns and key_col != col and pd.notna(row[key_col]):
                            context_parts.append(f"{key_col}: {row[key_col]}")
                    
                    chunk_text = ". ".join(context_parts)
                    self.text_chunks.append(chunk_text)
                    
                    self.metadata_store.append({
                        'chunk_type': 'column_focused',
                        'row_index': idx,
                        'primary_column': col,
                        'primary_value': primary_value,
                        'source_data': row.to_dict(),
                        'chunk_text': chunk_text
                    })
    

    def _create_hybrid_chunks(self, df: pd.DataFrame, text_columns: Optional[List[str]]) -> None:
        """Create both row-based and column-focused chunks"""
        self._create_row_based_chunks(df, text_columns)
        
        important_columns = ['Skills', 'Description', 'Notes', 'Comments', 'Experience', 'Education']
        existing_columns = [col for col in important_columns if col in df.columns]
        
        if existing_columns:
            current_chunk_count = len(self.text_chunks)
            self._create_column_based_chunks(df, existing_columns)
            
            # Mark the new chunks as supplementary
            for i in range(current_chunk_count, len(self.metadata_store)):
                self.metadata_store[i]['chunk_type'] = 'supplementary_column'
    

    def retrieve_relevant_data(self, query: str, top_k: int = 5, 
                             similarity_threshold: float = 0.3) -> List[Dict[str, Any]]:
        """
        Retrieve most relevant data chunks for a given query
        
        Args:
            query: User query text
            top_k: Number of top results to return
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of relevant data chunks with metadata
        """
        if not self.is_initialized:
            raise ValueError("Database not initialized. Call initialize_from_csv() first.")
        
        # Encode query
        query_embedding = self.embedding_model.encode([query], convert_to_tensor=False)
        faiss.normalize_L2(query_embedding.astype(np.float32))
        
        # Search for similar chunks
        similarities, indices = self.vector_index.search(
            query_embedding.astype(np.float32), 
            top_k
        )
        
        relevant_chunks = []
        for similarity, idx in zip(similarities[0], indices[0]):
            if similarity >= similarity_threshold:
                chunk_metadata = self.metadata_store[idx].copy()
                chunk_metadata['similarity_score'] = float(similarity)
                relevant_chunks.append(chunk_metadata)
        
        return relevant_chunks
    

    def prepare_context_for_llm(self, relevant_chunks: List[Dict[str, Any]], 
                               max_context_length: int = 100000) -> str:
        """
        Convert retrieved chunks into context string for LLM
        
        Args:
            relevant_chunks: Retrieved chunks from retrieve_relevant_data
            max_context_length: Maximum character length for context
            
        Returns:
            Formatted context string
        """
        if not relevant_chunks:
            return "No relevant information found in the database."
        context_parts = []
        current_length = 0
        for i, chunk in enumerate(relevant_chunks, 1):
            chunk_info = f"Record {i} (similarity: {chunk['similarity_score']:.3f}):\n"
            chunk_info += chunk['chunk_text'] + "\n"
            if current_length + len(chunk_info) > max_context_length:
                break
            context_parts.append(chunk_info)
            current_length += len(chunk_info)
        return "\n".join(context_parts)
    

    def enhance_openai_call(self, user_query: str, config, clearance: c.ClearanceLevel,  **openai_kwargs) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Enhanced OpenAI call with automatic database retrieval
        
        Args:
            user_query: User's question/prompt
            **openai_kwargs: Additional OpenAI API parameters
            
        Returns:
            Tuple of (llm_response, retrieved_chunks)
        """
        relevant_chunks = self.retrieve_relevant_data(user_query, top_k=config['retrieval_k'])
        database_context = self.prepare_context_for_llm(relevant_chunks)
        messages = []
        # system_prompt = config['system_prompt_filepath'] + config['system_prompt']
        # with open(system_prompt, "r", encoding="utf-8") as f:
        #     system_prompt_text = f.read()
        privacy_rules = config['system_prompt_filepath'] + config['privacy_rules']
        with open(privacy_rules, "r", encoding="utf-8") as f:
            privacy_rules_text = f.read()
        enhanced_system_prompt = f"""
            You have access to the following personal information from the database:
            \n\n{database_context}.
            \n\nThe User's Clearance Level is:
            \n\n{clearance}.
            \n\nAlways follow the privacy rules:
            \n\n{privacy_rules_text}.
            """
        messages.append({"role": "system", "content": enhanced_system_prompt})
        messages.append({"role": "user", "content": user_query})
        response = self.openai_client.chat.completions.create(
            model=config['model'],
            messages=messages,
            **openai_kwargs
        )
        return response.choices[0].message.content, relevant_chunks


# Integration function for existing OpenAI workflow
def integrate_embedding_retrieval(config, chunk_strategy, openai_client=None) -> EmbeddingDatabaseRetriever:
    """
    Factory function to quickly set up embedding-based retrieval

    Args:
        csv_path: Path to your CSV database
        embedding_model: Sentence transformer model name
        openai_client: OpenAI client instance
        
    Returns:
        Configured EmbeddingDatabaseRetriever instance
    """
    retriever = EmbeddingDatabaseRetriever(
        embedding_model_name=config['embedding_model'],
        openai_client=openai_client
    )
    retriever.initialize_from_csv(config['dataset'], chunk_strategy=chunk_strategy)
    return retriever

# Example usage pattern for replacing your existing RAG structure
def enhanced_rag_query(retriever: EmbeddingDatabaseRetriever, clearance: c.ClearanceLevel, user_query: str, config) -> str:
    """
    Single function to handle the complete RAG workflow
    
    Args:
        retriever: Initialized EmbeddingDatabaseRetriever
        user_query: User's question
        custom_system_prompt: Custom system instructions
        
    Returns:
        LLM response enhanced with database context
    """
    response, retrieved_data = retriever.enhance_openai_call(
        user_query,
        config,
        clearance,
        temperature=0.7,
        max_tokens=500
    )
    return response
