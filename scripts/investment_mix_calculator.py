import pandas as pd
import matplotlib.pyplot as plt
import os

# Load Data
DATA_PATH = "data/processed/cleaned_crypto_data.csv"
df = pd.read_csv(DATA_PATH)

print("\nWelcome to Crypto Investment Manager")
print("-------------------------------------")

# Risk Checker
def get_risk_level(coin_name):

    volatility = df.groupby("cryptocurrency")["price"].std()
    value = volatility[coin_name]

    if value > 1000:
        return "High Risk"
    elif value > 100:
        return "Moderate Risk"
    else:
        return "Low Risk"

# Profit Checker
def check_profit(coin_name):

    avg_price = df.groupby("cryptocurrency")["price"].mean()
    latest_price = df.groupby("cryptocurrency")["price"].last()

    growth = ((latest_price[coin_name] - avg_price[coin_name]) / avg_price[coin_name]) * 100
    return round(growth, 2)


# LOOP
while True:

    investment_amount = float(input("\nEnter Investment Amount (INR): "))
    risk_preference = input("Enter Risk Level (low / medium / high): ").lower()
    coin_choice = input("Enter Cryptocurrency (Bitcoin / Ethereum / Tether): ").capitalize()
    investment_percent = float(input("Enter % you want to invest in this coin: "))

    if coin_choice not in df["cryptocurrency"].unique():
        print("Invalid Cryptocurrency Entered!")
        continue

    investment_value = (investment_percent / 100) * investment_amount

    print("\nInvestment Summary")
    print("-------------------")
    print(f"Selected Coin: {coin_choice}")
    print(f"Risk Preference: {risk_preference.upper()}")
    print(f"Your Investment %: {investment_percent}%")
    print(f"Amount Invested: ₹{investment_value:,.2f}")

    # Risk Check
    risk_level = get_risk_level(coin_choice)
    print(f"Actual Risk Level of {coin_choice}: {risk_level}")

    # Profit Check
    growth = check_profit(coin_choice)

    if growth > 0:
        print(f"{coin_choice} shows positive growth of {growth}%")
    else:
        print(f"{coin_choice} shows negative/stable growth of {growth}%")

    # Graph
    plt.figure()
    plt.bar([coin_choice], [investment_value])
    plt.title("Manual Investment Allocation")
    plt.xlabel("Cryptocurrency")
    plt.ylabel("Investment Amount (₹)")
    plt.show()

    # Save investment result
    investment_record = pd.DataFrame({
        "Cryptocurrency": [coin_choice],
        "Investment Amount": [investment_value],
        "Risk Preference": [risk_preference]
    })

    file_path = "data/processed/customer_investments.csv"

    investment_record.to_csv(
        file_path,
        mode="a",
        index=False,
        header=not os.path.exists(file_path)
    )

    again = input("\nDo you want to make another investment? (yes/no): ").lower()

    if again != "yes":
        print("\nThank you for using Crypto Investment Manager!")
        break