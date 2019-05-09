
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from bank.models import Customer

from bank.serializers import CustomerSerializer


CUSTOMER_URL = reverse('bank:customer')


def sample_customer(user, **params):
    """Create and return a sample customer"""
    defaults = {
        'fname': 'Jon',
        'lname': 'Snow',
        'city': 'Winterfell',
        'house': 'Stark'
    }
    defaults.update(params)

    return Customer.objects.create(user=user, **defaults)


class PublicBankApiTest(TestCase):
    """Test unauthenticated recipe API request"""

    def setUp(self):
        self.client = APIClient()

    def test_customer_auth_required(self):
        res = self.client.get(CUSTOMER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCustomerApiTests(TestCase):
    """Test authenticated API access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='testpass',
            username='test'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retreive_customer(self):
        """Test retreiving a customer"""
        sample_customer(user=self.user)

        res = self.client.get(CUSTOMER_URL)

        customer = Customer.objects.all().order_by('-id')

        serializer = CustomerSerializer(customer, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data[0])

    def test_customer_limited_to_user(self):
        """Test retrieving customer for user"""
        user2 = get_user_model().objects.create_user(
            email='other@gleb.com',
            password='otherpass',
            username='test_1'
        )
        sample_customer(user=user2)
        sample_customer(user=self.user)

        res = self.client.get(CUSTOMER_URL)

        customers = Customer.objects.filter(user=self.user)

        serializer = CustomerSerializer(customers, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data[0])

    def test_create_customer(self):
        """Test creating customer"""
        payload = {
            'fname': 'Ned',
            'lname': 'Stark',
            'city': 'Winterfell',
            'house': 'Stark',

        }
        res = self.client.put(CUSTOMER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        customer = Customer.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(customer, key))

    def test_create_customer_with_image(self):
        """Test creating customer"""

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            payload = {
                'fname': 'Ned',
                'lname': 'Stark',
                'city': 'Winterfell',
                'house': 'Stark',
                'image': ntf
            }

            res = self.client.put(CUSTOMER_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        customer = Customer.objects.get(id=res.data['id'])
        for key in payload.keys():
            if key != 'image':
                self.assertEqual(payload[key], getattr(customer, key))

        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(customer.image.path))
        customer.image.delete()

    def test_partial_update_cuptomer(self):
        """Test updating customer with patch"""

        customer = sample_customer(user=self.user)

        payload = {
            'fname': 'Nad',
            'city': 'Moscow'
        }

        res = self.client.patch(CUSTOMER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        customer.refresh_from_db()

        self.assertEqual(customer.city, payload['city'])

    def test_full_update_customer(self):
        """Test recipe update with put"""
        # create customer with image
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)

            customer = sample_customer(user=self.user)
            customer.image.save('abc.jpg', ntf)

        # full update
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            payload = {
                'fname': 'Ned',
                'lname': 'Stark',
                'city': 'Balashiha',
                'house': 'Stark',
                'image': ntf
            }

            res = self.client.put(CUSTOMER_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        customer.refresh_from_db()

        self.assertEqual(customer.city, payload['city'])
        self.assertTrue(os.path.exists(customer.image.path))
        customer.image.delete()

        try:
            os.remove("/vol/web/media/upload/customer/abc.jpg")
        except Exception as e:
            if e:
                pass
