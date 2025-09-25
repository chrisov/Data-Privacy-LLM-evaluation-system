import json

UNDERLINE = "\x1b[4m"
RESET = "\033[0m"

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


def create_ground_truth(ground_truth: list) -> dict:
    new_dict = {}
    for item in ground_truth:
        field_name = item.get('field')
        field_value = item.get('value')
        if field_name:
            new_dict[field_name] = field_value
    return new_dict


def print_dict(d: dict, title: str, ind: str):
    if (d):
        print(f"{ind}{UNDERLINE}{title}{RESET}: ")
        for key, value in d.items():
            print(f"{ind}{key}: {value}")



# if __name__ == "__main__":
#     config = load_config()
#     list = load_json(config['prompts'], 'query')
#     for item in list:
#         print(item)