import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
from django.conf import settings

def send_email(sender, recipients, cc, bcc, subject, body, attachments=None):
    """Send email using SMTP with support for multiple attachments"""

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender

    # Process recipients
    recipient_list = [email.strip() for email in recipients.split(',') if email.strip()]
    msg['To'] = ', '.join(recipient_list)

    # Process CC if any
    cc_list = []
    if cc:
        cc_list = [email.strip() for email in cc.split(',') if email.strip()]
        msg['Cc'] = ', '.join(cc_list)

    # Process BCC if any (do not add a header for BCC)
    bcc_list = []
    if bcc:
        bcc_list = [email.strip() for email in bcc.split(',') if email.strip()]

    # Combine all recipients (BCC is hidden from the email header)
    all_recipients = recipient_list + cc_list + bcc_list

    msg['Subject'] = subject

    # Attach body
    msg.attach(MIMEText(body, 'plain'))

    # Attach files if provided
    attachment_names = []
    if attachments:
        for attachment in attachments:
            attachment_name = basename(attachment.name)
            attachment_names.append(attachment_name)
            part = MIMEApplication(attachment.read(), Name=attachment_name)
            part['Content-Disposition'] = f'attachment; filename="{attachment_name}"'
            msg.attach(part)

    # Create secure context
    context = ssl.create_default_context()

    # Get email settings from Django settings
    email_host = settings.EMAIL_HOST
    email_port = settings.EMAIL_PORT
    email_user = settings.EMAIL_HOST_USER
    email_password = settings.EMAIL_HOST_PASSWORD

    # Send email
    try:
        with smtplib.SMTP_SSL(email_host, email_port, context=context) as server:
            server.login(email_user, email_password)
            server.sendmail(sender, all_recipients, msg.as_string())
        return True, "Email sent successfully", attachment_names
    except Exception as e:
        return False, f"Error sending email: {str(e)}", []
