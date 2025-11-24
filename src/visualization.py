import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, List


def set_plot_style(style: str = "whitegrid"):
    sns.set_style(style)
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 11


def plot_stock_prices(
    df: pd.DataFrame,
    date_col: str = 'Date',
    price_col: str = 'Close',
    ticker_col: str = 'Ticker',
    title: str = "Stock Prices Over Time"
) -> plt.Figure:

    fig, ax = plt.subplots(figsize=(14, 7))
    
    for ticker in df[ticker_col].unique():
        ticker_data = df[df[ticker_col] == ticker]
        ax.plot(ticker_data[date_col], ticker_data[price_col], 
                label=ticker, linewidth=2, marker='o', markersize=2)
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price ($)', fontsize=12)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_returns_distribution(
    returns: pd.Series,
    title: str = "Returns Distribution",
    bins: int = 50
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.histplot(returns.dropna(), bins=bins, kde=True, ax=ax, color='steelblue')
    
    mean_return = returns.mean()
    ax.axvline(mean_return, color='red', linestyle='--', linewidth=2, 
               label=f'Mean: {mean_return:.4f}')
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Returns', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_correlation_heatmap(
    corr_matrix: pd.DataFrame,
    title: str = "Stock Returns Correlation Matrix",
    cmap: str = "coolwarm",
    annot: bool = True
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(corr_matrix, annot=annot, cmap=cmap, center=0, 
                square=True, linewidths=1, ax=ax, fmt='.3f',
                cbar_kws={'label': 'Correlation Coefficient'})
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    return fig


def plot_volatility(
    df: pd.DataFrame,
    date_col: str = 'Date',
    volatility_col: str = 'Volatility',
    ticker_col: Optional[str] = None,
    title: str = "Rolling Volatility"
) -> plt.Figure:

    fig, ax = plt.subplots(figsize=(14, 7))
    
    if ticker_col:
        for ticker in df[ticker_col].unique():
            ticker_data = df[df[ticker_col] == ticker]
            ax.plot(ticker_data[date_col], ticker_data[volatility_col], 
                    label=ticker, linewidth=2)
    else:
        ax.plot(df[date_col], df[volatility_col], linewidth=2, color='darkred')
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Volatility (Annualized)', fontsize=12)
    if ticker_col:
        ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_risk_return_scatter(
    risk: pd.Series,
    returns: pd.Series,
    labels: Optional[List[str]] = None,
    title: str = "Risk-Return Profile"
) -> plt.Figure:

    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.scatter(risk, returns, s=200, alpha=0.6, c='steelblue', edgecolors='black')
    
    if labels:
        for i, label in enumerate(labels):
            ax.annotate(label, (risk.iloc[i], returns.iloc[i]), 
                       fontsize=12, fontweight='bold',
                       xytext=(5, 5), textcoords='offset points')
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Risk (Volatility)', fontsize=12)
    ax.set_ylabel('Average Return', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
    
    plt.tight_layout()
    return fig


def plot_cumulative_returns(
    df: pd.DataFrame,
    date_col: str = 'Date',
    returns_col: str = 'Cumulative_Returns',
    ticker_col: str = 'Ticker',
    title: str = "Cumulative Returns"
) -> plt.Figure:

    fig, ax = plt.subplots(figsize=(14, 7))
    
    for ticker in df[ticker_col].unique():
        ticker_data = df[df[ticker_col] == ticker]
        ax.plot(ticker_data[date_col], ticker_data[returns_col] * 100, 
                label=ticker, linewidth=2)
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Cumulative Returns (%)', fontsize=12)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def create_interactive_price_chart(
    df: pd.DataFrame,
    date_col: str = 'Date',
    price_col: str = 'Close',
    ticker_col: str = 'Ticker',
    title: str = "Interactive Stock Prices"
) -> go.Figure:

    fig = px.line(df, x=date_col, y=price_col, color=ticker_col,
                  title=title, labels={price_col: 'Price ($)', date_col: 'Date'})
    
    fig.update_layout(
        hovermode='x unified',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        legend_title='Ticker',
        font=dict(size=12),
        height=600
    )
    
    return fig

