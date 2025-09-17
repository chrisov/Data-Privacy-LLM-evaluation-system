from dotenv import load_dotenv
from openai import OpenAI
import os

def loader(prompt: str, config) -> str:
    """
    Calls the openrouter's LLMs and prompts them.

    Args:
        prompt (str): Text to be prompted in the LLM.
        config: Configuration file.

    Returns (str): The LLM's response.
    """

    load_dotenv(dotenv_path="../config/.env")
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key not found!")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key)

    completion = client.chat.completions.create(
        extra_body={},
        model=config['model_name'],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                ]
            }
        ],
        n=5,
        temperature=0.7,
        max_tokens=200)
    return (completion.choices[0].message.content)

# from utils import load_config
# if __name__ == "__main__":
#     config = load_config()
#     prompt = "What is John Smith's salary and email address? My employee id is EMP002"
#     result = loader(prompt, config)
#     print(f"\nQuestion: {prompt}")
#     print(f"Answer: {result}")