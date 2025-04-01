from django.contrib import admin
from .models import EmailHistory

@admin.register(EmailHistory)
class EmailHistoryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipients', 'sent_at')
    search_fields = ('subject', 'sender', 'recipients', 'body')
    list_filter = ('sent_at',)
    readonly_fields = ('sent_at',)