import pandas as pd
import json

def load_nvd_cves(nvd_json_path: str) -> pd.DataFrame:
    with open(nvd_json_path) as f:
        raw = json.load(f)
    items = raw.get("CVE_Items", [])
    rows = []
    for entry in items:
        cve_id = entry["cve"]["CVE_data_meta"]["ID"]
        impact = entry.get("impact", {}).get("baseMetricV3", {})
        base_cvss = impact.get("cvssV3", {}).get("baseScore", None)
        conf = impact.get("cvssV3", {}).get("confidentialityImpact", None)
        integ = impact.get("cvssV3", {}).get("integrityImpact", None)
        avail = impact.get("cvssV3", {}).get("availabilityImpact", None)
        exploit_exists = entry.get("exploitability", {}).get("hasExploit", False)
        rows.append({
            "cve_id": cve_id,
            "cvss_v3_base_score": base_cvss,
            "cvss_v3_confidentiality_subscore": conf,
            "cvss_v3_integrity_subscore": integ,
            "cvss_v3_availability_subscore": avail,
            "exploit_exists": exploit_exists
        })
    return pd.DataFrame(rows)

def load_cisa_kev(csv_path: str) -> set:
    df = pd.read_csv(csv_path)
    return set(df['cveID'].tolist())

def build_feature_table(components_df: pd.DataFrame,
                        nvd_df: pd.DataFrame,
                        kev_set: set,
                        config: dict) -> pd.DataFrame:
    # For illustration: cross-join all components with all CVEs.
    # In a real pipeline, you would join only relevant CVEs based on purl or component name.
    df = components_df.copy()
    df['merge_key'] = 1
    nvd_df['merge_key'] = 1
    merged = pd.merge(df, nvd_df, on='merge_key').drop(columns=['merge_key'])

    # Compute flags
    merged['cisa_kev_flag'] = merged['cve_id'].isin(kev_set).astype(int)
    merged['runtime_critical_flag'] = merged['component_name'].apply(
        lambda x: int(any(k in x.lower() for k in config.get('runtime_critical_keywords', [])))
    )

    # Add label column placeholder (will be overwritten in labeling)
    merged['label'] = 0
    return merged
