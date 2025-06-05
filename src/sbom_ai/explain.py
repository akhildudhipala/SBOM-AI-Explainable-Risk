import shap
import pandas as pd
import matplotlib.pyplot as plt

def compute_shap_summary(model, X, output_path: str):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    shap.summary_plot(shap_values, X, show=False)
    plt.savefig(output_path, bbox_inches="tight")
    plt.clf()

def compute_shap_force(model, X_row: pd.DataFrame, output_path: str):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_row)
    shap.force_plot(explainer.expected_value, shap_values, X_row, matplotlib=True)
    plt.savefig(output_path, bbox_inches="tight")
    plt.clf()
