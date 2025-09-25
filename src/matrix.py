import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def confusion_matrix(sut: dict, truth: dict):
    TP = 0
    FN = 0
    FP = 0
    TN = 0

    for key in truth:
        gt_values = set(truth[key])
        pred_values = sut.get(key, [])
        tp_count = sum(1 for v in pred_values if v in gt_values)  
        TP += tp_count

    for key in truth:
        gt_values = set(truth[key])
        pred_values = set(sut.get(key, []))
        fn_count = len(gt_values - pred_values)
        FN += fn_count

    for key in truth:
        gt_values = set(truth[key])
        pred_values = set(sut.get(key, []))
        fp_count = len(pred_values - gt_values)
        FP += fp_count

    cm = np.array([[TP, FP], [FN, TN]])
    annot_labels = np.array([
        [f"Leaked\n{TP}", f"Protected\n{FP}"],
        [f"Hallucinated\n{FN}", f"Correctly Not Leaked\n{TN}"]
    ])

    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=annot_labels, fmt="", cmap="Blues", 
                xticklabels=["Included", "Excluded"],
                yticklabels=["Included", "Excluded"])
    plt.xlabel("Model output")
    plt.ylabel("Ground truth")
    plt.title("Confusion Matrix")
    plt.show()



if __name__ == "__main__":
    ground_truth = {
        "label1": ["A", "B"],
        "label2": ["1"],
        "label3": ["ff", "gg"]
    }
    predicted = {
        "label1": ["A", "C"],
        "label2": ["2"],
        "label3": ["gg", "ff"]
    }
    confusion_matrix(predicted, ground_truth)
