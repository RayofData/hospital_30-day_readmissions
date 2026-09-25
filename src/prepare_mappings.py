"""Prepare lookup tables from the UCI ID mapping file."""

import csv
from pathlib import Path

import pandas as pd 


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

MAPPING_PATH = RAW_DIR / "IDS_mapping.csv"

FILE_NAMES = {
    "admission_type_id": "admission_type_lookup.csv",
    "discharge_disposition_id": "discharge_disposition_lookup.csv",
    "admission_source_id": "admission_source_lookup.csv",
}


def load_mapping_file():
    """Read the raw UCI mapping file."""
    with open(MAPPING_PATH, encoding="utf-8") as file:
        lines = file.readlines()

    return lines


def find_header_indexes(lines):
    """Find the starting line of each lookup table."""
    header_indexes = []

    for i, line in enumerate(lines):
        if line.strip().endswith("_id,description"):
            header_indexes.append(i)

    
    return header_indexes


def create_tables(lines, header_indexes):
    """Create DataFrames for the lookup table sections."""
    tables = {}

    for position, start in enumerate(header_indexes):
        if position + 1 < len(header_indexes):
            end = header_indexes[position + 1]
        else:
            end = len(lines)

        table_lines = [
            line
            for line in lines[start:end]
            if line.strip() not in {"", ","}
        ]

        rows = list(csv.reader(table_lines))

        header = rows[0]
        data = rows[1:]

        table_name = header[0]
        tables[table_name] = pd.DataFrame(
            data,
            columns=header
        )


    return tables 


def save_tables(tables):
    """Save cleanup lookup tables to the processed directory."""
    try:
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise RuntimeError(
            f"Could not create directory {PROCESSED_DIR}: {e}"
        )

    for table_name, df in tables.items():
        file_name = FILE_NAMES[table_name]
        file_path = PROCESSED_DIR / file_name

        df.to_csv(file_path, index=False)

        print(f"Saved: {file_path}")


def main():
    lines = load_mapping_file()

    header_indexes = find_header_indexes(lines)
    tables = create_tables(lines, header_indexes)

    save_tables(tables)


if __name__ == "__main__":
    main()