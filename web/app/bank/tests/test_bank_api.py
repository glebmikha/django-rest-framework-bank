
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

CUSTOMER_URL = reverse('bank:customer-list')


def image_upload_url(recipe_id):
    """Return url for recipe image upload"""
    return reverse('recipe:recipe-upload-image', args=[recipe_id])


def detail_url(recipe_id):
    """Return recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


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

    def test_auth_required(self):
        """Test that authentication is required"""
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
        self.assertEqual(res.data, serializer.data)

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
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    # find best prictices for creating profile tables w/ drf

    def test_create_basic_customer(self):
        """Test creating customer"""
        payload = {
            'fname': 'Ned',
            'lname': 'Stark',
            'city': 'Winterfell',
            'house': 'Stark',

        }
        res = self.client.post(CUSTOMER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        customer = Customer.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(customer, key))

    # def test_create_recipe_with_tags(self):
    #     """Test creating a recipe with tags"""
    #     tag1 = sample_tag(user=self.user, name='Tag 1')
    #     tag2 = sample_tag(user=self.user, name='Tag 2')
    #     payload = {
    #         'title': 'Test recipe with two tags',
    #         'tags': [tag1.id, tag2.id],
    #         'time_minutes': 30,
    #         'price': 10.00
    #     }
    #     res = self.client.post(RECIPE_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     recipe = Recipe.objects.get(id=res.data['id'])
    #     tags = recipe.tags.all()
    #     self.assertEqual(tags.count(), 2)
    #     self.assertIn(tag1, tags)
    #     self.assertIn(tag2, tags)

    # def test_create_recipe_with_ingredients(self):
    #     """Test creating recipe with ingredients"""
    #     ingredient1 = sample_ingridient(user=self.user, name='Ingredient 1')
    #     ingredient2 = sample_ingridient(user=self.user, name='Ingredient 2')
    #     payload = {
    #         'title': 'Test recipe with ingredients',
    #         'ingredients': [ingredient1.id, ingredient2.id],
    #         'time_minutes': 45,
    #         'price': 15.00
    #     }

    #     res = self.client.post(RECIPE_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     recipe = Recipe.objects.get(id=res.data['id'])
    #     ingredients = recipe.ingredients.all()
    #     self.assertEqual(ingredients.count(), 2)
    #     self.assertIn(ingredient1, ingredients)
    #     self.assertIn(ingredient2, ingredients)

    # def test_partial_update_recipe(self):
    #     """Test updating recipe with patch"""
    #     recipe = sample_recipe(user=self.user)
    #     recipe.tags.add(sample_tag(user=self.user))

    #     new_tag = sample_tag(user=self.user, name='Carry')

    #     payload = {
    #         'title': 'Chiken tikka',
    #         'tags': [new_tag.id]
    #     }

    #     url = detail_url(recipe.id)

    #     self.client.patch(url, payload)

    #     recipe.refresh_from_db()

    #     self.assertEqual(recipe.title, payload['title'])

    #     tags = recipe.tags.all()
    #     self.assertEqual(len(tags), 1)

    #     self.assertIn(new_tag, tags)

    # def test_full_update_recipe(self):
    #     """Test recipe update with put"""
    #     recipe = sample_recipe(user=self.user)
    #     recipe.tags.add(sample_tag(user=self.user))
    #     payload = {
    #         'title': 'Spagetti carbonara',
    #         'time_minutes': 25,
    #         'price': 5.00
    #     }

    #     url = detail_url(recipe.id)

    #     self.client.put(url, payload)

    #     recipe.refresh_from_db()

    #     self.assertEqual(recipe.title, payload['title'])
    #     self.assertEqual(recipe.time_minutes, payload['time_minutes'])
    #     self.assertEqual(recipe.price, payload['price'])
    #     tags = recipe.tags.all()
    #     self.assertEqual(len(tags), 0)
