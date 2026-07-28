import pandas as pd
files = {
    "btc-usd-max.csv": "Bitcoin",
    "eth-usd-max.csv": "Ethereum",
    "usdt-usd-max.csv": "Tether"
}
all_data = []
for file, coin_name in files.items():
    df = pd.read_csv(f"data/raw/{file}")
    # Rename columns
    df = df.rename(columns={"snapped_at": "date"})
    # Convert date
    df["date"] = pd.to_datetime(df["date"])
    # Sort and take last 200 days
    df = df.sort_values("date").tail(200)
    # Add cryptocurrency name
    df["cryptocurrency"] = coin_name
    # Keep only existing useful columns
    df = df[[
        "cryptocurrency",
        "date",
        "price",
        "market_cap",
        "total_volume"
    ]]
    # Remove missing values
    df = df.dropna()
    all_data.append(df)
# Merge all three cryptocurrencies
final_df = pd.concat(all_data, ignore_index=True)
# Save processed data
final_df.to_csv(
    "data/processed/cleaned_crypto_data.csv",
    index=False
)
print(" data preparation completed successfully")
