import argparse
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def main():
    parser = argparse.ArgumentParser(description="Evaluate trained models on test data")
    parser.add_argument("--models-dir", required=True, help="Directory containing saved models")
    parser.add_argument("--test-data", required=True, help="Path to CSV with features and label")
    parser.add_argument("--metrics-output", required=True, help="Path to output metrics CSV")
    args = parser.parse_args()

    df_test = pd.read_csv(args.test_data)
    X_test = df_test.drop(columns=["label"])
    y_test = df_test["label"]

    rows = []
    for model_name, filename in [
        ("RandomForest", "random_forest.pkl"),
        ("LightGBM", "lightgbm_model.txt"),
        ("CatBoost", "catboost_model.cbm"),
    ]:
        # Load model
        if model_name == "RandomForest":
            model = joblib.load(f"{args.models_dir}/{filename}")
        elif model_name == "LightGBM":
            from lightgbm import Booster
            model = Booster(model_file=f"{args.models_dir}/{filename}")
        else:
            from catboost import CatBoostClassifier
            model = CatBoostClassifier()
            model.load_model(f"{args.models_dir}/{filename}")

        # Predictions
        if model_name == "RandomForest":
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]
        else:
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]

        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc = roc_auc_score(y_test, y_proba)

        rows.append({
            "model": model_name,
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
            "roc_auc": roc
        })

    metrics_df = pd.DataFrame(rows)
    metrics_df.to_csv(args.metrics_output, index=False)
    print(f"✅ Metrics saved to {args.metrics_output}")

if __name__ == "__main__":
    main()
