"""
test for user api
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from user.models import Address

CREATE_USER_URL=reverse('user:create')
TOKEN_URL=reverse('user:token')

def create_user(**params):
    """create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """test public features of user api"""

    def setUp(self):
        self.client=APIClient()
        self.address_info={
            "state":"NY",
            "city":"New York",
            "address_1":"fifth avenue",
            "postal_code":"1234567",
            "phone_number":"09356732"
        }
        self.address=Address.objects.create(**self.address_info)

    def test_create_user_successfull(self):
        "test creating a user is successfull"
        payload={
            'email':'test@test.com',
            'password':'Testpass123',
            'name':'test name',
            "address":self.address_info
        }
        
        res=self.client.post(CREATE_USER_URL,format='json',data=payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user=get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(user.address.state,payload["address"]["state"])
        self.assertNotIn('password',res.data)

    def test_user_with_email_exists(self):
        """check for user with email already exists"""
        user={
            'email':'test@test.com',
            'password':'testpass123',
            'name':'test name',
        }
        payload={
            **user,
            "address":self.address_info
        }
        create_user(**user,address=self.address)
        res=self.client.post(CREATE_USER_URL,format='json',data=payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_validation(self):
        """check if password is too short or has at least one capital letter,one number and one lower case letter"""
        payload={
            'email':'test@test.com',
            'name':'test name',
            "address":self.address_info
        }

        password_sample=[
            '1234',
            'abcd',
            'abc3',
            'Abc4',
            '12345',
            'abcde',
            'abcde3',
            'ABCDE3',
            'Abcde'
        ]
        for p in password_sample:
            res=self.client.post(CREATE_USER_URL,format='json',data={**payload,'password':p})
            self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
            user_exists=get_user_model().objects.filter(email=payload['email']).exists()
            self.assertFalse(user_exists)

    def create_token_for_user(self):

        user_details={
            'name':'hesam',
            'email':'test@example.com',
            'password':'testpass213'
        }

        create_user(**user_details,address=self.address)

        payload={
            'email':user_details['email'],
            'paasword':user_details['password']
        }

        res=self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def create_token_for_user_bad_cred(self):

        user_details={
            'name':'hesam',
            'email':'test@example.com',
            'password':'testpass213'
        }

        create_user(**user_details,address=self.address)

        payload={
            'email':'ali@gmail.com',
            'paasword':user_details['password']
        }

        res=self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unathorized(self):

        res=self.client.get(reverse('user:update',kwargs={'pk':2}))
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateUserAppiTest(TestCase):

    def setUp(self):
        self.address_info={
            "state":"NY",
            "city":"New York",
            "address_1":"fifth avenue",
            "postal_code":"1234567",
            "phone_number":"09356732"
        }
        address=Address.objects.create(**self.address_info)
        address2=Address.objects.create(**self.address_info)
        self.user=create_user(
            email='test@test.com',
            password='testpass123',
            name='ali test',
            address=address
        )
        self.user2=create_user(
            email='test3@test.com',
            password='testpa3ss123',
            name='ali test3',
            address=address2
        )
        self.client=APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        
        res=self.client.get(reverse('user:update',kwargs={'pk':self.user.id}))
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data['name'],self.user.name)
        self.assertEqual(res.data['email'],self.user.email)

    def test_retrive_profile_fail(self):
        """trying to access a profile that is not yours"""

        res=self.client.get(reverse('user:update',kwargs={'pk':self.user2.id}))
        self.assertEqual(res.status_code,status.HTTP_403_FORBIDDEN)

    def test_post_profile_not_allowed(self):

        res=self.client.post(reverse('user:update',kwargs={'pk':self.user2.id}),{})
        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        
        payload={
            'name':'updated name',
            'password':'Newpassword123'
        }

        res=self.client.patch(reverse('user:update',kwargs={'pk':self.user.id}),format='json',data=payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name,payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code,status.HTTP_200_OK)

