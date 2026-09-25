"""Extract UCI diabetes hospital dataset and save to csv."""

from pathlib import Path
from pprint import pprint
import textwrap

from ucimlrepo import fetch_ucirepo 


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

DATA_PATH = RAW_DIR / "diabetes_130_us_hospitals_for_years_1999_2008.csv"
VARIABLES_PATH = RAW_DIR / "diabetes_130_us_hospitals_variables.csv"

  
def extract_data():
    """Fetch the UCI diabetes hospital dataset."""
    dataset = fetch_ucirepo(id=296) 
  
    df = dataset.data.original.copy()
    variables_df = dataset.variables.copy()


    return dataset, df, variables_df
  

def inspect_data(dataset, df):
    """Print basic dataset information for initial exploration."""
    print("\n--- Metadata ---")
    pprint(
        dataset.metadata,
        width=150,
        sort_dicts=False
    )
    
    print("\n--- Variables ---")
    for _, row in dataset.variables.iterrows():
        print("\n" + "=" * 150)

        for column, value in row.items():
            if column == "description":
                value = textwrap.fill(str(value), width=150)
            print(f"{column}: {value}")
            

    print("\n--- Data Preview ---")
    print(df.head())

    print("\n--- Data Shape ---")
    print(df.shape)


def save_data(df, variables_df):
    """Save the raw dataset and variable metadata."""
    try:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise RuntimeError(
            f"Could not create directory {RAW_DIR}: {e}"
        )
    
    df.to_csv(DATA_PATH, index=False)
    variables_df.to_csv(VARIABLES_PATH)
    print(f"\nSaved raw data to: {DATA_PATH}")
    print(f"\nSaved variable metadata to: {VARIABLES_PATH}")


def main():
    dataset, df, variables_df = extract_data()
    inspect_data(dataset, df)
    save_data(df, variables_df)


if __name__ == "__main__":
    main()