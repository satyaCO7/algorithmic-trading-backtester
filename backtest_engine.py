import yfinance as yf
import numpy as np
import pandas as pd

def fetch_historical_data(ticker, start_date, end_date):
    """Ingests real historical market data using yfinance."""
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def generate_signals(data, fast_window=20, slow_window=50):
    """Calculates moving averages and maps algorithmic buy/sell triggers."""
    if data.empty:
        return pd.DataFrame()
    df = data.copy()
    df['Fast_MA'] = df['Close'].rolling(window=fast_window).mean()
    df['Slow_MA'] = df['Close'].rolling(window=slow_window).mean()
    
    df['State'] = np.where(df['Fast_MA'] > df['Slow_MA'], 1, 0)
    df['Signal'] = df['State'].diff()
    
    df = df.dropna(subset=['Fast_MA', 'Slow_MA']).copy()
    return df

def run_backtest(df, initial_capital=100000.0, transaction_fee_rate=0.001, slippage_rate=0.0005):
    """Simulates chronological trade execution over historical time series."""
    if df.empty:
        return df
        
    cash = initial_capital
    position = 0.0  
    portfolio_values = []
    trade_log = []
    
    for date, row in df.iterrows():
        current_price = float(row['Close'])
        signal = row['Signal']
        
        if signal == 1.0 and cash > 0:
            execution_price = current_price * (1 + slippage_rate)
            available_cash = cash / (1 + transaction_fee_rate)
            position = available_cash / execution_price
            cash = 0.0
            trade_log.append({"Type": "BUY", "Date": date, "Price": execution_price})
            
        elif signal == -1.0 and position > 0:
            execution_price = current_price * (1 - slippage_rate)
            gross_proceeds = position * execution_price
            fee = gross_proceeds * transaction_fee_rate
            cash = gross_proceeds - fee
            trade_log.append({"Type": "SELL", "Date": date, "Price": execution_price})
            position = 0.0
            
        current_portfolio_value = cash + (position * current_price)
        portfolio_values.append(current_portfolio_value)
        
    df['Portfolio_Value'] = portfolio_values
    return df, trade_log

def calculate_performance_metrics(df, initial_capital=100000.0, risk_free_rate=0.04):
    """Calculates Sharpe Ratio, Maximum Drawdown, and Total ROI percentage."""
    if df.empty or 'Portfolio_Value' not in df.columns:
        return 0.0, 0.0, 0.0
        
    final_value = df['Portfolio_Value'].iloc[-1]
    total_roi = ((final_value - initial_capital) / initial_capital) * 100
    
    df['Daily_Return'] = df['Portfolio_Value'].pct_change()
    mean_daily_return = df['Daily_Return'].mean()
    std_daily_return = df['Daily_Return'].std()
    
    if std_daily_return > 0:
        daily_risk_free = risk_free_rate / 252
        sharpe_ratio = ((mean_daily_return - daily_risk_free) / std_daily_return) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0
        
    rolling_peak = df['Portfolio_Value'].cummax()
    drawdowns = (df['Portfolio_Value'] - rolling_peak) / rolling_peak
    max_drawdown = drawdowns.min() * 100
    
    return total_roi, sharpe_ratio, max_drawdown