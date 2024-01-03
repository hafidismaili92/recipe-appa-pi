"""tests for the user API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
GET_TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """create and return a new user"""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    """test public features of user api (no need to be authenticated)"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        """test create user will success"""
        payload = {
            'email':'test@exemple.com',
            'password':'testpass123',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertTrue(user.check_password(payload["password"]))

        self.assertNotIn('password',res.data)
    
    def test_user_with_email_exist_error(self):
        """error returned if user with email exist"""
        payload = {
            'email':'test@exemple.com',
            'password':'testpass123',
            'name': 'Test 2 Name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertTrue(user_exists)
    
    def test_user_short_password_error(self):
        """error returned if user with email exist"""
        payload = {
            'email':'testpassword@exemple.com',
            'password':'pw',
            'name': 'Test 2 Name'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)
    
    def test_create_token_success(self):
        user = {
            'email':'test@exemple.com',
            'password':'12345678'
        }
        create_user(**user)

        payload = {
            'email':'test@exemple.com',
            'password':'12345678'
        }

        res = self.client.post(GET_TOKEN_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertIn('token',res.data)
    
    def test_create_token_error(self):
        user = {
            'email':'test@exemple.com',
            'password':'correctpassword'
        }
        create_user(**user)

        payload = {
            'email':'test@exemple.com',
            'password':'badpassword'
        }
        res = self.client.post(GET_TOKEN_URL)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token',res.data)
    
    def test_retrieve_user_unauthorized(self):
        """Tests authentication is required"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PublicUserApiTest(TestCase):
    """handle authenticated tests"""
    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password = 'testpass',
            name ='test name'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_profil_success(self):
        """Test retrieve profile of authenticated user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'name':self.user.name,
            'email':self.user.email
        })
    
    def test_post_me_not_allowed(self):
        """test POST is not allowed on me endpoint"""

        res = self.client.post(ME_URL,{})

        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_user_profile(self):
        """test updating the user profile for the authenticated user"""

        payload = {'name':'updated name','password':'newpassword123'}

        res = self.client.patch(ME_URL,payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name,payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code,status.HTTP_200_OK)