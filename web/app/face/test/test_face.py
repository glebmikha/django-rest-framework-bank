from django.test import TestCase
from django.test import Client
from django.urls import reverse
from face.models import Url, BoundingBox


class FaceTest(TestCase):
    """Test our app"""

    def setUp(self):
        self.client = Client()

    def test_delete_item(self):
        """Test deleting Url with bounding box"""
        url = Url.objects.create(image_url='http://www.gleb.ru/picture.jpg')
        BoundingBox.objects.create(top=1, bottom=1, right=1, left=1, image=url)

        urls = Url.objects.all()
        bbs = BoundingBox.objects.all()     

        self.client.get(reverse('delete', kwargs={'url_id': url.id}))
        urls = Url.objects.all()
        bbs = BoundingBox.objects.all()

        self.assertEqual(len(urls), 0)
        self.assertEqual(len(bbs), 0)
