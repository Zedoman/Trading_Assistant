import streamlit as st
import tensorflow as tf
import requests
import os
from dotenv import load_dotenv
import json
import hmac
import hashlib
import base64
import datetime

# Load environment variables
load_dotenv()
OKX_API_KEY = os.getenv("OKX_API_KEY")
OKX_SECRET_KEY = os.getenv("OKX_SECRET_KEY")
OKX_PASSPHRASE = os.getenv("OKX_API_PASSPHRASE")
OKX_PROJECT_ID = os.getenv("OKX_PROJECT_ID")

# OKX DEX API base URL
BASE_URL = "https://web3.okx.com/api/v5/dex/aggregator"

# Helper function to generate OKX API signature
def generate_signature(timestamp, method, request_path, body, secret_key):
    if body:
        body_str = json.dumps(body)
    else:
        body_str = ""
    message = f"{timestamp}{method}{request_path}{body_str}"
    hmac_key = secret_key.encode('utf-8')
    message_bytes = message.encode('utf-8')
    signature = hmac.new(hmac_key, message_bytes, hashlib.sha256).digest()
    return base64.b64encode(signature).decode('utf-8')

# Helper function to create OKX API headers
def create_okx_headers(method, endpoint, body=None):
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    request_path = f"{endpoint}{'' if not body else json.dumps(body)}"
    signature = generate_signature(timestamp, method, endpoint, body, OKX_SECRET_KEY)
    headers = {
        "OK-ACCESS-KEY": OKX_API_KEY,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": OKX_PASSPHRASE,
        "Content-Type": "application/json"
    }
    return headers

# Function to fetch tokens from OKX DEX API
def fetch_tokens(chain_index):
    endpoint = f"/api/v5/dex/aggregator/all-tokens?chainIndex={chain_index}"
    url = f"{BASE_URL}{endpoint}"
    headers = create_okx_headers("GET", endpoint)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch tokens: {e}")
        return None

# Function to execute swap using OKX DEX API
def execute_swap(chain_index, from_token, to_token, amount, wallet_address, slippage=0.05):
    endpoint = f"/api/v5/dex/aggregator/swap?chainIndex={chain_index}&amount={amount}&toTokenAddress={to_token}&fromTokenAddress={from_token}&slippage={slippage}&userWalletAddress={wallet_address}"
    url = f"{BASE_URL}/swap?chainIndex={chain_index}&amount={amount}&toTokenAddress={to_token}&fromTokenAddress={from_token}&slippage={slippage}&userWalletAddress={wallet_address}"
    payload = {
        "gasless": True,
        "source": "GrokAssistant"
    }
    headers = create_okx_headers("GET", endpoint, payload)
    try:
        response = requests.get(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Swap failed: {e}")
        return None

# AI Model for market prediction (simplified mock)
def predict_market_trend():
    # Mock data for demonstration (replace with real market data in production)
    mock_features = tf.random.uniform([1, 5])  # Mock input features
    mock_model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(5,)),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    prediction = mock_model(mock_features).numpy()[0][0]
    return "Bullish" if prediction > 0.5 else "Bearish"

# Streamlit UI
st.title("AI-Powered Gasless DeFi Trading Assistant")

# Sidebar for user inputs
st.sidebar.header("Trade Settings")
blockchain = st.sidebar.selectbox("Select Blockchain", ["Ethereum", "BNB Chain", "Polygon"])
chain_index = {"Ethereum": 1, "BNB Chain": 56, "Polygon": 137}[blockchain]
risk_level = st.sidebar.slider("Risk Level", 1, 10, 5)
strategy = st.sidebar.selectbox("Trading Strategy", ["Conservative", "Moderate", "Aggressive"])
wallet_address = st.sidebar.text_input("Wallet Address")
from_token = st.sidebar.text_input("From Token Address")
to_token = st.sidebar.text_input("To Token Address")
amount = st.sidebar.number_input("Amount to Trade", min_value=0.0, value=1.0)

# Fetch and display tokens
tokens_data = fetch_tokens(chain_index)
if tokens_data:
    st.write("Available Tokens:")
    st.json(tokens_data)

# AI Market Prediction
if st.button("Analyze Market"):
    trend = predict_market_trend()
    st.write(f"Market Trend Prediction: {trend}")

# Execute Trade
if st.button("Execute Trade"):
    if not wallet_address or not from_token or not to_token:
        st.error("Please provide wallet address and token addresses.")
    else:
        swap_result = execute_swap(chain_index, from_token, to_token, amount, wallet_address)
        if swap_result:
            st.success("Trade executed successfully!")
            st.json(swap_result)

# Mock Portfolio Chart (replace with real data in production)
st.subheader("Portfolio Performance")
st.line_chart([100, 110, 105, 120, 115])  # Mock data