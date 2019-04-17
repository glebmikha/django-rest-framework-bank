from django.db import models


class Url(models.Model):
    image_url = models.CharField(max_length=255)
