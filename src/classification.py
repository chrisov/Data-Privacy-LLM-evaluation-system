from enum import Enum
from colorama import init, Fore, Style
import openrouter as ai
import utils

init()
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

class EvaluationSuite:
    """
    Declares and initializes the evaluation system for a multi tenant system.
    Different tenants can simulate the different sessions.
    """

    def __init__(self):
       self.init_tenants()
       self.init_users()
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
    
    def init_users(self):
        """
        Init the different types of users accessing the system,
        with different levels of hierarchy
        """

        self._users = [
            {
                'tenant': '42 + 1 GmbH',
                'role': Role.CUSTOMER,
                'clearance': ClearanceLevel.PUBLIC,
                'department': None,
            },
            {
                'tenant': '42 + 1 GmbH',
                'role': Role.EXT_CONTRACTOR,
                'clearance': ClearanceLevel.INTERNAL,
                'department': 'it_support',
            },
            {
                'tenant': '42 + 1 GmbH',
                'role': Role.AGENT,
                'clearance': ClearanceLevel.INTERNAL,
                'department': 'customer_support',
            },
            {
                'tenant': '42 + 1 GmbH',
                'role': Role.ANALYST,
                'clearance': ClearanceLevel.CONFIDENTIAL,
                'department': 'risk_management',
            },
            {
                'tenant': '42 + 1 GmbH', 
                'role': Role.ADMIN,
                'clearance': ClearanceLevel.PRIVATE,
                'department': 'customer_support',
            }
        ]

    def run(self, prompt: str, config) -> str:
        print(prompt)
        for i, tenant in enumerate(self._tenants, 1):
            print(f"{UNDERLINE}Tenant {i}{Style.RESET_ALL}: '{tenant['name']}'\n")
            query = prompt['query']
            print(f"\t{UNDERLINE}Question{Style.RESET_ALL}: {query}")
            for j, user in enumerate(self._users, 1):
                clearance = utils.check_clearance(user['clearance'].value, prompt['ground_truth'])
                print(f"\n\t\t{UNDERLINE}User {j}{Style.RESET_ALL} ({user['role'].value}): {clearance} clearance!")
        # respond = ai.loader(prompt, config)



        # print(users)


from utils import load_config
import json
if __name__ == "__main__":
    config = load_config()
    ev = EvaluationSuite()
    with open(config['prompts'], 'r') as f:
        prompts = json.load(f)
    prompt = prompts[0]
    ev.run(prompt, config)
    
