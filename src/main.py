import utils
import LLM_loader as llm
import gliner_model as ner
import baseline as gtruth
import metrics as eval
import statistics
import os
import warnings
from urllib3.exceptions import NotOpenSSLWarning
from transformers import logging as hf_logging
from huggingface_hub.utils import disable_progress_bars

def main():
    config = utils.load_config()
    prompts = utils.load_json(config['prompts_filepath'], 'query')
    # print("\n------------------------------------")
    for index, prompt in enumerate(prompts):
        ground_truth = gtruth.create_dict(prompt, config)
        precision = []
        recall = []
        f1 = []
        print("\n------------------------------------\n")
        print(f"Question {index + 1}: {prompt}\n")
        for i in range(config['iterations']):
            respond = llm.loader(prompt, config)
            data = ner.loader(prompt, respond, config)
            print(f"Answer #{i}: {respond}\n")
            # print("Sensitive data: ")
            # for key, value in data.items():
            #     print(f"{key}: {value}")
            # print("\nGround truth: ")
            # if (ground_truth):
            #     for key, value in ground_truth.items():
            #         print(f"{key}: {value}")
            # else:
            #     print("No ground truth!\n")
            eval.measure(ground_truth, data, precision, recall, f1)
        precision.append(statistics.mean(precision))
        recall.append(statistics.mean(recall))
        f1.append(statistics.mean(f1))
        eval.print_records(precision, recall, f1)
        print("\n------------------------------------")

    # Compare the NER model's output with the ground truth's output
    

if __name__ == "__main__":
    # 1. Disable urllib3 NotOpenSSLWarning
    warnings.filterwarnings('ignore', category=NotOpenSSLWarning)

    # 2. Disable tokenizers parallelism warning
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # 3. Disable transformers logging messages
    hf_logging.set_verbosity_error()

    disable_progress_bars()

    main()
