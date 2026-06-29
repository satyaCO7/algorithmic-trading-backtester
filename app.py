import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backtest_engine import fetch_historical_data, generate_signals, run_backtest, calculate_performance_metrics

st.set_page_config(page_title="Algorithmic Backtester Engine", layout="wide")

st.title("🖲️ Quantitative Algorithmic Trading & Backtesting Engine")
st.markdown("An institutional-grade local simulation workspace that models historical execution sequences under transaction fee and slippage friction.")

# --- SIDEBAR CONFIGURATIONS ---
st.sidebar.header("Strategy Configuration")
ticker = st.sidebar.text_input("Equity Ticker symbol", value="AAPL").upper()
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2026-01-01"))

st.sidebar.subheader("Moving Average Windows")
fast_window = st.sidebar.slider("Fast MA Window (Days)", min_value=5, max_value=50, value=20)
slow_window = st.sidebar.slider("Slow MA Window (Days)", min_value=20, max_value=200, value=50)

st.sidebar.subheader("Execution Parameters")
initial_capital = st.sidebar.number_input("Starting Balance ($)", value=100000.0)
fees = st.sidebar.slider("Brokerage Commission (%)", min_value=0.0, max_value=0.5, value=0.1, step=0.05) / 100
slippage = st.sidebar.slider("Market Slippage Friction (%)", min_value=0.0, max_value=0.5, value=0.05, step=0.01) / 100

# --- DATA PIPELINE RUNNER ---
if st.sidebar.button("Execute Historical Run"):
    raw_data = fetch_historical_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    
    if not raw_data.empty:
        signals_df = generate_signals(raw_data, fast_window, slow_window)
        results_df, trades = run_backtest(signals_df, initial_capital, fees, slippage)
        roi, sharpe, max_dd = calculate_performance_metrics(results_df, initial_capital)
        
        # --- METRIC DISPLAY PANELS ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Strategy ROI", f"{roi:.2f}%")
        col2.metric("Annualized Sharpe Ratio", f"{sharpe:.2f}")
        col3.metric("Maximum Drawdown", f"{max_dd:.2f}%")
        
        # --- GRAPHICAL PLOTTING ENGINE ---
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        # Plot 1: Underlying Stock Price & Moving Average Crossings
        ax1.plot(results_df.index, results_df['Close'], label=f'{ticker} Price', color='gray', alpha=0.6)
        ax1.plot(results_df.index, results_df['Fast_MA'], label=f'Fast MA ({fast_window}d)', color='blue', linestyle='--')
        ax1.plot(results_df.index, results_df['Slow_MA'], label=f'Slow MA ({slow_window}d)', color='orange', linestyle='--')
        ax1.set_title("Historical Asset Price & Strategy Indicators")
        ax1.set_ylabel("Asset Price ($)")
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Portfolio Equity Growth Curve
        ax2.plot(results_df.index, results_df['Portfolio_Value'], label='Portfolio Total Value', color='green', linewidth=2)
        ax2.set_title("Portfolio Equity Growth Curve")
        ax2.set_ylabel("Portfolio Capital ($)")
        ax2.set_xlabel("Timeline")
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        # --- RECENT TRADE LEDGER LOG ---
        if trades:
            st.subheader("📋 Execution Log (Chronological Fills)")
            trades_df = pd.DataFrame(trades)
            trades_df['Date'] = trades_df['Date'].dt.strftime('%Y-%m-%d')
            st.dataframe(trades_df.tail(10), use_container_width=True)
    else:
        st.error("No data found for the given parameters. Please check the ticker name or date bounds.")