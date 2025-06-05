import pandas as pd

def apply_rule_labeling(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    cond_cvss = (
        (df["cvss_v3_confidentiality_subscore"] >= config["cvss_confidentiality_threshold"])
        | (df["cvss_v3_availability_subscore"] >= config["cvss_availability_threshold"])
    )
    cond_exploit = df["exploit_exists"] == True
    cond_kev = df["cisa_kev_flag"] == True
    cond_runtime = df["runtime_critical_flag"] == True

    df["label"] = ((cond_cvss | cond_exploit | cond_kev | cond_runtime).astype(int))
    return df
