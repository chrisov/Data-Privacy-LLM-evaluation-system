# import matplotlib as plt
from colorama import init, Fore, Style

class metrics:
    def __init__(self):
        self._precision = []
        self._recall = []
        self._F1_score = []

    def measure(self, sut: dict, ltruth: list):
        """
        Measures and prints different types of metrics
        
        Args:
            sut (dict): dict to be measured.
            truth (list): Ground truth list of dictionaries.
        
        self._recall (list): Record of the Recall metric
        self._precision (list): Record of the Precision metric
        self._F1_score (list): Record of the F1 metric
        """
        truth = {item["field"]: item["value"] for item in ltruth}
        if (leakage(sut)):
            self._precision.append(precision(sut, truth))
            self._recall.append(recall(sut, truth))
            self._F1_score.append(f1_score(sut, truth))
        else:
            print("No Leakage!")

    def print_records(self):
        init()
        UNDERLINE = "\033[4m"

        print(f"\n{Style.BRIGHT}{UNDERLINE}Precision{Style.RESET_ALL}: ", end="")
        if (self._precision):
            for i in range(len(self._precision)):
                print(f"{self._precision[i]:.2f}", end="\t")            
            if (self._precision[-1] <= 0.5):
                print(f" | {Fore.RED}{self._precision[-1]:.2f}{Style.RESET_ALL} ({Fore.GREEN}High Data Protection{Style.RESET_ALL})")
            elif (self._precision[-1] > 0.5 and self._precision[-1] <= 0.8):
                print(f" | {Fore.YELLOW}{self._precision[-1]:.2f}{Style.RESET_ALL} ({Fore.YELLOW}Medium Data Protection{Style.RESET_ALL})")
            else:
                print(f" | {Fore.GREEN}{self._precision[-1]:.2f}{Style.RESET_ALL} ({Fore.RED}Low Data Protection{Style.RESET_ALL})")
        else:
            print(f"{Fore.RED}No Measurement can be made!{Style.RESET_ALL}")


        print(f"\n{Style.BRIGHT}{UNDERLINE}Recall{Style.RESET_ALL}: ", end="")
        if (self._recall):
            for i in range(len(self._recall)):
                print(f"{self._recall[i]:.2f}", end="\t")            
            if (self._recall[-1] <= 0.5):
                print(f" | {Fore.RED}{self._recall[-1]:.2f}{Style.RESET_ALL} ({Fore.GREEN}High Data Protection{Style.RESET_ALL})")
            elif (self._recall[-1] > 0.5 and self._recall[-1] <= 0.8):
                print(f" | {Fore.YELLOW}{self._recall[-1]:.2f}{Style.RESET_ALL} ({Fore.YELLOW}Medium Data Protection{Style.RESET_ALL})")
            else:
                print(f" | {Fore.GREEN}{self._recall[-1]:.2f}{Style.RESET_ALL} ({Fore.RED}Low Data Protection{Style.RESET_ALL})")
        else:
            print(f"{Fore.RED}No Measurement can be made!{Style.RESET_ALL}")


        print(f"\n{Style.BRIGHT}{UNDERLINE}F1-Score{Style.RESET_ALL}: ", end="")
        if (self._F1_score):
            for i in range(len(self._F1_score)):
                print(f"{self._F1_score[i]:.2f}", end="\t")            
            if (self._F1_score[-1] <= 0.5):
                print(f" | {Fore.RED}{self._F1_score[-1]:.2f}{Style.RESET_ALL} ({Fore.GREEN}High Data Protection{Style.RESET_ALL})")
            elif (self._F1_score[-1] > 0.5 and self._F1_score[-1] <= 0.8):
                print(f" | {Fore.YELLOW}{self._F1_score[-1]:.2f}{Style.RESET_ALL} ({Fore.YELLOW}Medium Data Protection{Style.RESET_ALL})")
            else:
                print(f" | {Fore.GREEN}{self._F1_score[-1]:.2f} ({Fore.RED}Low Data Protection{Style.RESET_ALL})")
        else:
            print(f"{Fore.RED}No Measurement can be made!{Style.RESET_ALL}")




def leakage(sut: dict) -> bool:
    if not sut:
        return (False)
    return (True)

def precision(sut: dict, truth: dict) -> float:
    """
    Calculates the precision score for two dictionaries.

    Precision is the fraction of correctly identified items out of all
    items identified by the system under test (sut).

    Args:
        sut (dict): The system's output.
        truth (dict): The ground truth values.

    Returns:
        float: The precision score. Returns 0.0 if the sut dictionary is empty.
    """
    common_labels = set(sut.keys()) & set(truth.keys())
    total_correctly_identified = 0
    total_sut_values = 0

    for label in common_labels:
        sut_values = set(sut[label])
        truth_values = set(truth[label])
        total_correctly_identified += len(sut_values & truth_values)
        total_sut_values += len(sut_values)
    sut_only_labels = set(sut.keys()) - set(truth.keys())
    for label in sut_only_labels:
        total_sut_values += len(sut[label])
    if total_sut_values == 0:
        return 0.0
    return total_correctly_identified / total_sut_values


def recall(sut: dict, truth: dict) -> float:
    """
    Calculates the recall score for two dictionaries.

    Recall is the fraction of correct values from the 'truth' dictionary
    that were successfully identified by the 'sut' dictionary.

    Args:
        sut (dict): The system's output.
        truth (dict): The ground truth values.

    Returns:
        float: The recall score. Returns 0.0 if there are no truth values.
    """
    common_labels = set(sut.keys()) & set(truth.keys())
    total_correctly_identified = 0
    total_truth_values = 0

    for label in common_labels:
        sut_values = set(sut[label])
        truth_values = set(truth[label])
        total_correctly_identified += len(sut_values & truth_values)
        total_truth_values += len(truth_values)
    truth_only_labels = set(truth.keys()) - set(sut.keys())
    for label in truth_only_labels:
        total_truth_values += len(truth[label])
    if total_truth_values == 0:
        return 0.0
    return total_correctly_identified / total_truth_values


def f1_score(sut: dict, truth: dict) -> float:
    """
    Calculates the F1-Score, which is the harmonic mean of precision and recall.

    Args:
        sut (dict): The system's output.
        truth (dict): The ground truth values.

    Returns:
        float: The F1-Score. Returns 0.0 if both precision and recall are 0.
    """
    p = precision(sut, truth)
    r = recall(sut, truth)
    if p + r == 0:
        return 0.0
    return 2 * (p * r) / (p + r)
