import argparse
import pandas as pd
import json
import yaml
from sbom_ai.features import load_nvd_cves, load_cisa_kev, build_feature_table

def main():
    parser = argparse.ArgumentParser(description="Build feature table from components and vulnerability feeds")
    parser.add_argument("--components", required=True, help="Path to components CSV (from step 1)")
    parser.add_argument("--nvd", required=True, help="Path to nvd_cve_feed.json")
    parser.add_argument("--cisa", required=True, help="Path to cisa_kev_list.csv")
    parser.add_argument("--config", required=True, help="Path to config/default_config.yaml")
    parser.add_argument("--output", required=True, help="Output CSV path for enriched features")
    args = parser.parse_args()

    # Load config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    # Load data
    df_comps = pd.read_csv(args.components)
    nvd_df = load_nvd_cves(args.nvd)
    kev_set = load_cisa_kev(args.cisa)

    # Build features
    features_df = build_feature_table(df_comps, nvd_df, kev_set, config)

    features_df.to_csv(args.output, index=False)
    print(f"✅ Enriched features saved to {args.output}")

if __name__ == "__main__":
    main()
