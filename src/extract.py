"""Extract UCI diabetes hospital dataset and save to csv."""

from pathlib import Path
from pprint import pprint

import pandas as pd 
from ucimlrepo import fetch_ucirepo 

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
FILE_PATH = RAW_DIR / "diabetes_130_us_hospitals_for_years_1999_2008.csv"

  
def extract_data():
    """Fetch the UCI diabetes hospital dataset."""
    dataset = fetch_ucirepo(id=296) 
  

    X = dataset.data.features 
    y = dataset.data.targets 

    df = pd.concat([X, y], axis=1)

    return dataset, df
  

def inspect_data(dataset, df):
    """Print basic dataset information for initial exploration."""
    print("\n--- Metadata ---")
    pprint(
        dataset.metadata,
        width=125,
        sort_dicts=False
    )
    
    print("\n--- Variables ---")
    print(dataset.variables.to_string()) 

    print("\n--- Data Preview ---")
    print(df.head())

    print("\n--- Data Shape ---")
    print(df.shape)


def save_data(df):
    """Save the raw dataset to the project data directory."""
    try:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise RuntimeError(
            f"Could not create directory {RAW_DIR}: {e}"
        )
    
    df.to_csv(FILE_PATH, index=False)
    print(f"\nSaved raw data to: {FILE_PATH}")


def main():
    dataset, df = extract_data()
    inspect_data(dataset, df)
    save_data(df)


if __name__ == "__main__":
    main()