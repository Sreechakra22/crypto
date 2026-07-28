import pandas as pd
import matplotlib.pyplot as plt
import threading
import smtplib
from email.message import EmailMessage

print("\nMilestone 3 - Risk Analysis Based on Customer Investments")
print("----------------------------------------------------------")

# Load investments from Milestone 2
investments = pd.read_csv(
    "data/processed/customer_investments.csv",
    names=["Cryptocurrency", "Investment Amount", "Risk Preference"],
    header=None
)

# Load crypto dataset
crypto_data = pd.read_csv("data/processed/cleaned_crypto_data.csv")

risk_results = {}
trend_results = {}

# --------------------------------
# Email Alert Function
# --------------------------------
def send_email_alert(coin, volatility):

    sender_email = "sreechakrakommera@gmail.com"
    receiver_email = "23r01a05dz@cmrithyderabad.edu.in"
    app_password = "pkwh qcqg tkae ftny"

    msg = EmailMessage()
    msg["Subject"] = f"Crypto Risk Alert: {coin}"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(
        f"""
High Risk Cryptocurrency Detected!

Coin: {coin}
Volatility: {volatility}

This asset is currently classified as HIGH RISK.
Please review your investment.

Crypto Investment Manager
"""
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        print(f"Email alert sent for {coin}")

    except Exception as e:
        print("Email sending failed:", e)

# --------------------------------
# Risk Checker
# --------------------------------
def risk_checker():

    volatility = crypto_data.groupby("cryptocurrency")["price"].std()

    for coin in investments["Cryptocurrency"]:

        if coin not in volatility:
            continue

        value = volatility[coin]

        if value > 1000:
            level = "High Risk"
            send_email_alert(coin, round(value,2))
        elif value > 100:
            level = "Moderate Risk"
        else:
            level = "Low Risk"

        risk_results[coin] = value

    print("Risk analysis completed.")

# --------------------------------
# Trend Prediction
# --------------------------------
def trend_prediction():

    avg_price = crypto_data.groupby("cryptocurrency")["price"].mean()
    latest_price = crypto_data.groupby("cryptocurrency")["price"].last()

    for coin in investments["Cryptocurrency"]:

        if coin not in avg_price:
            continue

        if latest_price[coin] > avg_price[coin]:
            trend_results[coin] = "Uptrend Expected"
        else:
            trend_results[coin] = "Stable / Downtrend"

    print("Trend prediction completed.")

# --------------------------------
# Run Tasks in Parallel
# --------------------------------
t1 = threading.Thread(target=risk_checker)
t2 = threading.Thread(target=trend_prediction)

t1.start()
t2.start()

t1.join()
t2.join()

# --------------------------------
# Report
# --------------------------------
print("\nCustomer Investment Risk Report")
print("--------------------------------")

for coin in risk_results:

    print(f"{coin}")
    print(f"Volatility: {round(risk_results[coin],2)}")
    print(f"Predicted Trend: {trend_results.get(coin,'Unknown')}")
    print()

# --------------------------------
# Graph
# --------------------------------
coins = list(risk_results.keys())
values = list(risk_results.values())

plt.bar(coins, values)

plt.title("Risk Level of Customer Investments")
plt.xlabel("Cryptocurrency")
plt.ylabel("Volatility")

plt.show()