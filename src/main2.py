from huggingface_hub.utils import disable_progress_bars
from transformers import logging as hf_logging
import classification as eval
from utils import load_config
import json

UNDERLINE = "\x1b[4m"

disable_progress_bars()
hf_logging.set_verbosity_error()

if __name__ == "__main__":
    config = load_config()
    with open(config['prompts'], 'r') as f:
        prompts = json.load(f)
    # prompts = utils.load_json(config['prompts'], 'query')
    for i, prompt in enumerate(prompts, 1):
        # ground_truth = gtruth.create_dict(prompt, config)
        ev = eval.Simulation()
        ev.run(prompt, config)
        # for j in range(config['iterations']):
        #     respond = ai.loader(prompt, config)
        #     # exposed_data = ner.loader(prompt, respond, config)
        #     print(f"\n{UNDERLINE}Answer {j + 1}{Style.RESET_ALL}: {respond}\n")
        #     utils.print_dicts(exposed_data, None)
        #     met.measure(exposed_data, ground_truth)
        # utils.print_dicts(None, ground_truth)
        # met.print_records()
