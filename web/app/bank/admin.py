from django.contrib import admin

from bank.models import Customer, Account, Action, Transaction

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Action)
admin.site.register(Transaction)
