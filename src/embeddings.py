import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import openai
from typing import List, Dict, Any, Optional, Tuple

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
        # First create row-based chunks
        self._create_row_based_chunks(df, text_columns)
        
        # Then add column-focused chunks for important fields
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
    

    def enhance_openai_call(self, user_query: str, config, **openai_kwargs) -> Tuple[str, List[Dict[str, Any]]]:
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
        privacy_rules = config['system_prompt_filepath'] + config['privacy_rules']
        # with open(system_prompt, "r", encoding="utf-8") as f:
        #     system_prompt_text = f.read()
        with open(privacy_rules, "r", encoding="utf-8") as f:
            privacy_rules_text = f.read()
        enhanced_system_prompt = f"You have access to the following personal information from the database:\n\n{database_context}.\n\nAlways follow the privacy rules:\n\n{privacy_rules_text}."
        messages.append({"role": "system", "content": enhanced_system_prompt})
        messages.append({"role": "user", "content": user_query})
        response = self.openai_client.chat.completions.create(
            model=config['model'],
            messages=messages,
            **openai_kwargs
        )
        return response.choices[0].message.content, relevant_chunks


    # def batch_enhance_queries(self, queries: List[str], system_prompt: str = None,
    #                         retrieval_k: int = 5, model: str = "google/gemini-2.5-flash-lite",
    #                         **openai_kwargs) -> List[Tuple[str, List[Dict[str, Any]]]]:
    #     """
    #     Process multiple queries with database enhancement
        
    #     Args:
    #         queries: List of user queries
    #         system_prompt: Base system prompt
    #         retrieval_k: Number of database chunks to retrieve per query
    #         model: OpenAI model to use
    #         **openai_kwargs: Additional OpenAI API parameters
            
    #     Returns:
    #         List of (llm_response, retrieved_chunks) tuples
    #     """
    #     results = []
    #     for query in queries:
    #         response, chunks = self.enhance_openai_call(
    #             query, system_prompt, retrieval_k, model, **openai_kwargs
    #         )
    #         results.append((response, chunks))
        
    #     return results

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
def enhanced_rag_query(retriever: EmbeddingDatabaseRetriever, user_query: str, config) -> str:
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
        temperature=0.7,
        max_tokens=500
    )
    return response

# # Advanced retrieval with custom filtering
# class AdvancedEmbeddingRetriever(EmbeddingDatabaseRetriever):
    """Extended retriever with filtering and ranking capabilities"""
    
    def retrieve_with_filters(self, query: str, filters: Dict[str, Any] = None,
                            top_k: int = 5, similarity_threshold: float = 0.3) -> List[Dict[str, Any]]:
        """
        Retrieve data with additional filtering
        
        Args:
            query: Search query
            filters: Dictionary of column:value filters to apply
            top_k: Number of results
            similarity_threshold: Minimum similarity
            
        Returns:
            Filtered and ranked results
        """
        # Get initial retrieval results
        initial_results = self.retrieve_relevant_data(query, top_k * 2, similarity_threshold)
        
        if not filters:
            return initial_results[:top_k]
        
        # Apply filters
        filtered_results = []
        for chunk in initial_results:
            source_data = chunk['source_data']
            
            # Check if chunk matches all filters
            matches_filters = True
            for filter_column, filter_value in filters.items():
                if filter_column not in source_data:
                    matches_filters = False
                    break
                
                source_value = str(source_data[filter_column]).lower()
                filter_value = str(filter_value).lower()
                
                if filter_value not in source_value:
                    matches_filters = False
                    break
            
            if matches_filters:
                filtered_results.append(chunk)
        
        return filtered_results[:top_k]
    
    def hybrid_retrieve(self, query: str, boost_columns: List[str] = None,
                       top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Hybrid retrieval that boosts certain column matches
        
        Args:
            query: Search query
            boost_columns: Columns to give extra weight to
            top_k: Number of results
            
        Returns:
            Boosted and ranked results
        """
        results = self.retrieve_relevant_data(query, top_k * 2)
        
        if not boost_columns:
            return results[:top_k]
        
        # Apply boosting
        for result in results:
            boost_factor = 1.0
            source_data = result['source_data']
            
            # Check if any boost columns contain query terms
            query_terms = query.lower().split()
            for boost_col in boost_columns:
                if boost_col in source_data and source_data[boost_col]:
                    col_value = str(source_data[boost_col]).lower()
                    if any(term in col_value for term in query_terms):
                        boost_factor *= 1.2  # 20% boost per matching column
            
            result['boosted_score'] = result['similarity_score'] * boost_factor
        
        # Re-sort by boosted score
        results.sort(key=lambda x: x.get('boosted_score', x['similarity_score']), reverse=True)
        
        return results[:top_k]