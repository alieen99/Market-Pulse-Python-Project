import pandas as pd
import numpy as np
from typing import Optional


def calculate_returns(
    df: pd.DataFrame,
    price_column: str = 'Close',
    group_by: Optional[str] = 'Ticker'
) -> pd.DataFrame:
    df_copy = df.copy()
    
    if group_by:
        df_copy['Returns'] = df_copy.groupby(group_by)[price_column].pct_change()
    else:
        df_copy['Returns'] = df_copy[price_column].pct_change()
    
    return df_copy


def calculate_log_returns(
    df: pd.DataFrame,
    price_column: str = 'Close',
    group_by: Optional[str] = 'Ticker'
) -> pd.DataFrame:
    df_copy = df.copy()
    
    if group_by:
        df_copy['Log_Returns'] = df_copy.groupby(group_by)[price_column].apply(
            lambda x: np.log(x / x.shift(1))
        )
    else:
        df_copy['Log_Returns'] = np.log(df_copy[price_column] / df_copy[price_column].shift(1))
    
    return df_copy


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = "forward_fill"
) -> pd.DataFrame:


    df_copy = df.copy()
    
    if strategy == "drop":
        return df_copy.dropna()
    elif strategy == "forward_fill":
        return df_copy.fillna(method="ffill")
    elif strategy == "backward_fill":
        return df_copy.fillna(method="bfill")
    elif strategy == "interpolate":
        numeric_columns = df_copy.select_dtypes(include=[np.number]).columns
        df_copy[numeric_columns] = df_copy[numeric_columns].interpolate(method='linear')
        return df_copy
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def filter_outliers(
    df: pd.DataFrame,
    column: str,
    method: str = "iqr",
    threshold: float = 1.5
) -> pd.DataFrame:

    df_copy = df.copy()
    
    if column not in df_copy.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    if not pd.api.types.is_numeric_dtype(df_copy[column]):
        raise ValueError(f"Column '{column}' is not numeric")
    
    if method == "iqr":
        Q1 = df_copy[column].quantile(0.25)
        Q3 = df_copy[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return df_copy[(df_copy[column] >= lower_bound) & (df_copy[column] <= upper_bound)]
    elif method == "z-score":
        z_scores = np.abs((df_copy[column] - df_copy[column].mean()) / df_copy[column].std())
        return df_copy[z_scores < threshold]
    else:
        raise ValueError(f"Unknown outlier detection method: {method}")


def pivot_stock_data(
    df: pd.DataFrame,
    index_col: str = 'Date',
    columns_col: str = 'Ticker',
    values_col: str = 'Close'
) -> pd.DataFrame:

    return df.pivot(index=index_col, columns=columns_col, values=values_col)

