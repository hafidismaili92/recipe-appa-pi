"""test admin calpabilities"""

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class AdminSiteTest(TestCase):

    """setup before test (create super user, a user and a client and force login)"""
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            email="hafidadmin@example.com",
            password="12345678",
        )
        self.client.force_login(self.admin)
        self.user = get_user_model().objects.create_user(
            email="hafiduser@example.com",
            password="12345678",
        )
    
    def test_list_users(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res,self.user.name)
        self.assertContains(res,self.user.email)