import sys
from pathlib import Path

src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

from data_loader import fetch_stock_data, save_dataframe
from data_processing import calculate_returns, pivot_stock_data
from analysis import calculate_correlation, calculate_volatility, calculate_descriptive_stats
from visualization import (
    plot_stock_prices, 
    plot_correlation_heatmap, 
    plot_volatility,
    plot_risk_return_scatter,
    set_plot_style
)
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def main():
    print("Market Pulse: Stock Market Analysis")
    print("=" * 50)
    
    # Define stocks to analyze
    tech_stocks = ['AAPL', 'MSFT', 'GOOGL']
    financial_stocks = ['JPM', 'BAC', 'GS']
    all_stocks = tech_stocks + financial_stocks
    
    # Fetch data
    print("\n1. Fetching stock data...")
    end_date = datetime.now().strftime('%Y-%m-%d')
    stock_data = fetch_stock_data(
        tickers=all_stocks,
        start_date='2020-01-01',
        end_date=end_date
    )
    
    # Save raw data
    save_dataframe(stock_data, 'data/raw/stock_prices.csv')
    
    # Calculate returns
    print("\n2. Calculating returns...")
    stock_data = calculate_returns(stock_data)
    
    # Pivot data for correlation analysis
    print("\n3. Analyzing correlations...")
    returns_pivot = pivot_stock_data(stock_data, values_col='Returns')
    correlation_matrix = calculate_correlation(returns_pivot)
    
    # Calculate statistics
    print("\n4. Calculating statistics...")
    stats = calculate_descriptive_stats(returns_pivot)
    print("\nDescriptive Statistics:")
    print(stats)
    
    # Save processed data
    save_dataframe(returns_pivot, 'data/processed/daily_returns.csv')
    
    # Visualizations
    print("\n5. Creating visualizations...")
    set_plot_style()
    
    # Plot stock prices
    fig1 = plot_stock_prices(stock_data)
    plt.savefig('data/processed/stock_prices.png', dpi=300, bbox_inches='tight')
    
    # Plot correlation heatmap
    fig2 = plot_correlation_heatmap(correlation_matrix)
    plt.savefig('data/processed/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    
    # Calculate risk-return profile
    avg_returns = returns_pivot.mean()
    volatility = returns_pivot.std() * (252 ** 0.5)  # Annualized
    
    fig3 = plot_risk_return_scatter(volatility, avg_returns, labels=all_stocks)
    plt.savefig('data/processed/risk_return.png', dpi=300, bbox_inches='tight')
    
    print("\n✓ Analysis complete!")
    print("✓ Results saved to data/processed/")
    print("\nTo view visualizations, check the data/processed/ folder")


if __name__ == "__main__":
    main()
