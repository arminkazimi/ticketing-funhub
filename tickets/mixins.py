from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class TicketAccessMixin(UserPassesTestMixin):
    def test_func(self):
        ticket = self.get_object()
        user = self.request.user
        has_permission = user.has_perm('tickets.can_reply_to_tickets')
        print(has_permission)
        return has_permission or user.is_staff or ticket.created_by == user

    def handle_no_permission(self):
        raise PermissionDenied("You don't have permission to access this ticket.")