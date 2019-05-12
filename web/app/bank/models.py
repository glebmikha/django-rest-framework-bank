from django.db import models
from django.conf import settings
import uuid
import os


def customer_image_file_path(instande, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('upload/customer/', filename)


class Customer(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=customer_image_file_path)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.fname} {self.lname}'


class Account(models.Model):
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT  # we cannot delete user with money
    )

    def __str__(self):
        return f'Balance is {str(self.balance)}'


class Action(models.Model):
    amount = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    date = models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'Account number {self.account.id} ' +\
            f'was changed on {str(self.amount)}'
