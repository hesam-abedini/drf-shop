"""
test for user models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from user.models import Address


class ModelTests(TestCase):
    """
    Test Models
    """
    def test_create_user_with_address(self):
        """
        test for creating user
        """
        email="test@example.com"
        password="Yestpass1234"
        address_info={
            "state":"NY",
            "city":"New York",
            "address_1":"fifth avenue",
            "postal_code":"1234567",
            "phone_number":"09356732"
        }

        address=Address.objects.create(**address_info)
        user=get_user_model().objects.create_user(email=email,password=password,address=address)
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.address.state,address_info["state"])
        self.assertEqual(user.address.city,address_info["city"])

