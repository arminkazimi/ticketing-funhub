from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class CustomUserTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.assertEqual(user.email, 'user@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_email_normalized(self):
        email = 'test@EXAMPLE.com'
        user = self.User.objects.create_user(email=email, password='testpass123')
        self.assertEqual(user.email, email.lower())

    def test_email_required(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='', password='testpass123')

    def test_create_superuser_with_non_staff_status(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='admin@example.com',
                password='testpass123',
                is_staff=False
            )

    def test_create_superuser_with_non_superuser_status(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='admin@example.com',
                password='testpass123',
                is_superuser=False
            )