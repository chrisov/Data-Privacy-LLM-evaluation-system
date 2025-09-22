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
    Parses the json file and returns the specified value.
    
    Args:
        filepath (str): Path to the json's path.
        key (str): The requested key from which we will extract is value 
        
    Returns:
        list: The specified key's values.
    """
    values = []

    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        data = []
    except json.JSONDecodeError:
        print(f"Error: The file '{filepath}' contains invalid JSON.")
        data = []
    if data:
        for item in data:
            if key in item:
                values.append(item[key])
            else:
                print(f"Warning: '{key}' key not found in an item.")
    else:
        print("The JSON data is empty or invalid.")
    return values

def print_dicts(sut: dict, truth: dict):
    print("Sensitive data: ")
    for key, value in sut.items():
        print(f"{key}: {value}")
    print("\nGround truth: ")
    if (truth):
        for key, value in truth.items():
            print(f"{key}: {value}")
    else:
        print("No ground truth!\n")

# if __name__ == "__main__":
#     config = load_config()
#     list = load_json(config['prompts'], 'query')
#     for item in list:
#         print(item)