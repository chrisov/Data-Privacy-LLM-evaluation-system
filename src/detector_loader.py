import json
import ast

def process_pii_data(prompt: list) -> dict:
    """
    Loads and processes a PII dataset, extracting PII entities and source texts.

    Args:
        pii_name (str): The name of the dataset from Hugging Face Hub.

    Returns:
        tuple: A tuple containing a list of all texts and a dictionary of extracted PII.
    """

    pii_data = {}
    labels = ast.literal_eval(prompt['span_labels'])
    text = prompt['source_text']
    if labels:
        for label in labels:
            start_char = label[0]
            end_char = label[1]
            label_name = label[2]
            pii_text = text[start_char:end_char]
            if label_name not in pii_data:
                pii_data[label_name] = []
            pii_data[label_name].append(pii_text)
    return pii_data

def save_to_json(data: list, file_path: str):
    """
    Saves a list of dictionaries to a JSON file.
    """

    try:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
            if not isinstance(existing_data, list):
                existing_data = [existing_data]
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []
    existing_data.extend(data)
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)


def clear_json_file(file_path: str):
    """
    Clears all content from a JSON file.
    """

    with open(file_path, 'w') as file:
        pass  # The 'w' mode truncates the file, leaving it empty

