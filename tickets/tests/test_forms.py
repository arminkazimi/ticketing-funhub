from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from tickets.forms import TicketCreateForm, TicketMessageForm
from tickets.models import Ticket, TicketMessage

class TicketCreateFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_valid_ticket_creation(self):
        form_data = {
            'title': 'Test Ticket',
            'description': 'Test ticket description'
        }
        test_file = SimpleUploadedFile(
            'test.txt',
            b'Test file content',
            content_type='text/plain'
        )
        form = TicketCreateForm(
            data=form_data,
            files={'attachment': test_file}
        )
        form.instance.created_by = self.user
        self.assertTrue(form.is_valid())
        ticket = form.save()
        self.assertEqual(ticket.title, 'Test Ticket')
        self.assertEqual(ticket.messages.count(), 1)
        message = ticket.messages.first()
        self.assertEqual(message.content, 'Test ticket description')
        self.assertTrue(message.attachment)

    def test_invalid_ticket_creation(self):
        form_data = {
            'title': '',
            'description': ''
        }
        form = TicketCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('description', form.errors)

class TicketMessageFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            created_by=self.user
        )

    def test_valid_message_creation(self):
        form_data = {
            'content': 'Test reply content'
        }
        test_file = SimpleUploadedFile(
            'test.txt',
            b'Test file content',
            content_type='text/plain'
        )
        form = TicketMessageForm(
            data=form_data,
            files={'attachment': test_file},
            user=self.user,
            ticket=self.ticket
        )
        self.assertTrue(form.is_valid())
        message = form.save()
        self.assertEqual(message.content, 'Test reply content')
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.ticket, self.ticket)
        self.assertTrue(message.attachment)

    def test_invalid_message_creation(self):
        form_data = {'content': ''}
        form = TicketMessageForm(
            data=form_data,
            user=self.user,
            ticket=self.ticket
        )
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_message_reply(self):
        original_message = TicketMessage.objects.create(
            ticket=self.ticket,
            user=self.user,
            content='Original message'
        )
        form_data = {'content': 'Reply content'}
        form = TicketMessageForm(
            data=form_data,
            user=self.user,
            ticket=self.ticket,
            replied_to=original_message
        )
        self.assertTrue(form.is_valid())
        reply = form.save()
        self.assertEqual(reply.replied_to, original_message)