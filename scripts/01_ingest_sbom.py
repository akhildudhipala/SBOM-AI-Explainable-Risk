import argparse
import os
import pandas as pd
from sbom_ai.ingest import parse_sbom_folder

def main():
    parser = argparse.ArgumentParser(description="Ingest CycloneDX SBOMs into CSV")
    parser.add_argument("--input", required=True, help="Folder containing CycloneDX SBOM JSON/XML files")
    parser.add_argument("--output", required=True, help="Output CSV file path for components")
    args = parser.parse_args()

    df = parse_sbom_folder(args.input)
    df.to_csv(args.output, index=False)
    print(f"✅ Components CSV saved to {args.output}")

if __name__ == "__main__":
    main()
