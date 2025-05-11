import pandas as pd
from pathlib import Path
import os
from typing import Dict, List

from scripts.constants import PROJECT_ROOT, KPI_LABELS, SEGMENTS

def read_text_file(file_path: str) -> str:
    """
    Reads a UTF-8 encoded text file and returns its content as a string.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: The full content of the file as a single string.
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"The file does not exist: {file_path}")
    if path.suffix.lower() != ".txt":
        raise ValueError("Only .txt files are supported.")
    
    try:
        with path.open("r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Failed to read file '{file_path}': {e}")

def load_ifo_data(csv_path: Path) -> pd.DataFrame:
    """
    Load and preprocess IFO business climate data from a prepared CSV file.

    Args:
        csv_path (Path): Path to the prepared IFO CSV file

    Returns:
        pd.DataFrame: Preprocessed DataFrame with datetime index
    """
    # Read CSV with proper separators and decimal handling
    df = pd.read_csv(csv_path, sep=";", decimal=",")

    # Convert 'Monat/Jahr' to datetime
    df['Monat/Jahr'] = pd.to_datetime(df['Monat/Jahr'], format=" %m/%Y")

    # Normalize column names
    df.columns = [
        col.strip().lower()
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
        for col in df.columns
    ]

    # Set date as index (optional, useful for time series work)
    df.set_index("monat/jahr", inplace=True)
    df.dropna(how="all", inplace=True, axis='columns')
    df.dropna(how="all", inplace=True, axis='index')

    return df
    
def extract_metrics_from_excel(path: Path) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Extract key financial KPIs from multiple sheets within a financial summary Excel file using flexible keyword matching.

    Args:
        path (Path): Path to the Excel file

    Returns:
        Dict[str, Dict[str, Dict[str, str]]]: Nested dictionary of segment → KPI → period → value
    """
    xls = pd.ExcelFile(path)
    data = {}

    for sheet, segment_key in SEGMENTS.items():
        df = xls.parse(sheet, header=None)
        headers = df.iloc[3]
        content_df = df.iloc[5:].copy()
        content_df.columns = headers
        content_df.dropna(how="all", inplace=True)
        content_df.fillna("", inplace=True)

        segment_data = {}

        for row_idx, row in content_df.iterrows():
            row_label = str(row.iloc[0]).lower()
            for kpi_key, keywords in KPI_LABELS.items():
                if any(kw in row_label for kw in keywords):
                    values = row.iloc[1:]
                    metrics = {
                        str(period).replace(" ", "_").replace(".", "").replace("\n", "_").strip(): str(v).strip()
                        for period, v in zip(values.index, values.values)
                        if str(v).strip() != ""
                    }
                    segment_data[kpi_key] = metrics

        data[segment_key] = segment_data

    return data
