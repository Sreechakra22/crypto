import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("data/processed/cleaned_crypto_data.csv")

# BASIC ED 
print("First 5 rows:")
print(df.head())

print("\nDataset structure:")
print(df.info())

print("\nStatistical summary:")
print(df.describe())

#  ED INSIGHTS 
print("\nAverage price per cryptocurrency:")
print(df.groupby("cryptocurrency")["price"].mean())

print("\nPrice volatility (standard deviation):")
print(df.groupby("cryptocurrency")["price"].std())

#  SAVE ED SUMMARY 
summary = df.groupby("cryptocurrency").agg({
    "price": ["mean", "max", "min", "std"],
    "total_volume": "mean"
})
summary.to_csv("data/processed/ed_summary.csv")

#  PRICE TREND 
plt.figure()
for coin in df["cryptocurrency"].unique():
    coin_data = df[df["cryptocurrency"] == coin]
    plt.plot(coin_data["date"], coin_data["price"], label=coin)

plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.title("Cryptocurrency Price Trend (Bitcoin, Ethereum, Tether)")
plt.legend()
plt.show()

print("Exploratory Data analysis with single diagram completed successfully")
