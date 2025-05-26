import pandas as pd

def load_flow_data(path: str = "app/sample_data.csv") -> pd.DataFrame:
    """
    Load network flow data from a CSV file.

    Args:
        path (str): Path to the CSV file containing flow data.

    Returns:
        pd.DataFrame: DataFrame with the flow data.
    """
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at: {path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV file at {path} is empty")
    except Exception as e:
        raise RuntimeError(f"Error loading CSV file: {e}")

    return df
