import imaplib
import email
from email.header import decode_header

# IMAP server information
IMAP_SERVER = 'domain.com'
IMAP_PORT = 993

EMAIL_ADDRESS = 'user@domain.com'
PASSWORD = 'password'

# Establish IMAP connection
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

# Login to the IMAP server
mail.login(EMAIL_ADDRESS, PASSWORD)

# Access the inbox
mail.select('inbox')

# Fetch all messages in the inbox
result, data = mail.search(None, 'ALL')

messages = []

if result == 'OK':
    for num in data[0].split():
        result, message_data = mail.fetch(num, '(RFC822)')
        if result == 'OK':
            raw_email = message_data[0][1]
            msg = email.message_from_bytes(raw_email)
            # Decode the subject header properly
            subject = decode_header(msg['Subject'])[0][0]
            if isinstance(subject, bytes):
                # Decode the subject properly
                try:
                    subject = subject.decode('utf-8')
                except UnicodeDecodeError:
                    # If unable to decode with UTF-8, decode with ISO-8859-1 by default
                    subject = subject.decode('ISO-8859-1')
            messages.append({
                'From': msg['From'],
                'Subject': subject,
                'Date': msg['Date']
            })

# Close the IMAP connection
mail.logout()

# Display the retrieved messages
for message in messages:
    print("From:", message['From'])
    print("Subject:", message['Subject'])
    print("Date:", message['Date'])
    print("="*30)
