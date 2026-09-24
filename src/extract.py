import os
from pathlib import Path


from ucimlrepo import fetch_ucirepo 
from pprint import pprint
import pandas as pd 

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
FILE_PATH = RAW_DIR / "diabetes_130_us_hospitals_for_years_1999_2008.csv"
  
# fetch dataset 
diabetes_130_us_hospitals_for_years_1999_2008 = fetch_ucirepo(id=296) 
  
# data (as pandas dataframes) 
X = diabetes_130_us_hospitals_for_years_1999_2008.data.features 
y = diabetes_130_us_hospitals_for_years_1999_2008.data.targets 
  
# metadata 
pprint(
    diabetes_130_us_hospitals_for_years_1999_2008.metadata,
    width=125,
    sort_dicts=False
)
  
# variable information 
print(diabetes_130_us_hospitals_for_years_1999_2008.variables) 

df = pd.concat([X, y], axis=1)
print(df.head())
print(df.shape)

try:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
except OSError as e:
    raise RuntimeError(
        f"Could not create weather directory {RAW_DIR}: {e}"
    )

df.to_csv(FILE_PATH)