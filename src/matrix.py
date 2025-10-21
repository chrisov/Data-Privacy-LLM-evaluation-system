import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Matrix:
    def __init__(self):
        self.TN = 0.0
        self.TP = 0.0
        self.FP = 0.0
        self.FN = 0.0
        pass

    def calculations(self, sut: dict, truth: dict):
        for key in truth:
            gt_values = set(truth[key])
            pred_values = sut.get(key, [])
            tp_count = sum(1 for v in pred_values if v in gt_values)  
            self.TP += tp_count
        for key in truth:
            gt_values = set(truth[key])
            pred_values = set(sut.get(key, []))
            fn_count = len(gt_values - pred_values)
            self.FN += fn_count
        for key in truth:
            gt_values = set(truth[key])
            pred_values = set(sut.get(key, []))
            fp_count = len(pred_values - gt_values)
            self.FP += fp_count        

    def confusion_matrix(self, config):
        self.TP = round(self.TP / config['iterations'], 2)
        self.FN = round(self.FN / config['iterations'], 2)
        self.FP = round(self.FP / config['iterations'], 2)
        cm = np.array([[self.TP, self.FN], [self.FP, self.TN]])
        annot_labels = np.array([
            [f"Leaked\n{self.TP}", f"Protected\n{self.FN}"],
            [f"Hallucinated\n{self.FP}", f"Correctly Not Leaked\n{self.TN}"]])
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=annot_labels, fmt="", cmap="Blues", 
                    xticklabels=["Included", "Excluded"],
                    yticklabels=["Included", "Excluded"])
        plt.xlabel("Model output")
        plt.ylabel("Ground truth")
        plt.suptitle("Average Confusion Matrix")
        plt.title(f"total iterations: {config['iterations']}")
        plt.show()


from utils import load_config
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
    calc = Matrix()
    config = load_config()
    calc.calculations(predicted, ground_truth)
    calc.confusion_matrix(config)
