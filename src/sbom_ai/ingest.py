import os
import pandas as pd
from cyclonedx.parser import JsonParser, XmlParser

def parse_sbom_folder(folder_path: str) -> pd.DataFrame:
    rows = []
    for fname in os.listdir(folder_path):
        path = os.path.join(folder_path, fname)
        if fname.endswith(".json"):
            parser = JsonParser(file_path=path)
        elif fname.endswith(".xml"):
            parser = XmlParser(file_path=path)
        else:
            continue
        bom = parser.parse()
        for comp in bom.components:
            rows.append({
                "component_name": comp.name,
                "version": comp.version,
                "purl": comp.purl,
                "package_type": comp.type.value if comp.type else "",
            })
    return pd.DataFrame(rows)
