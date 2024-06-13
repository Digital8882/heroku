from flask import Flask, request, jsonify, send_from_directory
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import asyncio
import traceback
import builtins
import re
import httpx
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.enums import TA_JUSTIFY
from SL_agents import researcher, product_manager, marketing_director, sales_director
from SL_tasks import icp_task, get_channels_task_template, pains_task, gains_task, jtbd_task, propdesign_task, customerj_task
from langchain_openai import ChatOpenAI
from langsmith import traceable
from crewai import Crew, Process, Task
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Swift Launch Backend API"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Load environment variables from .env file
load_dotenv()

smtp_server = "mail.privateemail.com"
smtp_port = 587
email_address = "yourorder@swiftlaunch.biz"
email_password = os.environ.get('EMAIL_PASSWORD')
LANGSMITH_API_KEY = os.environ.get('LANGSMITH_API_KEY')
os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "King Tikt"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Save the original print function
original_print = builtins.print

# Define a patched print function that logs instead of printing
def patched_print(*args, **kwargs):
    try:
        original_print(*args, **kwargs)
    except BrokenPipeError:
        logging.error(f"BrokenPipeError: {args}")
        logging.debug(traceback.format_exc())

# Patch the print function
builtins.print = patched_print

@traceable
def format_output(output):
    return output.strip()

