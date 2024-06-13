import streamlit as st
import os
import requests
import logging
from langchain_openai import ChatOpenAI
from langsmith import traceable
from html.parser import HTMLParser
from crewai import Crew, Agent, Task, Process

# Streamlit UI setup
st.title("SWIFT LAUNCH WORKS")

with st.form(key='input_form_unique'):
    name = st.text_input("Name", key="name_input")
    email = st.text_input("Email", key="email_input")
    product = st.text_input("Product", key="product_input")
    price = st.number_input("Price", min_value=0, step=1, key="price_input")
    currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "JPY", "AUD"], key="currency_input")
    features = st.text_area("Features", key="features_input")
    benefits = st.text_area("Benefits", key="benefits_input")
    store = st.selectbox("Store", ["Online", "Physical", "Both"], key="store_input")
    sales_areas = st.selectbox("Sales Areas", ["Local", "National", "International"], key="sales_areas_input")
    location = st.text_input("Location", key="location_input")
    marketing_channels = st.multiselect("Marketing Channels", ["Facebook", "Reddit", "X (Twitter)", "Instagram", "SEO", "Blog", "WhatsApp", "PPC", "Email", "Snapchat"], key="marketing_channels_input")
    submit_button = st.form_submit_button(label='Generate Report')

if submit_button:
    with st.spinner("Please wait while the report is generating..."):
        try:
            # Your logic for generating the report and interacting with the Flask backend
            # For example, sending data to your Flask endpoint and receiving the report:
            response = requests.post('https://sw-report-7df9fed5c54e.herokuapp.com/generate_report', json={
                "email": email,
                "icp_output": "ICP Output Placeholder",
                "jtbd_output": "JTBD Output Placeholder",
                "pains_output": "Pains Output Placeholder",
                "gains_output": "Gains Output Placeholder",
                "propdesign_output": "Proposition Design Placeholder",
                "customerj_output": "Customer Journey Placeholder",
                "channels_output": "Channels Placeholder",
                "vc_output": "Value Creation Placeholder"
            })

            if response.status_code == 200:
                st.success("Report generation complete! Check your email.")
            else:
                st.error("Failed to generate report. Please try again.")

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8501))
    st.run(port=port)
