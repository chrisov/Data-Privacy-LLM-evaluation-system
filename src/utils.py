import json
import csv

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


def create_ground_truth(ground_truth: list, user_clearance: int) -> dict:
    """
    Transforms a list of ground truth items into a dictionary, filtering 
    items based on the user's clearance level and the item's sensitivity.

    Args:
        ground_truth: A list of dictionaries, each expected to have 'field', 
                      'value', and 'sensitivity' keys.
        user_clearance: An integer (0, 1, 2, or 3) representing the access level.

    Returns:
        A dictionary with 'field' as keys and 'value' as values, based on clearance.
    """
    if user_clearance == 0:
        filtered_list = ground_truth
    elif user_clearance == 1:
        allowed_sensitivity = {"Medium", "High"}
        filtered_list = [
            item for item in ground_truth 
            if item.get('sensitivity') in allowed_sensitivity
        ]
    elif user_clearance == 2:
        allowed_sensitivity = {"High"}
        filtered_list = [
            item for item in ground_truth 
            if item.get('sensitivity') in allowed_sensitivity
        ]
    elif user_clearance == 3:
        return {}
    new_dict = {}
    for item in filtered_list:
        field_name = item.get('field')
        field_value = item.get('value')
        if field_name:
            new_dict[field_name] = field_value
    return new_dict


def print_dict(d: dict, title: str, ind: str):
    print(f"{ind}{UNDERLINE}{title}{RESET}: ")
    for key, value in d.items():
        print(f"{ind}{key}: {value}")


def append_to_csv(data: list[str], filename: str):
    """Writes a list of lists (tabular data) to a CSV file."""
    row = [data]
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(row)

# if __name__ == "__main__":
#     config = load_config()
#     list = load_json(config['prompts'], 'query')
#     for item in list:
#         print(item)