@traceable
def create_pdf(content, filename):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, spaceAfter=3.6))  # Reduce spacing by 50%
    styles.add(ParagraphStyle(name='Bold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13.2))  # Increase font size by 10%
    styles['Normal'].fontSize = 13.2  # Increase font size by 10%

    elements = []

    # Add header
    header = Paragraph("<para align=right><font color='orange' size=12>Swift Launch Report</font></para>", styles['Normal'])
    elements.append(header)
    elements.append(Spacer(1, 18))  # Small spacer after the header

    # Split content into lines
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith('## '):
            elements.append(Spacer(1, 13.5))  # Increase space above headers by 50%
            elements.append(Paragraph(line[3:], styles['Bold']))  # Bold and underline headers
            elements.append(Spacer(1, 3.6))  # Space after headers
        elif line.startswith('-'):
            # Handle bullet points
            items = line.split('- ')[1:]
            list_items = []
            for item in items:
                list_items.append(ListItem(Paragraph(item, styles['Justify']), leftIndent=20))
            elements.append(ListFlowable(list_items, bulletType='bullet'))
        elif line.startswith('**') and line.endswith('**'):
            # Handle bold lines
            elements.append(Paragraph(line.strip('*'), styles['Bold']))
            # Add specific check for the section needing more space
            if line.strip('*') == "Unique Selling Points and Positioning:":
                elements.append(Spacer(1, 14.4))  # Increase space after specific bold lines by 100%
            else:
                elements.append(Spacer(1, 3.6))  # Default space after bold lines
        else:
            # Handle normal paragraphs
            elements.append(Paragraph(line, styles['Justify']))
            elements.append(Spacer(1, 1.8))  # Reduce spacing by 50% below headers and content

    doc.build(elements)

    buffer.seek(0)
    with open(filename, 'wb') as f:
        f.write(buffer.getvalue())
    buffer.seek(0)
    return buffer

@traceable
def generate_pdf(icp_output, channels_output, pains_output, gains_output, jtbd_output, propdesign_output, customerj_output):
    # Combine all task outputs into a single markdown string
    combined_content = f"""
## ICP Output
{icp_output}

## Channels Output
{channels_output}

## Pains Output
{pains_output}

## Gains Output
{gains_output}

## JTBD Output
{jtbd_output}

## Product Design Output
{propdesign_output}

## Customer Journey Output
{customerj_output}
    """
    
    # Convert the combined content to HTML
    html_content = markdown.markdown(combined_content)

    # Create the PDF file
    output_filename = "Swift_Launch_Report.pdf"
    create_pdf(html_content, output_filename)
    logging.info(f"PDF generated: {output_filename}")

    # Check file size
    file_size = os.path.getsize(output_filename)
    logging.info(f"PDF file size: {file_size} bytes")
    if file_size > 20 * 1024 * 1024:  # Check if file size is greater than 20MB
        logging.error("PDF file size exceeds the 20MB limit")
        return None

    return output_filename

@traceable
def send_email_with_pdf(pdf_filename):
    try:
        if not pdf_filename or not os.path.exists(pdf_filename):
            logging.error(f"File not found or exceeds size limit: {pdf_filename}")
            return False

        logging.info(f"Preparing to send email to {RECEIVER_EMAIL} with attachment {pdf_filename}")

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = 'Your Swift Launch Report'
        body = 'Please find attached your Swift Launch Report.'
        msg.attach(MIMEText(body, 'plain'))

        with open(pdf_filename, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={pdf_filename}")
            msg.attach(part)

        logging.info("Connecting to SMTP server")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        logging.info("Sending email")
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        logging.info(f"Email sent to {RECEIVER_EMAIL} with attachment {pdf_filename}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        logging.debug(traceback.format_exc())
        return False

@traceable
async def start_crew_process(email, product_service, price, currency, payment_frequency, selling_scope, location, marketing_channels, features, benefits, retries=3):
    task_description = f"New task from {email} selling {product_service} at {price} {currency} with payment frequency {payment_frequency}."
    if selling_scope == "Locally":
        task_description += f" Location: {location}."
    task_description += f" Focus on the following marketing channels: {', '.join(marketing_channels)}."

    new_task = Task(description=task_description, expected_output="...")

    project_crew = Crew(
        tasks=[new_task, icp_task],
        agents=[researcher, product_manager, marketing_director, sales_director],
        manager_llm=ChatOpenAI(temperature=0, model="gpt-4o"),
        max_rpm=4,
        process=Process.hierarchical,
    )

    for attempt in range(retries):
        try:
            logging.info(f"Starting crew process, attempt {attempt + 1}")
            results = await asyncio.wait_for(project_crew.kickoff(), timeout=110)
            icp_output = icp_task.output.exported_output if hasattr(icp_task.output, 'exported_output') else "No ICP output"
            logging.info("Crew process completed successfully")
            return icp_output, "channels_output", "pains_output", "gains_output", "jtbd_output", "propdesign_output", "customerj_output"
        except asyncio.TimeoutError:
            logging.error(f"TimeoutError on attempt {attempt + 1}")
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)
            else:
                raise
        except BrokenPipeError as e:
            logging.error(f"BrokenPipeError occurred on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)
            else:
                raise
        except Exception as e:
            logging.error(f"An error occurred during the crew process: {e}")
            raise

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    email = data.get("email")
    product_service = data.get("product_service")
    price = data.get("price")
    currency = data.get("currency")
    payment_frequency = data.get("payment_frequency")
    selling_scope = data.get("selling_scope")
    location = data.get("location")
    marketing_channels = data.get("marketing_channels")
    features = data.get("features")
    benefits = data.get("benefits")

    try:
        icp_output, channels_output, pains_output, gains_output, jtbd_output, propdesign_output, customerj_output = asyncio.run(
            start_crew_process(
                email, product_service, price, currency, payment_frequency, selling_scope, location, marketing_channels, features, benefits
            )
        )

        pdf_filename = generate_pdf(icp_output, channels_output, pains_output, gains_output, jtbd_output, propdesign_output, customerj_output)
        if pdf_filename:
            if send_email_with_pdf(pdf_filename):
                return jsonify({"status": "success", "message": "Report generated and email sent successfully"}), 200
            else:
                return jsonify({"status": "error", "message": "Failed to send email"}), 500
        else:
            return jsonify({"status": "error", "message": "PDF generation failed or exceeds size limit"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.debug(traceback.format_exc())
        return jsonify({"status": "error", "message": "An internal error occurred"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
