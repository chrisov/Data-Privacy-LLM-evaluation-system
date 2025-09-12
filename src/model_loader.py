from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from utils import load_config

# def NER_model(model_name, num_labels=2):
#     """
#     Load a pre-trained model and tokenizer from the Hugging Face Hub.
    
#     Args:
#         model_name (str): The identifier of the pre-trained model.
#         num_labels (int): Number of labels for token classification. Default is 2.

#     Returns:
#         model: The loaded pre-trained model.
#         tokenizer: The loaded tokenizer.   
#     """
    
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=num_labels)
#     return model, tokenizer

def loader(NER_model_name: str, input: str) -> dict:
    config = load_config()

    NER_tokenizer = AutoTokenizer.from_pretrained(NER_model_name)
    NER_model = AutoModelForTokenClassification.from_pretrained(NER_model_name)

    nlp = pipeline("ner", model=NER_model, tokenizer=NER_tokenizer)

    # print(f"\nText: '{example}'\n")
    ner_results = nlp(input)

    final_entities = {}
    current_entity_words = []
    current_entity_type = None

    for result in ner_results:
        word = result['word']
        entity_label = result['entity']
        if entity_label.startswith('B-'):
            # Process and store the previous entity if one existed
            if current_entity_words:
                full_entity = "".join(current_entity_words).replace("##", "").replace(" ", " ")
                if current_entity_type not in final_entities:
                    final_entities[current_entity_type] = []
                final_entities[current_entity_type].append(full_entity)
            # Start a new entity
            current_entity_words = [word]
            current_entity_type = entity_label.split('-')[1]

        # Handle the continuation of an entity
        elif entity_label.startswith('I-'):
            if current_entity_words:
                if word.startswith('##'):
                    current_entity_words.append(word)
                else:
                    current_entity_words.append(" " + word)

    # Process and store the last entity after the loop
    if current_entity_words:
        full_entity = "".join(current_entity_words).replace("##", "").replace(" ", " ")
        if current_entity_type not in final_entities:
            final_entities[current_entity_type] = []
        final_entities[current_entity_type].append(full_entity)

    return final_entities

# if __name__ == "__main__":
#     config = load_config()
#     example = "My name is Wolfgang, I live in Berlin and I work at the Kostal Dental Office in Portugal"
#     dict = loader(config['NER_model_name'], example)
#     for key, value in dict.items():
#         print(f"{key}: {value}")