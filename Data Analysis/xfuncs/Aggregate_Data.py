import pandas as pd
import glob
import os

# gather all per‑state CSVs
csv_files = glob.glob(r"Datasets\AquaStat Data Each state\*_climate_2022.csv")
dfs = []
for fp in csv_files:
    state = os.path.basename(fp) \
              .replace("_climate_2022.csv", "") \
              .replace("_", " ")
    df = pd.read_csv(fp)
    df["state"] = state
    dfs.append(df)

# concatenate
if dfs:
    all_states = pd.concat(dfs, ignore_index=True)

    # drop any “Total” rows under Month
    all_states = all_states[all_states["Month"] != "Total"]

    # write out
    out_path = r"Datasets/all_states_climate_2022.csv"
    all_states.to_csv(out_path, index=False)
    print(f"→ Aggregated {len(dfs)} files (minus Totals) into {out_path}")
else:
    print("⚠ No CSV files found to aggregate.")