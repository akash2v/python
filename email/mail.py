import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Function to read credentials from config file
def load_credentials(config_file):
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    return config_data['email'], config_data['password']

# Function to send the email
def send_email(subject, json_file_path, attachment_file_path, config_file):
    from_email, from_password = load_credentials(config_file)

    # Load the JSON file that contains recipients and message
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    recipients = data['email']  # List of recipient email addresses
    message_body = data['message']  # The message content

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['Subject'] = subject

    # Attach the message body to the email
    msg.attach(MIMEText(message_body, 'plain'))

    # Open the attachment (JSON file) and attach it to the email
    with open(attachment_file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{attachment_file_path}"')
        msg.attach(part)

    server = None  # Initialize server variable to avoid 'UnboundLocalError'
    try:
        # Establish a connection to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server (for example)
        server.starttls()  # Secure the connection

        # Login to your email account
        server.login(from_email, from_password)

        # Send email to each recipient
        for recipient in recipients:
            msg['To'] = recipient
            text = msg.as_string()
            server.sendmail(from_email, recipient, text)
            print(f"Email sent to {recipient}!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Make sure to call quit only if the server was created
        if server:
            server.quit()

# Example usage
subject = "Subject of the Email"
json_file_path = "email.json"  # Path to the JSON file with email addresses and message
attachment_file_path = "your_file.json"  # Path to the file you want to attach
config_file = "config.json"  # Path to the config file containing credentials

send_email(subject, json_file_path, attachment_file_path, config_file)
