import argparse
import pandas as pd
import os
import joblib
import yaml
from sbom_ai.trainer import train_random_forest, train_lightgbm, train_catboost, save_models
from sklearn.model_selection import train_test_split

def main():
    parser = argparse.ArgumentParser(description="Train ML models on labeled data")
    parser.add_argument("--input", required=True, help="Path to labeled.csv")
    parser.add_argument("--config", required=True, help="Path to config/default_config.yaml")
    parser.add_argument("--output-dir", required=True, help="Directory to save trained models")
    args = parser.parse_args()

    # Load config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    # Load labeled data
    df = pd.read_csv(args.input)
    X = df.drop(columns=["label"])
    y = df["label"]

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Train models
    rf = train_random_forest(X_train, y_train, config["models"]["random_forest"])
    lgbm = train_lightgbm(X_train, y_train, config["models"]["lightgbm"])
    cb = train_catboost(X_train, y_train, config["models"]["catboost"])

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    save_models(rf, lgbm, cb, args.output_dir)
    print(f"✅ Models saved to {args.output_dir}")

if __name__ == "__main__":
    main()
