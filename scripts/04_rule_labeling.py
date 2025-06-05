import argparse
import pandas as pd
import yaml
from sbom_ai.labeler import apply_rule_labeling

def main():
    parser = argparse.ArgumentParser(description="Apply rule-based labeling to feature table")
    parser.add_argument("--features", required=True, help="Path to enriched_features.csv")
    parser.add_argument("--config", required=True, help="Path to config/default_config.yaml")
    parser.add_argument("--output", required=True, help="Output CSV path for labeled data")
    args = parser.parse_args()

    # Load config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    # Load features
    df = pd.read_csv(args.features)

    # Apply labeling
    labeled_df = apply_rule_labeling(df, config)
    labeled_df.to_csv(args.output, index=False)
    print(f"✅ Labeled data saved to {args.output}")

if __name__ == "__main__":
    main()
