from huggingface_hub.utils import disable_progress_bars
from transformers import logging as hf_logging
import classification as ev
from utils import load_config
import json
from InquirerPy import inquirer
import sys
from colorama import init, Fore, Style


UNDERLINE = "\x1b[4m"

disable_progress_bars()
hf_logging.set_verbosity_error()
init()

def menu() -> str:
    choice = inquirer.select(
        message=f"""
        Clearance Levels:
        Customer -> 0 (PUBLIC)
        Agent -> 1 (INTERNAL)
        External Contractor -> 1 (INTENRAL)
        Analyst -> 2 (CONFIDENTIAL)
        Admin -> 3 (PRIVATE)

        Choose your option:
        """,
        choices=["Customer", "Agent", "External Contractor", "Analyst", "Admin", "Exit"],
    ).execute()
    if choice != "Exit":
        print("You entered as :", choice)
    return choice


if __name__ == "__main__":
    user = menu()
    if (user == "Exit"):
        sys.exit(0)
    config = load_config()
    with open(config['prompts'], 'r') as f:
        prompts = json.load(f)
    for i, prompt in enumerate(prompts, 1):
        eval = ev.Simulation(user)
        for i, tenant in enumerate(eval._tenants, 1):
            print(f"{UNDERLINE}\nTenant {i}{Style.RESET_ALL}: '{tenant['name']}'\n")
            eval.run(prompt, config)
