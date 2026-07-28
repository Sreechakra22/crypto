import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="Crypto Portfolio Manager", layout="wide")

# ---------------- CUSTOM THEME ----------------
st.markdown("""
<style>
body {background-color:#0E1117;}
h1,h2,h3 {color:#00FFD1;}
.stMetric {background-color:#1f2937;padding:15px;border-radius:10px;}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
crypto_data = pd.read_csv("data/processed/cleaned_crypto_data.csv")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Crypto Portfolio Manager")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Investment Planner",
        "Risk Analyzer",
        "Price Prediction",
        "Portfolio Growth",
        "Market Insights"
    ]
)

# ---------------- EMAIL SETTINGS ----------------
st.sidebar.subheader("Email Alert Settings")

sender_email = st.sidebar.text_input("Sender Email")
receiver_email = st.sidebar.text_input("Receiver Email")
email_password = st.sidebar.text_input("App Password", type="password")

st.sidebar.info("Email alerts will be sent automatically when high risk is detected.")

# ---------------- EMAIL FUNCTION ----------------
def send_email_alert(coin, volatility, sender, receiver, password):

    subject = "Crypto Portfolio Risk Alert"

    body = f"""
High Risk Cryptocurrency Detected

Coin: {coin}
Volatility: {volatility}

Recommendation:
Please review your crypto investment portfolio.
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()

        server.login(sender,password)

        server.sendmail(sender,receiver,msg.as_string())

        server.quit()

        return True

    except:
        return False

# ---------------- ML MODEL ----------------
def predict_price(df, coin):

    data = df[df["cryptocurrency"] == coin].reset_index()

    data["day"] = np.arange(len(data))

    X = data[["day"]]
    y = data["price"]

    model = LinearRegression()
    model.fit(X,y)

    future = model.predict([[len(data)+30]])

    return round(future[0],2)

# ---------------- PORTFOLIO GROWTH ----------------
def portfolio_growth(df, coin, investment):

    coin_data = df[df["cryptocurrency"] == coin]

    avg = coin_data["price"].mean()
    latest = coin_data["price"].iloc[-1]

    growth_rate = (latest - avg) / avg

    future_value = investment * (1 + growth_rate)

    return round(future_value,2)

# ------------------------------------------------
# DASHBOARD
# ------------------------------------------------
if page == "Dashboard":

    st.title("Crypto Market Dashboard")

    volatility = crypto_data.groupby("cryptocurrency")["price"].std()
    avg_price = crypto_data.groupby("cryptocurrency")["price"].mean()
    latest_price = crypto_data.groupby("cryptocurrency")["price"].last()

    returns = ((latest_price - avg_price) / avg_price) * 100

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Total Cryptos",len(volatility))
    col2.metric("Highest Risk",volatility.idxmax())
    col3.metric("Top Performer",returns.idxmax())
    col4.metric("Average Return",f"{returns.mean():.2f}%")

    st.subheader("Price Trend")

    coin = st.selectbox("Select Cryptocurrency",crypto_data["cryptocurrency"].unique())

    coin_data = crypto_data[crypto_data["cryptocurrency"] == coin]

    st.line_chart(coin_data["price"])

    st.subheader("Risk Distribution")

    fig,ax = plt.subplots()

    ax.bar(volatility.index,volatility.values,color="orange")

    st.pyplot(fig)

# ------------------------------------------------
# INVESTMENT PLANNER
# ------------------------------------------------
elif page == "Investment Planner":

    st.title("Investment Planner")

    amount = st.number_input("Investment Amount (INR)",min_value=1000)

    coin = st.selectbox("Cryptocurrency",crypto_data["cryptocurrency"].unique())

    percent = st.slider("Investment Percentage",10,100,50)

    if st.button("Calculate Investment"):

        invest = (percent/100)*amount

        st.success(f"Investment in {coin}: ₹{invest}")

        fig,ax = plt.subplots()

        ax.pie(
            [invest,amount-invest],
            labels=[coin,"Remaining"],
            autopct="%1.1f%%",
            colors=["gold","gray"]
        )

        st.pyplot(fig)

        df = pd.DataFrame({
            "Cryptocurrency":[coin],
            "Investment":[invest]
        })

        df.to_csv(
            "data/processed/customer_investments.csv",
            mode="a",
            header=False,
            index=False
        )

# ------------------------------------------------
# RISK ANALYZER + EMAIL ALERT
# ------------------------------------------------
elif page == "Risk Analyzer":

    st.title("Crypto Risk Analyzer")

    volatility = crypto_data.groupby("cryptocurrency")["price"].std()

    df = pd.DataFrame({
        "Cryptocurrency":volatility.index,
        "Volatility":volatility.values
    })

    st.dataframe(df)

    fig,ax = plt.subplots()

    ax.scatter(df["Cryptocurrency"],df["Volatility"],color="red")

    st.pyplot(fig)

    high_risk = df[df["Volatility"] > 1000]

    if not high_risk.empty:

        st.warning("High Risk Cryptocurrency Detected")

        st.write(high_risk)

        if sender_email and receiver_email and email_password:

            for coin in high_risk["Cryptocurrency"]:

                vol = high_risk.loc[
                    high_risk["Cryptocurrency"] == coin,
                    "Volatility"
                ].values[0]

                sent = send_email_alert(
                    coin,
                    vol,
                    sender_email,
                    receiver_email,
                    email_password
                )

                if sent:
                    st.success(f"Email Alert Sent to {receiver_email}")
                else:
                    st.error("Email Sending Failed")

        else:
            st.info("Enter email details in sidebar to enable alerts.")

# ------------------------------------------------
# PRICE PREDICTION
# ------------------------------------------------
elif page == "Price Prediction":

    st.title("Crypto Price Prediction (Linear Regression)")

    coin = st.selectbox(
        "Select Cryptocurrency",
        crypto_data["cryptocurrency"].unique()
    )

    if st.button("Predict Price"):

        predicted = predict_price(crypto_data,coin)

        st.success(f"Estimated price after 30 days: ₹{predicted}")

# ------------------------------------------------
# PORTFOLIO GROWTH
# ------------------------------------------------
elif page == "Portfolio Growth":

    st.title("Portfolio Growth Simulator")

    amount = st.number_input("Investment Amount",min_value=1000)

    coin = st.selectbox("Cryptocurrency",crypto_data["cryptocurrency"].unique())

    if st.button("Simulate Growth"):

        future = portfolio_growth(crypto_data,coin,amount)

        st.success(f"Estimated Portfolio Value: ₹{future}")

        fig,ax = plt.subplots()

        ax.bar(["Initial","Projected"],[amount,future],color=["blue","green"])

        st.pyplot(fig)

# ------------------------------------------------
# MARKET INSIGHTS
# ------------------------------------------------
elif page == "Market Insights":

    st.title("Crypto Market Insights")

    st.write("""
Bitcoin is the first decentralized cryptocurrency introduced in 2009.
Ethereum enables smart contracts and decentralized applications.
Tether is a stablecoin pegged to the US Dollar.
""")

    st.markdown("### Live Crypto Market Links")

    st.markdown("""
Bitcoin → https://www.coingecko.com/en/coins/bitcoin  

Ethereum → https://www.coingecko.com/en/coins/ethereum  

Tether → https://www.coingecko.com/en/coins/tether  

Data Sources:
CoinGecko | CoinMarketCap | TradingView
""")

    st.subheader("Market Growth")

    avg_price = crypto_data.groupby("date")["price"].mean()

    st.area_chart(avg_price)