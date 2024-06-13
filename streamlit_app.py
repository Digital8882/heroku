import streamlit as st
import requests
import os

# Set the backend URL directly
backend_url = "https://sw-report-7df9fed5c54e.herokuapp.com"

st.title("ICP and Channels Report Generator")

with st.form("input_form"):
    email = st.text_input("Email")
    product_service = st.text_input("Product/Service")
    price = st.number_input("Price", min_value=0.0, format="%f")
    currency = st.selectbox("Currency", ["USD", "EUR", "GBP"])
    payment_frequency = st.selectbox("Payment Frequency", ["One-time", "Monthly", "Yearly"])
    selling_scope = st.selectbox("Selling Scope", ["Locally", "Globally"])
    location = st.text_input("Location", disabled=(selling_scope == "Globally"))

    marketing_channels = st.multiselect("Marketing Channels", ["Facebook", "Twitter (x)", "Instagram", "Reddit", "TikTok", "SEO", "Blog", "PPC", "LinkedIn"])

    features = st.text_area("Features", help="Enter the features of your product/service")
    benefits = st.text_area("Benefits", help="Enter the benefits of your product/service")

    submit_button = st.form_submit_button(label="Generate Swift Launch Report")

if submit_button:
    st.info("Sending request to generate your report...")
    payload = {
        "email": email,
        "product_service": product_service,
        "price": price,
        "currency": currency,
        "payment_frequency": payment_frequency,
        "selling_scope": selling_scope,
        "location": location,
        "marketing_channels": marketing_channels,
        "features": features,
        "benefits": benefits
    }

    try:
        response = requests.post(f'{backend_url}/generate_report', json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        try:
            response_data = response.json()
        except ValueError:
            st.error("Failed to parse response as JSON")
            st.write("Response text:", response.text)
            response_data = None
        
        if response_data:
            st.write(f"Response status code: {response.status_code}")
            st.write(f"Response content: {response_data}")

            if response.status_code == 200:
                st.success("Report generated and email sent successfully!")
            else:
                st.error(f"Failed to generate report: {response_data.get('message')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
