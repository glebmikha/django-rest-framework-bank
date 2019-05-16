from .models import Account, Transfer
from django.db import transaction


def make_transfer(from_account, to_account, amount):

    if from_account.balance < amount:
        raise(ValueError('Not enough money'))

    with transaction.atomic():
        from_account.balance -= amount
        from_account.save()

        to_account.balance += amount
        to_account.save()

        transfer = Transfer.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )

    return transfer


def filter_user_account(user, account_id):
    try:
        account = Account.objects.filter(
            user=user).get(pk=account_id)
    except Exception as e:
        print(e)
        raise(ValueError('No such account'))

    return account


def check_account_exists(account_id):
    try:
        account = Account.objects.get(pk=account_id)
    except Exception as e:
        print(e)
        raise(ValueError('No such account'))

    return account
