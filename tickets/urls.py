from django.urls import path
from .views import (
    TicketListView,
    TicketDetailView,
    TicketCreateView,
    ticket_reply,
    close_ticket
)

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket-list'),
    path('create/', TicketCreateView.as_view(), name='ticket-create'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:pk>/reply/', ticket_reply, name='ticket-reply'),
    path('<int:pk>/close/', close_ticket, name='close-ticket'),
]