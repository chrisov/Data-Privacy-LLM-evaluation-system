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



config = load_config()

tokenizer = AutoTokenizer.from_pretrained(config['model_name'])
model = AutoModelForTokenClassification.from_pretrained(config['model_name'])

nlp = pipeline("ner", model=model, tokenizer=tokenizer)
example = "My name is Wolfgang, I live in Berlin and I work at the Kostal Dental Office in Portugal"

print(f"\nText: '{example}'\n")
ner_results = nlp(example)
entities = {}
current_entity = None
for result in ner_results:
    entity_label = result['entity']
    word = result['word']
    if entity_label.startswith('B-'):
        if current_entity:
            entity_type = current_entity['entity'].split('-')[1]
            entities[entity_type] = " ".join(current_entity['words']).replace(" ##", "")
        current_entity = {
            'entity': entity_label,
            'words': [word]
        }
    elif entity_label.startswith('I-'):
        if current_entity:
            current_entity['words'].append(word)
if current_entity:
    entity_type = current_entity['entity'].split('-')[1]
    entities[entity_type] = " ".join(current_entity['words']).replace("##", "")
for entity_type, value in entities.items():
    print(f"Entity: '{entity_type}', Value: '{value}'")

print("\n\n", ner_results, "\n\n")
