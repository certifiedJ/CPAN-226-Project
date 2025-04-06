from django import forms
from django.forms.widgets import ClearableFileInput

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class EmailForm(forms.Form):
    sender = forms.EmailField(
        label="Sender's Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    recipients = forms.CharField(
        label="Recipient Email(s)",
        help_text="Enter email addresses separated by commas",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cc = forms.CharField(
        label="CC",
        required=False,
        help_text="Enter CC email addresses separated by commas",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    bcc = forms.CharField(
        label="BCC",
        required=False,
        help_text="Enter BCC email addresses separated by commas",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        label="Subject",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    body = forms.CharField(
        label="Email Body",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )
    attachments = MultipleFileField(
        label="Attachments",
        required=False,
        widget=MultipleFileInput(attrs={'class': 'form-control'})
    )

    def clean_recipients(self):
        recipients = self.cleaned_data.get('recipients', '')
        emails = [email.strip() for email in recipients.split(',') if email.strip()]
        for email in emails:
            if '@' not in email:
                raise forms.ValidationError(f"Invalid email address: {email}")
        return recipients

    def clean_cc(self):
        cc = self.cleaned_data.get('cc', '')
        if not cc:
            return cc
        emails = [email.strip() for email in cc.split(',') if email.strip()]
        for email in emails:
            if '@' not in email:
                raise forms.ValidationError(f"Invalid email address: {email}")
        return cc

    def clean_bcc(self):
        bcc = self.cleaned_data.get('bcc', '')
        if not bcc:
            return bcc
        emails = [email.strip() for email in bcc.split(',') if email.strip()]
        for email in emails:
            if '@' not in email:
                raise forms.ValidationError(f"Invalid email address: {email}")
        return bcc
