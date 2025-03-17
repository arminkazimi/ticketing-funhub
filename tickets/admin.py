from django.contrib import admin
from .models import Ticket, TicketMessage

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')


@admin.register(TicketMessage)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)
