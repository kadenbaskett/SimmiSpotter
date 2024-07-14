import smtplib
import sys
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv('NOTIFICATION_EMAIL')
PASSWORD = os.getenv('NOTIFICATION_EMAIL_PASSWORD')

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}

def send_message(recipients, message):
    auth = (EMAIL, PASSWORD)
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    recipient_addresses = [phone_number + CARRIERS[carrier] for phone_number, carrier in recipients]
    server.sendmail(auth[0], recipient_addresses, message)
    
    server.quit()

# python notifications/text.py 1234567890 att 2089493157 verizon "Hello, this is a test message"
if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) % 2 != 0:
        print(f"Usage: python3 {sys.argv[0]} <PHONE_NUMBER1> <CARRIER1> ... <PHONE_NUMBERN> <CARRIER> <MESSAGE>")
        sys.exit(0)

    recipients = [(sys.argv[i], sys.argv[i + 1]) for i in range(1, len(sys.argv) - 1, 2)]
    message = sys.argv[-1]

    send_message(recipients, message)
