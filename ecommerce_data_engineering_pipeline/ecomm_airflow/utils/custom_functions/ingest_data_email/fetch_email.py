import imaplib
import email
from email import policy

def get_email_body(message):
    if message.is_multipart():
        for part in message.iter_parts():
            content_type = part.get_content_type()
            if content_type in ["text/plain", "text/html"]:
                return part.get_content()
    else:
        return message.get_content()

def fetch_email_bodies(user, password, subject_filter, imap_url='imap.gmail.com'):
    
    # Connect to mailbox
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(user, password)
    mail.select('Inbox')

    # Search email matching subject
    status, data = mail.search(None, 'SUBJECT', subject_filter)
    email_ids = data[0].split()[:5]

    all_bodies = []

    # Fetch each email body
    for email_id in email_ids:
        status, data = mail.fetch(email_id, '(RFC822)')
        for _, raw_msg in (part for part in data if isinstance(part, tuple)):
            msg = email.message_from_bytes(raw_msg, policy=policy.default)
            body = get_email_body(msg)   # assumes you defined get_email_body
            all_bodies.append(body)

    mail.logout()
    return all_bodies