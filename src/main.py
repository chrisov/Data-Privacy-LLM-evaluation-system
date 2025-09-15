import utils
import LLM_loader as llm
import gliner_model as ner
import baseline as gtruth

def menu(config) -> dict:
    print("\n\nLLM Evaluation system")
    print("Choose one of the following options:")
    print("[1] Test with the prompt Dataset.")
    print("[2] Test with a custom prompt.")
    option = input("Choose: ")
    result = {}
    while (True):
        if (option == '1'):
            result = utils.load_json(config['prompts_filepath'], 'query')
            break ;
        elif (option == '2'):
            result = {'query', input('Ask the LLM:\n')}
            break ;
        else:
            option = input("Incorrect option. Choose again: ")
    return result


def main():
    config = utils.load_config()
    prompts = menu(config)
    print("\n------------------------------------")
    for index, prompt in enumerate(prompts):
        ground_truth = gtruth.create_dict(prompt, config)
        respond = llm.loader(prompt, config)
        data = ner.loader(prompt, respond, config)

        print("------------------------------------\n")
        print(f"Question {index + 1}: {prompt}\n")
        print(f"Answer: {respond}\n")
        print("Sensitive data: ")
        for key, value in data.items():
            print(f"{key}: {value}")
        print("\nGround truth: ")
        if (ground_truth):
            for key, value in ground_truth.items():
                print(f"{key}: {value}")
        else:
            print("No ground truth!")
        print("\n------------------------------------")

    # Compare the NER model's output with the ground truth's output

import os
import warnings
from urllib3.exceptions import NotOpenSSLWarning
from transformers import logging as hf_logging

if __name__ == "__main__":
    # 1. Disable urllib3 NotOpenSSLWarning
    warnings.filterwarnings('ignore', category=NotOpenSSLWarning)

    # 2. Disable tokenizers parallelism warning
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # 3. Disable transformers logging messages
    hf_logging.set_verbosity_error()
    main()
