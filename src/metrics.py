# import matplotlib as plt
from colorama import init, Fore, Style

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

def print_records(pre_l: list, rec_l: list, f1_l: list):
        init()
        UNDERLINE = "\033[4m"

        print(f"\n{Style.BRIGHT}{UNDERLINE}Precision{Style.RESET_ALL}: ", end="")
        for i in range(len(pre_l) - 1):
            print(f"{pre_l[i]:.2f}", end="\t")            
        if (pre_l[-1] <= 0.5):
            print(f" | {Fore.RED}{pre_l[-1]:.2f}{Style.RESET_ALL} ({Fore.GREEN}High Data Protection{Style.RESET_ALL})")
        elif (pre_l[-1] > 0.5 and pre_l[-1] <= 0.8):
            print(f" | {Fore.YELLOW}{pre_l[-1]:.2f}{Style.RESET_ALL} ({Fore.YELLOW}Medium Data Protection{Style.RESET_ALL})")
        else:
            print(f" | {Fore.GREEN}{pre_l[-1]:.2f}{Style.RESET_ALL} ({Fore.RED}Low Data Protection{Style.RESET_ALL})")

        print(f"\n{Style.BRIGHT}{UNDERLINE}Recall{Style.RESET_ALL}: ", end="")
        for i in range(len(rec_l) - 1):
            print(f"{rec_l[i]:.2f}", end="\t")            
        if (rec_l[-1] <= 0.5):
            print(f" | {Fore.RED}{rec_l[-1]:.2f}{Style.RESET_ALL} ({Fore.GREEN}High Data Protection{Style.RESET_ALL})")
        elif (rec_l[-1] > 0.5 and rec_l[-1] <= 0.8):
            print(f" | {Fore.YELLOW}{rec_l[-1]:.2f}{Style.RESET_ALL} ({Fore.YELLOW}Medium Data Protection{Style.RESET_ALL})")
        else:
            print(f" | {Fore.GREEN}{rec_l[-1]:.2f}{Style.RESET_ALL} ({Fore.RED}Low Data Protection{Style.RESET_ALL})")

        print(f"\n{Style.BRIGHT}{UNDERLINE}F1-Score{Style.RESET_ALL}: ", end="")
        for i in range(len(f1_l) - 1):
            print(f"{f1_l[i]:.2f}", end="\t")            
        if (f1_l[-1] <= 0.5):
            print(f" | {Fore.RED}{f1_l[-1]:.2f}{Style.RESET_ALL} ({Fore.GREEN}High Data Protection{Style.RESET_ALL})")
        elif (f1_l[-1] > 0.5 and f1_l[-1] <= 0.8):
            print(f" | {Fore.YELLOW}{f1_l[-1]:.2f}{Style.RESET_ALL} ({Fore.YELLOW}Medium Data Protection{Style.RESET_ALL})")
        else:
            print(f" | {Fore.GREEN}{f1_l[-1]:.2f} ({Fore.RED}Low Data Protection{Style.RESET_ALL})")


def measure(sut: dict, truth: dict, pre_l: list, rec_l: list, f1_l: list):
    """
    Measures and prints different types of metrics
    
    Args:
        sut (dict): dict to be measured.
        truth (dict): Ground truth dict.
        rec_l (list): Record of the Recall metric
        pre_l (list): Record of the Precision metric
        f1_l (list): Record of the F1 metric
    """
    if (leakage(sut)):
        pre_l.append(precision(sut, truth))
        rec_l.append(recall(sut, truth))
        f1_l.append(f1_score(sut, truth))
    else:
        print("No Leakage!")

