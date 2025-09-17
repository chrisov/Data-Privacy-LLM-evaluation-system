import utils
import openrouter as ai
import gliner_model as ner
import baseline as gtruth
import metrics as eval
import statistics
import os
from urllib3.exceptions import NotOpenSSLWarning
from transformers import logging as hf_logging
from huggingface_hub.utils import disable_progress_bars

def main():
    config = utils.load_config()
    prompts = utils.load_json(config['prompts_filepath'], 'query')
    for index, prompt in enumerate(prompts):
        ground_truth = gtruth.create_dict(prompt, config)
        precision = []
        recall = []
        f1 = []
        print("\n------------------------------------\n")
        print(f"Question {index + 1}: {prompt}\n")
        for i in range(config['iterations']):
            # respond = llm.loader(prompt, config)
            respond = ai.loader(prompt, config)
            exposed_data = ner.loader(prompt, respond, config)
            print(f"Answer #{i + 1}: {respond}\n")
            # utils.print_dicts()
            eval.measure(ground_truth, exposed_data, precision, recall, f1)
        precision.append(statistics.mean(precision))
        recall.append(statistics.mean(recall))
        f1.append(statistics.mean(f1))
        eval.print_records(precision, recall, f1)
        print("\n------------------------------------")

    # Compare the NER model's output with the ground truth's output
    

if __name__ == "__main__":
    # 1. Disable tokenizers parallelism warning
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # 2. Disable transformers logging messages
    hf_logging.set_verbosity_error()

    disable_progress_bars()

    main()
