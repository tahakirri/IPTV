import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# File to store customer data
DATA_FILE = "customers.csv"

# Load or initialize data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, parse_dates=['Purchase Date', 'Expiry Date'])
    else:
        return pd.DataFrame(columns=["Name", "Purchase Date", "Duration (days)", "Expiry Date", "Phone", "Email"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="Subscription Manager", layout="centered")

st.title("📅 Subscription Management App")

# --- Add new customer ---
with st.form("add_customer"):
    st.subheader("➕ Add New Customer")
    name = st.text_input("Customer Name")
    purchase_date = st.date_input("Purchase Date", datetime.today())
    duration = st.number_input("Subscription Duration (days)", min_value=1, value=30)
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    submitted = st.form_submit_button("Add Customer")

    if submitted:
        expiry_date = purchase_date + timedelta(days=int(duration))
        new_data = pd.DataFrame([{
            "Name": name,
            "Purchase Date": purchase_date,
            "Duration (days)": duration,
            "Expiry Date": expiry_date,
            "Phone": phone,
            "Email": email
        }])

        data = load_data()
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        st.success(f"Customer {name} added successfully!")

# --- Show current subscriptions ---
st.subheader("📋 All Subscriptions")

data = load_data()
if not data.empty:
    today = datetime.today()
    data["Days Left"] = (data["Expiry Date"] - today).dt.days
    st.dataframe(data.sort_values(by="Expiry Date"))

    # Show expiring soon
    st.subheader("⚠️ Expiring Soon (7 days or less)")
    expiring = data[data["Days Left"] <= 7]
    if not expiring.empty:
        st.warning("Some subscriptions are expiring soon!")
        st.dataframe(expiring)
    else:
        st.success("No subscriptions expiring soon.")
else:
    st.info("No customer data yet. Add some above!")

