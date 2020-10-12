import datetime

from django.core.management.base import BaseCommand
from url_api.models import URL

class Command(BaseCommand):
    """This command will delete all urls which have expired on the current day, or sooner"""
    help = 'Deletes expired urls from the database'

    def handle(self, *args, **kwargs):
        for url in URL.objects.all():
            expire_date = url.expired
            if expire_date <= datetime.date.today():
                url.delete()
                url.save()
