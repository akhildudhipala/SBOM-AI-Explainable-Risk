import argparse
import pandas as pd
import joblib
import shap
import os
from sbom_ai.explain import compute_shap_summary, compute_shap_force

def main():
    parser = argparse.ArgumentParser(description="Compute SHAP explainability plots")
    parser.add_argument("--models-dir", required=True, help="Directory containing saved models")
    parser.add_argument("--features", required=True, help="Path to enriched_features.csv")
    parser.add_argument("--output-dir", required=True, help="Directory to save SHAP plots")
    args = parser.parse_args()

    # Load features
    df = pd.read_csv(args.features)
    X = df.drop(columns=["label"]) if "label" in df.columns else df

    # Load CatBoost model for SHAP
    try:
        from catboost import CatBoostClassifier
        model = CatBoostClassifier()
        model.load_model(f"{args.models_dir}/catboost_model.cbm")
    except Exception as e:
        print(f"⚠️  Could not load CatBoost model for SHAP: {e}")
        return

    # Sample subset for SHAP (to speed up)
    X_sample = X.sample(n=min(500, len(X)), random_state=42)

    os.makedirs(args.output_dir, exist_ok=True)
    # Global summary
    summary_path = os.path.join(args.output_dir, "shap_summary.png")
    compute_shap_summary(model, X_sample, summary_path)
    print(f"✅ SHAP summary plot saved to {summary_path}")

    # Local force plot for the first high-risk sample (or first sample)
    high_risk_idx = X_sample.index[0]
    X_row = X_sample.loc[[high_risk_idx]]
    force_path = os.path.join(args.output_dir, "shap_force.png")
    compute_shap_force(model, X_row, force_path)
    print(f"✅ SHAP force plot saved to {force_path}")

if __name__ == "__main__":
    main()
