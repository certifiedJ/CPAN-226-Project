from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmailForm
from .email_handler import send_email
from .models import EmailHistory
import json

def email_form(request):
    """Display and process the email form"""
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            recipients = form.cleaned_data['recipients']
            cc = form.cleaned_data['cc']
            bcc = form.cleaned_data['bcc']  # Retrieve BCC field
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            attachments = form.cleaned_data['attachments']
            if not isinstance(attachments, list):
                attachments = [attachments] if attachments else []

            # Send the email with BCC included
            success, message, attachment_names = send_email(sender, recipients, cc, bcc, subject, body, attachments)

            if success:
                # Save to history including BCC
                email_record = EmailHistory(
                    sender=sender,
                    recipients=recipients,
                    cc=cc,
                    bcc=bcc,
                    subject=subject,
                    body=body,
                    attachment_names=json.dumps(attachment_names) if attachment_names else ""
                )
                email_record.save()

                messages.success(request, "Email sent successfully!")
                return redirect('email_success')
            else:
                messages.error(request, message)
    else:
        form = EmailForm()

    return render(request, 'emailer/email_form.html', {'form': form})


def email_success(request):
    """Display success page after sending email"""
    return render(request, 'emailer/success.html')


def email_history(request):
    """Display history of sent emails"""
    emails = EmailHistory.objects.all().order_by('-sent_at')

    # Process attachment names for display
    for email in emails:
        if email.attachment_names:
            try:
                email.attachment_list = json.loads(email.attachment_names)
            except:
                email.attachment_list = []
        else:
            email.attachment_list = []

    return render(request, 'emailer/history.html', {'emails': emails})
