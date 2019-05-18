from django.contrib import admin

from bank.models import (Customer, Account,
                         Action, Transaction,
                         Transfer, Interest)

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Action)
admin.site.register(Transaction)
admin.site.register(Transfer)
admin.site.register(Interest)
