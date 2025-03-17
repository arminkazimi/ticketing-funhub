from django.db import models
from django.conf import settings

class Ticket(models.Model)    :

    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator')
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ('can_view_all_tickets', 'Can view all tickets'),
            ('can_reply_to_tickets', 'Can reply to tickets'),
        ]

class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    replied_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='ticket_attachments/', null=True, blank=True)

    def __str__(self):
        return f"Message on {self.ticket.title} by {self.user.email}"

    class Meta:
        ordering = ['created_at']

