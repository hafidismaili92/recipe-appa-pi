from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):

    def test_createUser_success(self):
        email="hafid@example.com"
        password = "123456"

        user = get_user_model().objects.create_user(email=email,password=password)


        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email_success(self):
        """test user normalize success"""
        emails = [{"email":"Haif@EXample.com","normlizedEmail":"Haif@example.com"}]

        for email in emails:
            user = get_user_model().objects.create_user(email=email["email"],password="123456")
            self.assertEqual(user.email,email["normlizedEmail"])

    def test_create_superuser_success(self):
        email="super@example.com"
        password = "123456"
        user = get_user_model().objects.create_superuser(email=email,password=password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)





