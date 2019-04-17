from django.contrib import admin
from . import models

admin.site.register(models.Url)
admin.site.register(models.BoundingBox)
