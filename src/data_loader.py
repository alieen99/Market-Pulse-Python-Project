
import pandas as pd
import yfinance as yf
from pathlib import Path
from typing import List, Optional
from datetime import datetime


def fetch_stock_data(
    tickers: List[str],
    start_date: str,
    end_date: str,
    interval: str = "1d"
) -> pd.DataFrame:

    if not tickers:
        raise ValueError("Tickers list cannot be empty")
    
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Dates must be in format 'YYYY-MM-DD'")
    
    print(f"Fetching data for {len(tickers)} stocks from {start_date} to {end_date}...")
    
    all_data = []
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date, interval=interval)
            
            if hist.empty:
                print(f"Warning: No data found for {ticker}")
                continue
            
            hist['Ticker'] = ticker
            hist.reset_index(inplace=True)
            all_data.append(hist)
            print(f"✓ Fetched {len(hist)} records for {ticker}")
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")
            continue
    
    if not all_data:
        raise ValueError("No data was successfully retrieved for any ticker")
    
    combined_data = pd.concat(all_data, ignore_index=True)
    print(f"\nTotal records fetched: {len(combined_data)}")
    
    return combined_data


def load_csv(file_path: str, **kwargs) -> pd.DataFrame:

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return pd.read_csv(file_path, **kwargs)


def save_dataframe(
    df: pd.DataFrame,
    file_path: str,
    format: str = "csv",
    **kwargs
) -> None:

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == "csv":
        df.to_csv(file_path, index=False, **kwargs)
    elif format == "json":
        df.to_json(file_path, **kwargs)
    elif format == "excel":
        df.to_excel(file_path, index=False, **kwargs)
    elif format == "parquet":
        df.to_parquet(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    print(f"✓ Data saved to {file_path}")

