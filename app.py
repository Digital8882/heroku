from flask import Flask, request, jsonify, send_file
import os
import logging
import langsmith from traceback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.enums import TA_JUSTIFY
import requests
import httpx
from dotenv import load_dotenv

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



# Load environment variables from .env file
load_dotenv()

smtp_server = "mail.privateemail.com"
smtp_port = 587
email_address = "yourorder@swiftlaunch.biz"
email_password = os.environ.get('EMAIL_PASSWORD')
LANGSMITH_API_KEY = os.environ.get('LANGSMITH_API_KEY')
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Airtable configuration
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = 'appPcWNUeei7MNMCj'
AIRTABLE_TABLE_NAME = 'Table%201'
EMAIL_FIELD_NAME = 'Email'
ICPF_FIELD_NAME = 'Icp'
JTBD_FIELD_NAME = 'Jtbd'
PAINS_FIELD_NAME = 'Pains'
GAINS_FIELD_NAME = 'Gains'
PROPDESIGN_FIELD_NAME = 'Propdesign'
CUSTOMERJ_FIELD_NAME = 'Customerj'
CHANNELS_FIELD_NAME = 'Channels'
VC_FIELD_NAME = 'Vc'

def send_email(subject, body, to_email, pdf_content):
    logging.debug("Preparing to send email...")
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="report.pdf"')
        msg.attach(part)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        logging.debug("Email sent successfully")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False

def update_airtable(email, icp_output, jtbd_output, pains_output, gains_output, propdesign_output, customerj_output, channels_output, vc_output):
    logging.debug("Updating Airtable...")
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "records": [
            {
                "fields": {
                    EMAIL_FIELD_NAME: email,
                    ICPF_FIELD_NAME: icp_output,
                    JTBD_FIELD_NAME: jtbd_output,
                    PAINS_FIELD_NAME: pains_output,
                    GAINS_FIELD_NAME: gains_output,
                    PROPDESIGN_FIELD_NAME: propdesign_output,
                    CUSTOMERJ_FIELD_NAME: customerj_output,
                    CHANNELS_FIELD_NAME: channels_output,
                    VC_FIELD_NAME: vc_output
                }
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        logging.debug(f"Airtable response: {response_data}")
        return response_data['records'][0]['id']
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        return None

def retrieve_from_airtable(record_id):
    logging.debug(f"Retrieving data from Airtable for record ID: {record_id}")
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}/{record_id}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        record = response.json().get('fields', {})
        logging.debug(f"Retrieved record: {record}")
        return (
            record.get(ICPF_FIELD_NAME, ''),
            record.get(JTBD_FIELD_NAME, ''),
            record.get(PAINS_FIELD_NAME, ''),
            record.get(GAINS_FIELD_NAME, ''),
            record.get(PROPDESIGN_FIELD_NAME, ''),
            record.get(CUSTOMERJ_FIELD_NAME, ''),
            record.get(CHANNELS_FIELD_NAME, ''),
            record.get(VC_FIELD_NAME, '')
        )
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve data from Airtable: {e}")
        return None, None, None, None, None, None, None, None

def create_pdf(content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    elements = []

    for section_title, section_content in content.items():
        elements.append(Paragraph(f"<b>{section_title}</b>", styles['Normal']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(section_content, styles['Justify']))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    email = data.get("email")
    icp_output = data.get("icp_output")
    jtbd_output = data.get("jtbd_output")
    pains_output = data.get("pains_output")
    gains_output = data.get("gains_output")
    propdesign_output = data.get("propdesign_output")
    customerj_output = data.get("customerj_output")
    channels_output = data.get("channels_output")
    vc_output = data.get("vc_output")

    try:
        record_id = update_airtable(email, icp_output, jtbd_output, pains_output, gains_output, propdesign_output, customerj_output, channels_output, vc_output)
        if record_id:
            st.success("Airtable updated successfully!")
            retrieved_data = retrieve_from_airtable(record_id)
            if all(retrieved_data):
                pdf_content = create_pdf({
                    "ICP Output": retrieved_data[0],
                    "JTBD Output": retrieved_data[1],
                    "Pains Output": retrieved_data[2],
                    "Gains Output": retrieved_data[3],
                    "Proposition Design": retrieved_data[4],
                    "Customer Journey": retrieved_data[5],
                    "Channels": retrieved_data[6],
                    "Value Creation": retrieved_data[7]
                })
                if send_email(subject="Your SWIFT LAUNCH WORKS Report", body="Please find attached your marketing report.", to_email=email, pdf_content=pdf_content.getvalue()):
                    return jsonify({"status": "success", "message": "Report generated and email sent successfully"}), 200
                else:
                    return jsonify({"status": "error", "message": "Failed to send the report. Please try again later."}), 500
            else:
                return jsonify({"status": "error", "message": "Failed to retrieve data from Airtable."}), 500
        else:
            return jsonify({"status": "error", "message": "Failed to update Airtable."}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.debug(traceback.format_exc())
        return jsonify({"status": "error", "message": "An internal error occurred"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

