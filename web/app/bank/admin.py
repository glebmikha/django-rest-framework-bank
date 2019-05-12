from django.contrib import admin

from bank.models import Customer, Account, Action

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Action)
