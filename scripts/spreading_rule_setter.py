import pandas as pd
import matplotlib.pyplot as plt

print("\nMilestone 4 - Spreading Rule Setter & Portfolio Optimization")
print("-------------------------------------------------------------")

# -----------------------------------------
# Load Customer Investments (Milestone 2)
# -----------------------------------------
investments = pd.read_csv(
    "data/processed/customer_investments.csv",
    names=["Cryptocurrency", "Investment Amount", "Risk Preference"],
    header=None
)

# -----------------------------------------
# Load Crypto Market Data
# -----------------------------------------
crypto_data = pd.read_csv("data/processed/cleaned_crypto_data.csv")

# -----------------------------------------
# Calculate Volatility (Risk)
# -----------------------------------------
volatility = crypto_data.groupby("cryptocurrency")["price"].std()

# -----------------------------------------
# Portfolio Spreading Rules
# -----------------------------------------
optimized_portfolio = {}

for index, row in investments.iterrows():

    coin = row["Cryptocurrency"]
    amount = row["Investment Amount"]

    if coin not in volatility:
        continue

    risk = volatility[coin]

    # Spreading rules
    if risk > 1000:
        recommendation = "Reduce Investment (High Risk)"
        new_amount = amount * 0.5
    elif risk > 100:
        recommendation = "Balanced Investment"
        new_amount = amount * 0.8
    else:
        recommendation = "Safe Investment"
        new_amount = amount

    optimized_portfolio[coin] = {
        "Original Investment": amount,
        "Adjusted Investment": round(new_amount,2),
        "Volatility": round(risk,2),
        "Recommendation": recommendation
    }

# -----------------------------------------
# Display Portfolio Recommendation
# -----------------------------------------
print("\nFinal Portfolio Recommendation")
print("--------------------------------")

for coin, data in optimized_portfolio.items():

    print(f"{coin}")
    print(f"Original Investment: ₹{data['Original Investment']}")
    print(f"Adjusted Investment: ₹{data['Adjusted Investment']}")
    print(f"Volatility: {data['Volatility']}")
    print(f"Recommendation: {data['Recommendation']}")
    print()

# -----------------------------------------
# Save Final Portfolio Report
# -----------------------------------------
report = pd.DataFrame.from_dict(optimized_portfolio, orient="index")

report.to_csv("data/processed/final_portfolio_report.csv")

print("Final portfolio report saved as final_portfolio_report.csv")

# -----------------------------------------
# Graph - Optimized Portfolio
# -----------------------------------------
coins = list(optimized_portfolio.keys())
values = [data["Adjusted Investment"] for data in optimized_portfolio.values()]

plt.bar(coins, values)

plt.title("Optimized Crypto Portfolio Allocation")
plt.xlabel("Cryptocurrency")
plt.ylabel("Investment Amount (₹)")

plt.show()