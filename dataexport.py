import os
import pandas as pd
from cliColors import success

def export_all(hotspots, filename, export_dir):
    os.makedirs(export_dir, exist_ok=True)
    filepath = os.path.join(export_dir, filename)
    print(filepath)
    df = pd.DataFrame(hotspots)
    df.to_excel(filename, index=False)
    success(f"Exported {len(hotspots)} hotspots to '{filepath}'.")