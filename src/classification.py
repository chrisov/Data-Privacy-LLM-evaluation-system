from enum import Enum
from colorama import Fore, Style
import openrouter as ai
import utils
import metrics as m
import regex as rgx
import matrix as mtx

UNDERLINE = "\x1b[4m"

class ClearanceLevel(Enum):
    PUBLIC = 0
    INTERNAL = 1             # Available to anybody in the same tenant
    CONFIDENTIAL = 2         # Available up to certain clearance level of the same tenant
    PRIVATE = 3              # Available only to the specific individual

class Role(Enum):
    CUSTOMER = "Customer"
    EXT_CONTRACTOR = "External Contractor"
    AGENT = "Agent"
    ANALYST = "Analyst"
    ADMIN = "Admin"

class PIIType(Enum):
    EMPLOYEE_NAME = "Employee_Name"
    EMP_ID = "EmpID"
    SALARY = "Salary"
    HOME_ADDRESS = "Home_Address"
    EMAIL = "Email"
    PHONE_NUMBER = "phone_number"
    CREDIT_CARD = "Credit_Card"
    VOTER_ID = "voterID"
    IP = "IP"
    MAC = "IMEI/MAC address"
    USERNAME = "username"
    SSN = "SSN"
    IBAN = "IBAN"
    PASSPORT = "Passport"
    DOB = "DOB"
    SEX = "Sex"
    RACE = "RaceDesc"

class AttackVector(Enum):
    DIRECT_QUERY = "direct_query"
    INDIRECT_INFERENCE = "indirect_inference"
    MULTIPLE_CHOICE = "multiple_choice"
    INSTRUCTION_OVERRIDE = "instruction_override"
    ROLE_INVERSION = "role_inversion"
    PERMISSIVE_FRAMING = "permissive_framing" 
    IMPERSONATION = "impersonation"

class Simulation:
    """
    Declares and initializes the evaluation system for a multi tenant system.
    Different tenants can simulate the different sessions.
    """

    def __init__(self, user: str):
       self.init_tenants()
       self.init_user_profile(user)
       pass
 
    def init_tenants(self):
        """
        Init the different types of tenants in the case of a multi tenant system.

        Note: Only one as of now (Scale-up) 
        """

        self._tenants = [
            {
                'name': '42 + 1 GmbH',
                'size': 'Startup',
                'industry': 'financial',
                'compliance': ['PCI-DSS', 'SOX', 'GDPR'],
                'data_retention': 1,
                'encryption_level': 'AES-256'
            }
        ]

    def init_user_profile(self, choice: str):
        """
        Init the different types of users accessing the system,
        with different levels of hierarchy
        """

        if (choice == Role.CUSTOMER.value):
            self._user = {
                'tenant': '42 + 1 GmbH',
                'role': Role.CUSTOMER,
                'clearance': ClearanceLevel.PUBLIC,
                'department': None,
            }
        elif (choice == Role.EXT_CONTRACTOR.value):
            self._user = {
                'tenant': '42 + 1 GmbH',
                'role': Role.EXT_CONTRACTOR,
                'clearance': ClearanceLevel.INTERNAL,
                'department': 'it_support',
            }
        elif (choice == Role.AGENT.value):
            self._user = {
                'tenant': '42 + 1 GmbH',
                'role': Role.AGENT,
                'clearance': ClearanceLevel.INTERNAL,
                'department': 'customer_support',
            }
        elif (choice == Role.ANALYST.value):
            self._user = {
                'tenant': '42 + 1 GmbH',
                'role': Role.ANALYST,
                'clearance': ClearanceLevel.CONFIDENTIAL,
                'department': 'risk_management',
            }
        else:
            self._user = {
                'tenant': '42 + 1 GmbH', 
                'role': Role.ADMIN,
                'clearance': ClearanceLevel.PRIVATE,
                'department': 'customer_support',
            }

    def run_prompt(self, prompt: dict, config) -> str:
        query = prompt['query']
        ground_truth = utils.create_ground_truth(prompt['ground_truth'])
        metric = m.metrics()
        restriction = utils.check_clearance(self._user['clearance'].value, prompt['ground_truth'])
        matrix = mtx.Matrix()

        print(f"\t{UNDERLINE}Question{Style.RESET_ALL}: {query}\n")
        utils.print_dict(ground_truth, "Ground truth", "\t")
        # print(f"\n\t\t{UNDERLINE}{Style.RESET_ALL}:")
        
        for j in range(config['iterations']):
            response = ai.loader(query, restriction, config)
            exposed_data = rgx.search_for_sensitive_data(response, ground_truth)
            metric.measure(exposed_data, ground_truth)
            matrix.calculations(exposed_data, ground_truth)

            print(f"\n\t\t{UNDERLINE}{self._user['role'].value}'s Answer {j + 1}{Style.RESET_ALL}: {response}\n")
            utils.print_dict(exposed_data, "Sensitive data", "\t\t")
        
        metric.print_records()
        matrix.confusion_matrix(config)
        print(f"\n{Fore.YELLOW}========================================{Style.RESET_ALL}\n")



from utils import load_config
from huggingface_hub.utils import disable_progress_bars
from transformers import logging as hf_logging
import json
if __name__ == "__main__":
    disable_progress_bars()
    hf_logging.set_verbosity_error()
    config = load_config()
    # user = "Customer"
    user = "Agent"
    # user = "Admin"
    # user = "Analyst"
    ev = Simulation(user)
    with open(config['prompts'], 'r') as f:
        prompts = json.load(f)
    prompt = prompts[0]
    ev.run_prompt(prompt, config)
    
