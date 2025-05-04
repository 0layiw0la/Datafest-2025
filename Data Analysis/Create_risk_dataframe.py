import pandas as pd

# Load data
df = pd.read_csv("Datasets/all_states_climate_2022_with_flood.csv")
df.columns = df.columns.str.replace('\n', ' ').str.strip()
df = df.rename(columns={
    'Prc. mm/m':  'precip',
    'Tmp. min.': 'tmin',
    'Tmp. max.': 'tmax',
    'Tmp. Mean':'tmean',
    'Rel. Hum. %':'rh',
    'Sun shine':'sun',
    'Wind (2m) m/s':'wind',
    'ETo mm/m':    'eto',
    'State':'state'
})

# Crop-specific weights
crop_weights = {
    'maize':   {'precip':0.3, 'tmean':0.2, 'rh':0.1, 'flood':0.4},
    'rice':    {'precip':0.4, 'tmean':0.1, 'rh':0.2, 'flood':0.3},
    'sorghum': {'precip':0.2, 'tmean':0.3, 'rh':0.1, 'flood':0.4},
}

# 4. Normalize each variable to [0,1]
vars_to_norm = set().union(*crop_weights.values())
norm_data = {}
for var in vars_to_norm:
    arr = df[var].astype(float)
    norm_data[var] = (arr - arr.min()) / (arr.max() - arr.min())

norm_df = pd.DataFrame(norm_data)
norm_df['state'] = df['state']
norm_df['Month'] = df['Month']

# 5. Compute risk index columns for each crop
for crop, weights in crop_weights.items():
    norm_df[crop] = sum(norm_df[var] * w for var, w in weights.items())

# 6. Aggregate by state & month
risk_df = (
    norm_df
    .groupby(['state','Month'], as_index=False)[list(crop_weights.keys())]
    .mean()
)

# 7. Save or display
risk_df.to_csv(r"Datasets\risk_index_by_state_month.csv", index=False)
print("→ Created risk dataframe with columns:", risk_df.columns.tolist())