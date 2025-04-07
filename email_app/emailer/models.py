from django.db import models

class EmailHistory(models.Model):
    sender = models.EmailField()
    recipients = models.TextField()
    cc = models.TextField(blank=True)
    bcc = models.TextField(blank=True)  # New field for BCC addresses
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    attachment_names = models.TextField(blank=True)  # Stored as JSON string

    def __str__(self):
        return f"{self.subject} - {self.sent_at}"