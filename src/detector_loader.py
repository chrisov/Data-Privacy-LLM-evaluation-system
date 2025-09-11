from utils import load_config
from datasets import load_dataset
import ast

config = load_config()
dataset = load_dataset(config["pii_detector_name"], split='validation')
validation_examples = dataset.select(range(10))

# validation_examples: Dataset type, inlcudes a list of rows containing the examples
# Each row is a dataset with keys 'source_text' and 'span_labels' among others
# For the span_labels, each label is a list of lists with 'start', 'end', and 'label' keys
for example in validation_examples:
    text = example['source_text']
    span_labels = ast.literal_eval(example['span_labels'])

    print(f"\n\n\nText: '{text}'\n\n\n\n")
    if not span_labels:
        print("No PII labels found.")
    else:
        for label_info in span_labels:
            print(f"Label: '{label_info[-1]}'\n", f"Text: '{text[label_info[0]:label_info[1]]}'\n")
    print("--------------------------------------")
