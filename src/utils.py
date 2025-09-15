import json

def load_config(path="/Users/j.chrisov/Documents/LEVEL3-projects/llm-evaluation/config/config.json"):
    """
    Loads configuration from a JSON file.
    
    Args:
        path (str): Path to the JSON configuration file.
    
    Returns:
        dict: Configuration parameters.
    """

    with open(path, "r") as f:
        return json.load(f)

def load_json(filepath: str, key: str) -> dict:
    """
    Parses the json file.
    
    Args:
        filepath (str): Path to the json's path.
        
    Returns:
        list: list of the spicified key."""
    values = []

    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        data = [] # Exit the program or handle the empty case
    except json.JSONDecodeError:
        print(f"Error: The file '{filepath}' contains invalid JSON.")
        data = [] # Exit the program or handle the empty case
    if data:
        for item in data:
            # Check if the 'query' key exists to prevent a KeyError
            if key in item:
                values.append(item[key])
            else:
                print(f"Warning: '{key}' key not found in an item.")
    else:
        print("The JSON data is empty or invalid.")
    return values

# if __name__ == "__main__":
#     config = load_config()
#     list = load_json(config['prompts_filepath'], 'query')
#     for item in list:
#         print(item)