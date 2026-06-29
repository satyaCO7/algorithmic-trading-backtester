# Quantitative Algorithmic Trading & Backtesting Engine

An institutional-grade local simulation workspace designed to execute, backtest, and evaluate quantitative trading strategies against real-world historical market data. 

This engine bypasses high-level black-box backtesting libraries to build transaction processing, portfolio balancing, and asset accounting completely from the ground up, modeling structural market friction including brokerage commissions and order execution slippage.

## 🧠 Core Quantitative Features

* **Moving Average Crossover Logic:** Implemented dynamic rolling trend-following mathematics utilizing multi-period momentum indicators ($MA_{\text{Fast}}$ vs $MA_{\text{Slow}}$) to calculate deterministic trade triggers.
* **Friction-Adjusted Execution Ledger:** Programmed a chronological portfolio accounting simulator that tracks cash balances and share holdings day-by-day, applying penalty parameters for fixed broker commission percentages and market slippage costs.
* **Risk-Adjusted Performance Reporting:** Formulated an analytical reporting engine to extract institutional risk profiles:
    * **Total Return (ROI):** Absolute percentage equity appreciation over the timeline.
    * **Sharpe Ratio:** Annualized excess return per unit of total risk relative to a baseline risk-free rate ($R_f = 4\%$).
    * **Maximum Drawdown:** Absolute peak-to-trough calculation mapping maximum historical downside equity pain.

---

## 📈 Underlying Mathematical Specifications

The annualized Sharpe Ratio isolates strategy efficiency by dividing annualized excess daily returns by the annualized portfolio standard deviation:

$$\text{Sharpe Ratio} = \frac{\mu_{\text{daily}} - \frac{R_f}{252}}{\sigma_{\text{daily}}} \times \sqrt{252}$$

Where tracking metrics are captured across historical trading days ($N=252$). Maximum Drawdown monitors maximum peak preservation drops along the continuous capital timeline:

$$\text{Drawdown}_t = \frac{\text{Portfolio Value}_t - \max_{\tau \le t}(\text{Portfolio Value}_\tau)}{\max_{\tau \le t}(\text{Portfolio Value}_\tau)}$$

$$\text{Maximum Drawdown} = \min_{t} \left(\text{Drawdown}_t\right)$$

---

## 🚀 Local Installation & Execution

### 1. Clone the Project Workspace
```bash
git clone [https://github.com/satyaCO7/algorithmic-trading-backtester.git](https://github.com/satyaCO7/algorithmic-trading-backtester.git)
cd algorithmic-trading-backtester