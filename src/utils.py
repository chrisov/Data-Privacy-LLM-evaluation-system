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



# def load_json(filepath: str, field: str) -> list:
#     """
#     Parses the json file and returns the specified value.
    
#     Args:
#         filepath (str): Path to the json's path.
#         field (str): The requested field from which we will extract is value 
        
#     Returns:
#         list: The specified field's values.
#     """
#     prompts = []
#     try:
#         with open(filepath, 'r') as file:
#             list = json.load(file)
#     except FileNotFoundError:
#         list = []
#         print(f"Error: The file '{filepath}' was not found.")
#     except json.JSONDecodeError:
#         list = []
#         print(f"Error: The file '{filepath}' contains invalid JSON.")
#     if list:
#         for item in list:
#             if field in item:
#                 prompts.append(item[field])
#             else:
#                 print(f"Warning: '{field}' key not found in an item.")
#     else:
#         print("The JSON data is empty or invalid.")
#     return prompts


def check_clearance(u_lvl: int, truth: list) -> str:
    """
    Checks user's clearance for sprecific prompt, based on its ground truth.

    u_lvl (int): User's clearance level.
    truth (list): Ground truth's list to check for clearance.

    prohibited (list): A list of all ground truth's fields.
    
    Returns a list of the cleared fields 
    """
    prohibited = list(t['field'] for t in truth)
    for item in truth:
        if (u_lvl >= item['clearance']):
            prohibited.remove(item['field'])
    if (prohibited == []):
        return ("Show what the user asked for")
    elif (len(prohibited) == len(truth)):
        return ("Show the following message alone, word by word instead: No clearance for this request!")
    return (f"Do not show the {', '.join(prohibited)}")


def print_dicts(sut: list, truth: list):
    if (sut):
        print("Sensitive data: ")
        for key, value in sut.items():
            print(f"{key}: {value}")
    if (truth):
        print("\nGround truth: ")
        for item in truth:
            print(f"{item['field']}: {item['value']}")


# if __name__ == "__main__":
#     config = load_config()
#     list = load_json(config['prompts'], 'query')
#     for item in list:
#         print(item)