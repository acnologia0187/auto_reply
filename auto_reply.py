import imaplib
import smtplib
import time
import schedule
from email.mime.text import MIMEText
from email.parser import BytesParser
from email.policy import default

# Email configuration
EMAIL = 'your_email@gmail.com'
PASSWORD = 'your_password'
SMTP_SERVER = 'smtp.gmail.com'
IMAP_SERVER = 'imap.gmail.com'

def check_email():
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')

        # Search for unseen emails
        status, messages = mail.search(None, '(UNSEEN)')
        email_ids = messages[0].split()

        for email_id in email_ids:
            # Fetch the email
            _, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = BytesParser(policy=default).parsebytes(msg_data[0][1])

            # Send a reply
            send_reply(msg['From'])

            # Mark the email as seen
            mail.store(email_id, '+FLAGS', '\\Seen')

        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

def send_reply(to_email):
    try:
        # Create the reply message
        reply_message = "Sorry, I can not get to you right now. This is an automated response."
        msg = MIMEText(reply_message)
        msg['Subject'] = 'Re: Your Email'
        msg['From'] = EMAIL
        msg['To'] = to_email

        # Send the reply
        with smtplib.SMTP(SMTP_SERVER, 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())
            print(f"Replied to {to_email}")
    except Exception as e:
        print(f"Failed to send reply: {e}")

# Schedule the email checking function to run every hour
schedule.every().hour.do(check_email)

# Keep the script running
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
