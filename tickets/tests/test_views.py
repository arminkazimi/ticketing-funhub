from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from tickets.models import Ticket, TicketMessage
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class TicketViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = get_user_model().objects.create_user(
            
            email='admin@example.com',
            password='adminpass123'
        )
        content_type = ContentType.objects.get_for_model(Ticket)
        view_all_permission = Permission.objects.get(
            codename='can_view_all_tickets',
            content_type=content_type,
        )
        self.admin_user.user_permissions.add(view_all_permission)
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            created_by=self.user
        )

    def test_ticket_list_view_user(self):
        self.client.login(username=self.user.email, password='testpass123')
        response = self.client.get(reverse('ticket-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket_list.html')
        self.assertContains(response, 'Test Ticket')

    def test_ticket_list_view_admin(self):
        self.client.login(username=self.admin_user.email, password='adminpass123')
        other_ticket = Ticket.objects.create(
            title='Other Ticket',
            created_by=self.admin_user
        )
        response = self.client.get(reverse('ticket-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ticket')
        self.assertContains(response, 'Other Ticket')

    def test_ticket_detail_view(self):
        self.client.login(username=self.user.email, password='testpass123')
        response = self.client.get(
            reverse('ticket-detail', kwargs={'pk': self.ticket.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket_detail.html')
        self.assertContains(response, 'Test Ticket')

    def test_ticket_create_view(self):
        self.client.login(username=self.user.email, password='testpass123')
        test_file = SimpleUploadedFile(
            'test.txt',
            b'Test file content',
            content_type='text/plain'
        )
        response = self.client.post(
            reverse('ticket-create'),
            {
                'title': 'New Ticket',
                'description': 'New ticket description',
                'attachment': test_file
            }
        )
        self.assertEqual(response.status_code, 302)
        new_ticket = Ticket.objects.get(title='New Ticket')
        self.assertEqual(new_ticket.created_by, self.user)
        self.assertEqual(new_ticket.messages.count(), 1)

    def test_ticket_reply(self):
        self.client.login(username=self.user.email, password='testpass123')
        test_file = SimpleUploadedFile(
            'reply.txt',
            b'Reply file content',
            content_type='text/plain'
        )
        response = self.client.post(
            reverse('ticket-reply', kwargs={'pk': self.ticket.pk}),
            {
                'content': 'Test reply',
                'attachment': test_file
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.ticket.messages.count(), 1)
        message = self.ticket.messages.first()
        self.assertEqual(message.content, 'Test reply')
        self.assertTrue(message.attachment)

    def test_unauthorized_ticket_detail_access(self):
        other_user = get_user_model().objects.create_user(
            email='other@example.com',
            password='otherpass123'
        )
        self.client.login(username=other_user.email, password='otherpass123')
        response = self.client.get(
            reverse('ticket-detail', kwargs={'pk': self.ticket.pk})
        )
        self.assertEqual(response.status_code, 403)