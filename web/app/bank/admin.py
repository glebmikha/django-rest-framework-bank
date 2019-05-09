from django.contrib import admin

from bank.models import Customer, Account

admin.site.register(Customer)
admin.site.register(Account)
