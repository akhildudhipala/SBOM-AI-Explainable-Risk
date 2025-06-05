import argparse
import yaml
import joblib
import pandas as pd
from sbom_ai.ingest import parse_sbom_folder
from sbom_ai.features import load_nvd_cves, load_cisa_kev, build_feature_table
from sbom_ai.labeler import apply_rule_labeling

class SBOMRiskPipeline:
    def __init__(self, model, config):
        self.model = model
        self.config = config

    def predict(self, sbom_folder):
        # Ingest SBOMs
        df_comps = parse_sbom_folder(sbom_folder)
        # Build features
        nvd_df = load_nvd_cves(self.config["nvd_path"])
        kev_set = load_cisa_kev(self.config["cisa_path"])
        features_df = build_feature_table(df_comps, nvd_df, kev_set, self.config)
        # Predict risk probabilities
        X = features_df.drop(columns=["label"], errors="ignore")
        proba = self.model.predict_proba(X)[:, 1]
        return pd.DataFrame({
            "component": features_df["component_name"],
            "cve": features_df.get("cve_id", None),
            "risk_score": proba
        })

def main():
    parser = argparse.ArgumentParser(description="Export SBOM-AI pipeline as a single artifact")
    parser.add_argument("--models-dir", required=True, help="Directory containing saved models")
    parser.add_argument("--config", required=True, help="Path to config/default_config.yaml")
    parser.add_argument("--output", required=True, help="Path to save final_pipeline.pkl")
    args = parser.parse_args()

    # Load config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    # Load final model (e.g., CatBoost)
    from catboost import CatBoostClassifier
    model = CatBoostClassifier()
    model.load_model(f"{args.models_dir}/catboost_model.cbm")

    pipeline = SBOMRiskPipeline(model, config)
    joblib.dump(pipeline, args.output)
    print(f"✅ Pipeline artifact saved to {args.output}")

if __name__ == "__main__":
    main()
