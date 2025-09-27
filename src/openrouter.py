from dotenv import load_dotenv
from openai import OpenAI
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def loader() -> OpenAI:    
    load_dotenv(dotenv_path="../config/.env")
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key not found!")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    return client


from utils import load_config
import embeddings as emb
if __name__ == "__main__":
    config = load_config()
    retriever = emb.integrate_embedding_retrieval(config, 'hybrid', openai_client=loader())
    prompt = "What is Frank Booth's email address?"

    print("\n===============================================")
    print (f"Question: {prompt}")
    print("===============================================\n")
    for i in range(config['iterations']):
        result = emb.enhanced_rag_query(retriever, prompt, config)
        print(f"Answer {i + 1}: '{result}'\n")