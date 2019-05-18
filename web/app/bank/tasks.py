from celery import shared_task
from bank.services import make_interest


@shared_task
def hello():
    print("Hello there!")


@shared_task
def call_make_interest():
    make_interest()
