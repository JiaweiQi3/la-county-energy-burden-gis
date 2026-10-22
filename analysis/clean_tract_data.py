import pandas as pd
import numpy as np


# 1. Load dataset
df = pd.read_excel("LA_County_Full_Table.xlsx")

# 2. Keep only necessary columns
keep_cols = [
    "GEOID",
    "energy_burden_pctage",
    "energy_burden_li_pctage",
    "B19013_001E",
    "B25003_001E",
    "B25003_002E",
    "B25034_001E",
    "B25034_011E",
    "Shape_Length",
    "Shape_Area"
]

df = df[[col for col in keep_cols if col in df.columns]].copy()

# 3. Rename columns (English, clear, GIS-friendly)
df = df.rename(columns={
    "energy_burden_pctage": "REB",
    "energy_burden_li_pctage": "REB_LI",
    "B19013_001E": "Median_Income",
    "B25003_001E": "Total_Units",
    "B25003_002E": "Renter_Units",
    "B25034_001E": "Total_Age_Units",
    "B25034_011E": "Old_Units"
})

# 4. Convert numeric fields
numeric_cols = [
    "REB", "REB_LI", "Median_Income",
    "Total_Units", "Renter_Units",
    "Total_Age_Units", "Old_Units"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 5. Remove abnormal values
# Remove negative or impossible values
for col in ["REB", "Median_Income", "Total_Units", "Renter_Units", "Old_Units"]:
    df = df[df[col] >= 0]

# Remove known ACS error codes
error_codes = [-9999, -666666, -222222]
for col in ["REB", "Median_Income", "Total_Units", "Renter_Units", "Old_Units"]:
    df = df[~df[col].isin(error_codes)]

# Drop rows missing essential values
df = df.dropna(subset=["REB", "Median_Income", "Total_Units", "Renter_Units", "Old_Units"])

# 6. Create new indicator variables
# Renter percentage
df["Renter_Percentage"] = np.where(
    df["Total_Units"] > 0,
    df["Renter_Units"] / df["Total_Units"] * 100,
    np.nan
)

# Old housing percentage
df["Old_Housing_Percentage"] = np.where(
    df["Total_Age_Units"] > 0,
    df["Old_Units"] / df["Total_Age_Units"] * 100,
    np.nan
)

# Remove rows missing derived indicators
df = df.dropna(subset=["Renter_Percentage", "Old_Housing_Percentage"])

# 7. Final numeric check
final_numeric = [
    "REB", "REB_LI", "Median_Income",
    "Total_Units", "Renter_Units",
    "Old_Units", "Renter_Percentage",
    "Old_Housing_Percentage"
]

for col in final_numeric:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=final_numeric)

# 8. Export cleaned dataset
df.to_excel("LA_County_Cleansed.xlsx", index=False)

print("Cleaning complete. Output saved as LA_County_Cleansed.xlsx")