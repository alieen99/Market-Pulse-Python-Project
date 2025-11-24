import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime, timedelta
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.visualization import set_plot_style

st.set_page_config(
    page_title="Market Pulse Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

set_plot_style()

st.title("📈 Market Pulse: Stock Market Analysis Dashboard")
st.markdown("""
**Interactive dashboard for exploring stock market sector dynamics**

Analyze technology and financial sector stocks with real-time data, volatility metrics, 
and correlation patterns.
""")
st.markdown("---")

st.sidebar.header("⚙️ Configuration")

st.sidebar.subheader("Select Stocks")
tech_stocks_default = ['AAPL', 'MSFT', 'GOOGL']
finance_stocks_default = ['JPM', 'BAC', 'GS']

tech_stocks = st.sidebar.multiselect(
    "Technology Sector",
    ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA'],
    default=tech_stocks_default
)

finance_stocks = st.sidebar.multiselect(
    "Financial Sector",
    ['JPM', 'BAC', 'GS', 'WFC', 'C', 'MS'],
    default=finance_stocks_default
)

all_tickers = tech_stocks + finance_stocks

st.sidebar.subheader("Date Range")
end_date = datetime.now()
start_date = end_date - timedelta(days=4*365)

start_date_input = st.sidebar.date_input("Start Date", start_date)
end_date_input = st.sidebar.date_input("End Date", end_date)

st.sidebar.subheader("Analysis Parameters")
volatility_window = st.sidebar.slider("Volatility Window (days)", 10, 90, 30)

if st.sidebar.button("🔄 Fetch Data", type="primary"):
    st.session_state['fetch_data'] = True

if 'fetch_data' not in st.session_state:
    st.session_state['fetch_data'] = False

if not st.session_state['fetch_data']:
    st.info("👈 Configure your analysis parameters in the sidebar and click 'Fetch Data' to begin.")
    
    st.subheader("📊 What You'll Get")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Stock Analysis", "6+ stocks", "Real-time data")
    with col2:
        st.metric("Time Period", "4 years", "Daily data")
    with col3:
        st.metric("Visualizations", "5+ charts", "Interactive")
    
    st.markdown("---")
    st.subheader("🎯 Features")
    st.markdown("""
    - **Price Trends**: Historical price movements
    - **Return Analysis**: Daily and annualized returns
    - **Volatility Tracking**: Rolling volatility metrics
    - **Correlation Matrix**: Inter-stock relationships
    - **Risk-Return Profile**: Comprehensive performance view
    """)

else:
    with st.spinner(f"Fetching data for {len(all_tickers)} stocks..."):
        try:
            prices_list = []
            for ticker in all_tickers:
                stock = yf.download(ticker, start=start_date_input, end=end_date_input, progress=False, auto_adjust=True)
                if not stock.empty:
                    if isinstance(stock.columns, pd.MultiIndex):
                        close_price = stock['Close'][ticker] if ticker in stock['Close'].columns else stock['Close'].iloc[:, 0]
                    else:
                        close_price = stock['Close'] if 'Close' in stock.columns else stock.iloc[:, 0]
                    
                    prices_list.append(pd.Series(close_price.values, index=close_price.index, name=ticker))
            
            if not prices_list:
                st.error("No data fetched. Please check your stock selections and date range.")
                st.stop()
            
            prices_df = pd.concat(prices_list, axis=1)
            
            if prices_df.empty:
                st.error("No data fetched. Please check your stock selections and date range.")
                st.stop()
            
            prices_df = prices_df.ffill().bfill()
            returns_df = prices_df.pct_change().dropna()
            
            st.success(f"✓ Data fetched successfully! {len(prices_df)} trading days")
            
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.stop()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Price Trends", 
        "📊 Returns Analysis", 
        "📉 Volatility", 
        "🔗 Correlations",
        "🎯 Risk-Return"
    ])
    
    with tab1:
        st.subheader("Stock Price Trends")
        
        normalized_prices = (prices_df / prices_df.iloc[0]) * 100
        
        fig, ax = plt.subplots(figsize=(14, 6))
        for ticker in all_tickers:
            ax.plot(normalized_prices.index, normalized_prices[ticker], label=ticker, linewidth=2)
        
        ax.set_title('Normalized Stock Prices (Base = 100)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Normalized Price')
        ax.legend(loc='best', ncol=2)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Best Performer", 
                     normalized_prices.iloc[-1].idxmax(),
                     f"+{normalized_prices.iloc[-1].max()-100:.1f}%")
        with col2:
            st.metric("Worst Performer",
                     normalized_prices.iloc[-1].idxmin(),
                     f"{normalized_prices.iloc[-1].min()-100:.1f}%")
    
    with tab2:
        st.subheader("Returns Analysis")
        
        annualized_returns = returns_df.mean() * 252
        annualized_volatility = returns_df.std() * np.sqrt(252)
        sharpe_ratio = annualized_returns / annualized_volatility
        
        metrics_df = pd.DataFrame({
            'Annual Return (%)': annualized_returns * 100,
            'Annual Volatility (%)': annualized_volatility * 100,
            'Sharpe Ratio': sharpe_ratio
        }).sort_values('Sharpe Ratio', ascending=False)
        
        st.dataframe(metrics_df.style.format({
            'Annual Return (%)': '{:.2f}',
            'Annual Volatility (%)': '{:.2f}',
            'Sharpe Ratio': '{:.3f}'
        }).background_gradient(cmap='RdYlGn', subset=['Sharpe Ratio']))
        
        st.subheader("Return Distributions")
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        axes = axes.flatten()
        
        for idx, ticker in enumerate(all_tickers[:6]):
            axes[idx].hist(returns_df[ticker], bins=50, alpha=0.7, edgecolor='black')
            axes[idx].set_title(f'{ticker}', fontweight='bold')
            axes[idx].set_xlabel('Daily Return')
            axes[idx].set_ylabel('Frequency')
            axes[idx].grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with tab3:
        st.subheader(f"{volatility_window}-Day Rolling Volatility")
        
        rolling_vol = returns_df.rolling(window=volatility_window).std() * np.sqrt(252)
        
        fig, ax = plt.subplots(figsize=(14, 6))
        for ticker in all_tickers:
            ax.plot(rolling_vol.index, rolling_vol[ticker], label=ticker, linewidth=2)
        
        ax.set_title(f'{volatility_window}-Day Rolling Volatility (Annualized)', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Volatility')
        ax.legend(loc='best', ncol=2)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        st.subheader("Current Volatility Levels")
        current_vol = rolling_vol.iloc[-1].sort_values(ascending=False)
        
        col1, col2, col3 = st.columns(3)
        for idx, (ticker, vol) in enumerate(current_vol.items()):
            if idx % 3 == 0:
                col1.metric(ticker, f"{vol:.2%}")
            elif idx % 3 == 1:
                col2.metric(ticker, f"{vol:.2%}")
            else:
                col3.metric(ticker, f"{vol:.2%}")
    
    with tab4:
        st.subheader("Correlation Matrix")
        
        corr_matrix = returns_df.corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', 
                   center=0, square=True, linewidths=1, ax=ax,
                   cbar_kws={"shrink": 0.8})
        ax.set_title('Stock Returns Correlation Matrix', fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        
        st.subheader("Correlation Insights")
        
        corr_values = corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Correlation", f"{corr_values.mean():.3f}")
        with col2:
            st.metric("Max Correlation", f"{corr_values.max():.3f}")
    
    with tab5:
        st.subheader("Risk-Return Profile")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colors = {'Tech': '#2E86AB', 'Finance': '#A23B72'}
        sector_map = {ticker: 'Tech' if ticker in tech_stocks else 'Finance' 
                     for ticker in all_tickers}
        
        for ticker in all_tickers:
            color = colors[sector_map[ticker]]
            ax.scatter(annualized_volatility[ticker], annualized_returns[ticker],
                      s=200, alpha=0.6, color=color, edgecolors='black', linewidth=2)
            ax.annotate(ticker, (annualized_volatility[ticker], annualized_returns[ticker]),
                       xytext=(8, 8), textcoords='offset points', 
                       fontsize=10, fontweight='bold')
        
        ax.axhline(y=annualized_returns.mean(), color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=annualized_volatility.mean(), color='gray', linestyle='--', alpha=0.5)
        
        ax.set_xlabel('Annualized Volatility (Risk)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Annualized Return', fontsize=12, fontweight='bold')
        ax.set_title('Risk-Return Profile', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=colors['Tech'], label='Technology'),
                          Patch(facecolor=colors['Finance'], label='Financial')]
        ax.legend(handles=legend_elements, loc='best')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.subheader("Top Performers (by Sharpe Ratio)")
        top_stocks = metrics_df.head(3)
        
        for idx, (ticker, row) in enumerate(top_stocks.iterrows()):
            st.metric(
                f"#{idx+1}: {ticker}",
                f"{row['Annual Return (%)']:.2f}%",
                f"Sharpe: {row['Sharpe Ratio']:.3f}"
            )

st.markdown("---")
st.markdown("""
**Market Pulse Dashboard** | Coding for Data Science and Data Management  
Università degli Studi di Milano | Mohammad Ali Noroozshad | 2025/2026

*Data source: Yahoo Finance via yfinance library*
""")

