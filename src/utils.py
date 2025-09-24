import json
import colorama

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



# def load_json(filepath: str, key: str) -> dict:
#     """
#     Parses the json file and returns the specified value.
    
#     Args:
#         filepath (str): Path to the json's path.
#         key (str): The requested key from which we will extract is value 
        
#     Returns:
#         list: The specified key's values.
#     """
#     values = []
#     try:
#         with open(filepath, 'r') as file:
#             data = json.load(file)
#     except FileNotFoundError:
#         print(f"Error: The file '{filepath}' was not found.")
#         data = []
#     except json.JSONDecodeError:
#         print(f"Error: The file '{filepath}' contains invalid JSON.")
#         data = []
#     if data:
#         for item in data:
#             if key in item:
#                 values.append(item[key])
#             else:
#                 print(f"Warning: '{key}' key not found in an item.")
#     else:
#         print("The JSON data is empty or invalid.")
#     return values

def check_clearance(u_lvl: int, truth: list) -> str:
    """
    Checks user's clearance for sprecific prompt, based on its ground truth.

    u_lvl (int): User's clearance level
    truth (list): Ground truth's list to check for clearance 
    """
    clearance = len(truth)
    for item in truth:
        if (u_lvl < item['clearance']):
            clearance -= 1
    if (clearance == len(truth)):
        return ('full')
    elif (clearance > 0):
        return ('partial')
    return ('no')
    


def print_dicts(sut: dict, truth: dict):
    if (sut):
        print("Sensitive data: ")
        for key, value in sut.items():
            print(f"{key}: {value}")
    if (truth):
        print("\nGround truth: ")
        for key, value in truth.items():
            print(f"{key}: {value}")


# if __name__ == "__main__":
#     config = load_config()
#     list = load_json(config['prompts'], 'query')
#     for item in list:
#         print(item)