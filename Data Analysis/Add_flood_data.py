import pandas as pd
import calendar

# 1. load climate + state data
climate_path = r"Datasets\all_states_climate_2022.csv"
climate = pd.read_csv(climate_path)

# 2. load flood occurrences as strings, strip whitespace
flood = pd.read_csv(r"Datasets\flood_data_2022.csv", dtype=str)
flood["raw_date"] = flood["DATE OF OCCURRENCE"].fillna("").astype(str).str.strip()

# 3. drop blanks and filter valid dd/mm/YYYY dates
mask_valid = flood["raw_date"].str.match(r"^\d{1,2}/\d{1,2}/\d{4}$")
invalid = flood[~mask_valid]
if not invalid.empty:
    print("⚠ Invalid or blank dates:")
    print(invalid[["raw_date", "State"]])

flood = flood[mask_valid].copy()

# 4. parse to datetime
flood["DATE OF OCCURRENCE"] = pd.to_datetime(
    flood["raw_date"], dayfirst=True, format="%d/%m/%Y"
)

# 5. extract month abbrev (Jan, Feb, …)
flood["Month"] = flood["DATE OF OCCURRENCE"].dt.month.map(lambda m: calendar.month_abbr[m])

# 6. build set of (month, state) where flood occurred
flood_pairs = set(zip(
    flood["Month"],
    flood["State"].str.strip().str.title()
))

# 7. add flood flag to climate df
climate["flood"] = climate.apply(
    lambda r: 1 if (r["Month"], r["state"]) in flood_pairs else 0,
    axis=1
)

# 8. save augmented dataset
out_path = r"Datasets\all_states_climate_2022_with_flood.csv"
climate.to_csv(out_path, index=False)
print(f"→ Wrote augmented file with flood flag: {out_path}")