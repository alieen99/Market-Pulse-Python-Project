# Market Pulse: Stock Market Sector Analysis

A comprehensive analysis of stock market sectors, exploring volatility, correlations, and performance trends using Python data science tools.

**Course:** Coding for Data Science and Data Management
**Institution:** Professor Stefano Montanelli
**Author:** Mohammad Ali Noroozshad
**Academic Year:** 2025/2026

## 📊 Project Overview

This project analyzes the behavior of different stock market sectors by fetching and processing historical stock price data. The analysis uncovers performance trends, risk profiles, and correlations between major technology and financial sector stocks.

### Key Features

- **Real-time Data Fetching**: Automatically fetch historical stock data using Yahoo Finance API
- **Comprehensive Analysis**: Calculate returns, volatility, correlations, and risk metrics
- **Interactive Visualizations**: Create insightful charts including heatmaps, time series, and risk-return plots
- **Web Dashboard**: Interactive Streamlit application for exploring market dynamics
- **Statistical Computing**: Advanced numerical computations using NumPy and SciPy

## 🎯 Research Questions

1. How do technology and financial sector stocks correlate with each other?
2. Which stocks exhibit the highest volatility and risk?
3. What is the risk-return profile of different stocks?
4. How do stock prices and returns evolve over time?

## 🚀 Getting Started

### Prerequisites

- **Python 3.12** (Recommended)
- pip package manager
- Internet connection (for fetching stock data)

> ⚠️ **Important Note**: This project requires `pyarrow` which currently has compatibility issues with Python 3.14. Please use **Python 3.12** for the best experience.

### Installation

1. **Clone the repository**

```bash
gh repo clone alieen99/Market-Pulse-Python-Project
cd Market-Pulse-Python-Project
```

2. **Create virtual environment with Python 3.12**

```bash
# Make sure you're using Python 3.12
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install PyArrow first (required for Streamlit)**

```bash
pip install pyarrow
```

4. **Install remaining dependencies**

```bash
pip install -r requirements.txt
```

> **Troubleshooting**: If you encounter issues with `pyarrow` on Python 3.14, please downgrade to Python 3.12. The `pyarrow` library is required by Streamlit and currently doesn't support Python 3.14.

### Running the Project

#### Option 1: Jupyter Notebook (Recommended)

```bash
jupyter notebook
```

#### Option 2: Streamlit Dashboard

```bash
streamlit run app/streamlit_app.py
```

#### Option 3: Command Line

```bash
python main.py
```

## 📊 Data Sources

- **Yahoo Finance API** via `yfinance` library
- **Stocks Analyzed**:

  - Technology Sector: AAPL (Apple), MSFT (Microsoft), GOOGL (Google)
  - Financial Sector: JPM (JPMorgan), BAC (Bank of America), GS (Goldman Sachs)

- **Data Frequency**: Daily closing prices
