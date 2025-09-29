from huggingface_hub.utils import disable_progress_bars
from transformers import logging as hf_logging
import classification as ev
from utils import load_config
import json
from InquirerPy import inquirer
import sys
from colorama import init, Style

UNDERLINE = "\x1b[4m"

disable_progress_bars()
hf_logging.set_verbosity_error()
init()

def menu() -> str:
    choice = inquirer.select(
        message=f"""
        The Evaluation mode will test all the following User Profiles, exporting the results in a
        .csv file (results.csv), while there is also the ability to run the same tests as per a
        specific profile of your choice.

        Clearance Levels:
        - Customer: No access
        - Agent: Low Sensitive Info
        - External Contractor: Low Sensitive Info
        - Analyst: Medium Sensitive Info
        - Admin: High Sensitive Info

        Choose your option:\n
        """,
        choices=["Evaluation mode\n", "Customer", "Agent", "External Contractor", "Analyst", "Admin\n", "Exit"],
    ).execute()
    if choice == "Exit":
        sys.exit(0)
    print(f"You entered as {choice}\n")
    return choice

if __name__ == "__main__":
    user = menu().rstrip("\n")
    config = load_config()
    with open(config['prompts'], 'r') as f:
        prompts = json.load(f)
    for prompt in prompts:
        if user == "Evaluation mode":
            profiles = ["Customer", "Agent", "External Contractor", "Analyst", "Admin"]
            for profile in profiles:
                user_profile = ev.Simulation(user)
                for i, tenant in enumerate(user_profile._tenants, 1):
                    print(f"{UNDERLINE}\nTenant {i}{Style.RESET_ALL}: '{tenant['name']}'\n")
                    user_profile.run_prompt(prompt, config)
        else:
            user_profile = ev.Simulation(user)
            for i, tenant in enumerate(user_profile._tenants, 1):
                print(f"{UNDERLINE}\nTenant {i}{Style.RESET_ALL}: '{tenant['name']}'\n")
                user_profile.run_prompt(prompt, config, eval_flag=True)
