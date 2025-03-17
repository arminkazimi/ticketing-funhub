from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from tickets.models import Ticket, TicketMessage

class TicketModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_ticket_creation(self):
        ticket = Ticket.objects.create(
            title='Test Ticket',
            created_by=self.user,
            status='open'
        )
        self.assertEqual(str(ticket), 'Test Ticket')
        self.assertEqual(ticket.status, 'open')
        self.assertEqual(ticket.created_by, self.user)

    def test_ticket_ordering(self):
        ticket1 = Ticket.objects.create(
            title='First Ticket',
            created_by=self.user
        )
        ticket2 = Ticket.objects.create(
            title='Second Ticket',
            created_by=self.user
        )
        tickets = Ticket.objects.all()
        self.assertEqual(tickets[0], ticket2)
        self.assertEqual(tickets[1], ticket1)

class TicketMessageModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            created_by=self.user
        )

    def test_message_creation(self):
        message = TicketMessage.objects.create(
            ticket=self.ticket,
            user=self.user,
            content='Test message content'
        )
        self.assertEqual(
            str(message),
            f'Message on {self.ticket.title} by {self.user.email}'
        )

    def test_message_with_attachment(self):
        test_file = SimpleUploadedFile(
            'test.txt',
            b'Test file content',
            content_type='text/plain'
        )
        message = TicketMessage.objects.create(
            ticket=self.ticket,
            user=self.user,
            content='Test message with attachment',
            attachment=test_file
        )
        self.assertTrue(message.attachment)
        self.assertIn('test.txt', message.attachment.name)

    def test_message_reply(self):
        original_message = TicketMessage.objects.create(
            ticket=self.ticket,
            user=self.user,
            content='Original message'
        )
        reply_message = TicketMessage.objects.create(
            ticket=self.ticket,
            user=self.user,
            content='Reply message',
            replied_to=original_message
        )
        self.assertEqual(reply_message.replied_to, original_message)

    def test_message_ordering(self):
        message1 = TicketMessage.objects.create(
            ticket=self.ticket,
            user=self.user,
            content='First message'
        )
        message2 = TicketMessage.objects.create(
            ticket=self.ticket,
            user=self.user,
            content='Second message'
        )
        messages = TicketMessage.objects.all()
        self.assertEqual(messages[0], message1)
        self.assertEqual(messages[1], message2)