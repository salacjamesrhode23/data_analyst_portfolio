def fetch_email_bodies(user, password, subject_filter, imap_url='imap.gmail.com')
    
    # Connect to mailbox
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(user, password)
    mail.select('Inbox')

    # Search email matching subject
    status, data = mail.search(None, 'SUBJECT', subject_filter)
    email_ids = data[0].split()

    all_bodies = []

    # Fecth each email body
    for email_id in email_ids:
        status, data = mail.fetch(email_id, '(RFC822)')
        for _, raw_msg in (part for part in data if isinstance(part, tuple)):
            msg = email.message_from_bytes(raw_msg, policy=policy.default)
            body = get_email_body(msg)
            all_bodies.append(body)

    mail.logout()
    return all_bodies