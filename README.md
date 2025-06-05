# SBOM-AI Explainable Risk Classification (Code-Only)

## Overview

SBOM-AI is an explainable machine-learning framework designed to prioritize high-risk components in software supply chains. This repository contains **only the code** needed to reproduce the entire pipeline:

1. Ingest CycloneDX SBOM files  
2. Fetch NVD & CISA KEV vulnerability feeds  
3. Build a feature table (CVSS scores, exploit flags, runtime flags, etc.)  
4. Apply deterministic rule labeling for “High Risk” vs. “Low Risk”  
5. Train RandomForest, LightGBM, and CatBoost models  
6. Evaluate each model (metrics only; plots generated at runtime)  
7. Compute SHAP explainability plots (summary + force)  
8. (Optional) Bundle the entire pipeline as a single artifact

All data outputs (CSVs, model binaries, images) are **not** included here—users must download or generate them locally and run the scripts to produce results.

---

## Prerequisites

- **Python 3.8+**  
- At least **8 GB of RAM** (NVD JSON can be large)  
- Operating System: Linux, macOS, or Windows (with appropriate Python setup)

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/SBOM-AI-Explainable-Risk.git
   cd SBOM-AI-Explainable-Risk
