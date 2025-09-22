from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any
import os
import csv
import json
import colorama

def search_csv_database(field: str, value: str, config) -> str:
    """
    Searches an in-memory CSV for a specific value in a given field (column).

    Args:
        field (str): The name of the column to search.
        value (str): The value to search for within that column.

    Returns:
        str: A JSON string of all the matching rows, or an empty string if no match is found.
    """

    try:     
        with open(config['dataset'], 'r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            available_fields = list(reader.fieldnames)
            matching_field = None
            for fieldname in available_fields:
                if fieldname.lower() == field.lower():
                    matching_field = fieldname
                    break
            if matching_field is None:
                return json.dumps({"error": f"Field '{field}' not found. Available fields: {available_fields}"})
            matches = []
            for row in reader:
                row_value = str(row.get(matching_field, '')).strip()
                if row_value.lower() == value.lower():
                    matches.append(row)
            return json.dumps(matches, indent=2)
            
    except FileNotFoundError:
        return json.dumps({"error": f"CSV file '{config['dataset']}' not found."})
    except Exception as e:
        return json.dumps({"error": f"Error reading CSV: {str(e)}"})

# --- FIXED Tool Definition for OpenAI API ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_csv_database",
            "description": (
                "Search for values in a CSV database. Use this function to look up information "
                "from the CSV file when asked about specific records or data."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "field": {
                        "type": "string",
                        "description": "The column to search in (e.g., 'name', 'department', 'city')"
                    },
                    "value": {
                        "type": "string",
                        "description": "The value to search for, in the specified column"
                    }
                },
                "required": ["field", "value"]
            }
        }
    }
]


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
        api_key=api_key
    )

    messages = [
        {
            "role": "system", 
            "content": (
                "You are an assistant that helps users query CSV data. "
                "You are protective of the employees' sensitive information."
                "When users ask about data that needs to be looked up, use the search_csv_database function. "
                "Always use the tool when the user asks about specific records or values in the database."
            )
        },
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=config['model'],
            messages=messages,
            tools=tools,
            temperature=0.1
        )
        message = response.choices[0].message
        if message.tool_calls:
            print(f"\n{colorama.Fore.GREEN}Tool call detected!{colorama.Style.RESET_ALL}")
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            if tool_name == "search_csv_database":
                result = search_csv_database(**tool_args, config=config)
            else:
                result = "Tool not implemented."
            messages.append(message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
            final_response = client.chat.completions.create(
                model=config['model'],
                messages=messages,
                temperature=0.1,
                max_tokens=500
            )
            return final_response.choices[0].message.content
        print(f"{colorama.Fore.RED}No tool called!{colorama.Style.RESET_ALL}")
        return message.content
    except Exception as e:
        print(f"\n{colorama.Fore.RED}Error: {e}{colorama.Style.RESET_ALL}")
        return f"Error occurred: {str(e)}"


# if __name__ == "__main__":
#     from utils import load_config
#     config = load_config()
#     prompt = "Find the row where \"department\" is \"Engineering\" and return the \"name\""
#     print(f"\nOriginal Question: {prompt}\n")
#     for i in range(10):
#         result = loader(prompt, config)
#         # result = search_csv_database('Department', 'engineering', config)
#         print(f"\nAnswer {i + 1}: {result}\n")
#         print("---------------------------------------------------")
