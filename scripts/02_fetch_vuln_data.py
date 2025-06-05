import argparse
import requests

def main():
    parser = argparse.ArgumentParser(description="Fetch NVD JSON and CISA KEV CSV")
    parser.add_argument("--nvd-url", help="URL to download NVD JSON feed", default=None)
    parser.add_argument("--nvd-output", required=True, help="Path to save nvd_cve_feed.json")
    parser.add_argument("--cisa-url", help="URL to download CISA KEV CSV", default=None)
    parser.add_argument("--cisa-output", required=True, help="Path to save cisa_kev_list.csv")
    args = parser.parse_args()

    if args.nvd_url:
        r = requests.get(args.nvd_url)
        with open(args.nvd_output, "wb") as f:
            f.write(r.content)
        print(f"✅ NVD JSON downloaded to {args.nvd_output}")
    else:
        print(f"⚠️  Please manually download NVD JSON to: {args.nvd_output}")

    if args.cisa_url:
        r = requests.get(args.cisa_url)
        with open(args.cisa_output, "wb") as f:
            f.write(r.content)
        print(f"✅ CISA KEV CSV downloaded to {args.cisa_output}")
    else:
        print(f"⚠️  Please manually download CISA KEV CSV to: {args.cisa_output}")

if __name__ == "__main__":
    main()
