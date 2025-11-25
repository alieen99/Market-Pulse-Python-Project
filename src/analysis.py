import pandas as pd
import numpy as np
from scipy import stats
from typing import Optional, Dict


def calculate_descriptive_stats(
    df: pd.DataFrame,
    columns: Optional[list] = None
) -> pd.DataFrame:

    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    return df[columns].describe()


def calculate_correlation(
    df: pd.DataFrame,
    method: str = "pearson"
) -> pd.DataFrame:

    numeric_df = df.select_dtypes(include=[np.number])

    if method not in ["pearson", "spearman", "kendall"]:
        raise ValueError(f"Unknown correlation method: {method}")

    return numeric_df.corr(method=method)


def calculate_volatility(
    returns: pd.Series,
    window: int = 30,
    annualize: bool = True
) -> pd.Series:

    volatility = returns.rolling(window=window).std()

    if annualize:
        volatility = volatility * np.sqrt(252)  # 252 trading days per year

    return volatility


def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.02,
    periods_per_year: int = 252
) -> float:

    excess_returns = returns - (risk_free_rate / periods_per_year)
    mean_excess_return = excess_returns.mean()
    std_excess_return = excess_returns.std()

    if std_excess_return == 0:
        return 0.0

    sharpe = (mean_excess_return / std_excess_return) * np.sqrt(periods_per_year)
    return sharpe


def calculate_max_drawdown(prices: pd.Series) -> Dict[str, float]:

    cumulative_max = prices.expanding().max()
    drawdown = (prices - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min()

    max_drawdown_idx = drawdown.idxmin()
    peak_idx = prices[:max_drawdown_idx].idxmax()

    return {
        'max_drawdown': max_drawdown,
        'max_drawdown_pct': max_drawdown * 100,
        'peak_value': prices[peak_idx],
        'trough_value': prices[max_drawdown_idx],
        'peak_date': peak_idx,
        'trough_date': max_drawdown_idx
    }


def calculate_cumulative_returns(returns: pd.Series) -> pd.Series:

    return (1 + returns).cumprod() - 1


def calculate_moving_average(
    series: pd.Series,
    window: int
) -> pd.Series:
    return series.rolling(window=window).mean()


def detect_trends(series: pd.Series) -> Dict[str, float]:
    x = np.arange(len(series))
    y = series.values

    # Remove NaN values
    mask = ~np.isnan(y)
    x = x[mask]
    y = y[mask]

    if len(x) < 2:
        return {
            'slope': 0,
            'intercept': 0,
            'r_squared': 0,
            'p_value': 1,
            'trend': 'insufficient_data'
        }

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    if slope > 0:
        trend = "increasing"
    elif slope < 0:
        trend = "decreasing"
    else:
        trend = "stable"

    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_value**2,
        'p_value': p_value,
        'trend': trend
    }


def calculate_beta(
    stock_returns: pd.Series,
    market_returns: pd.Series
) -> float:

    covariance = stock_returns.cov(market_returns)
    market_variance = market_returns.var()

    if market_variance == 0:
        return 0.0

    beta = covariance / market_variance
    return beta

