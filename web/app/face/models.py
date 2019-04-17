from django.db import models


class Url(models.Model):
    image_url = models.CharField(max_length=255)


class BoundingBox(models.Model):
    top = models.DecimalField(decimal_places=3, max_digits=5)
    right = models.DecimalField(decimal_places=3, max_digits=5)
    bottom = models.DecimalField(decimal_places=3, max_digits=5)
    left = models.DecimalField(decimal_places=3, max_digits=5)
    image = models.ForeignKey(Url, on_delete=models.CASCADE)
