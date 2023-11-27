"""
djangpo command to wait for db to be available
"""
import time

from psycopg2 import OperationalError as Psycopg2Error


from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """EntryPoint for Command."""
        self.stdout.write("wait for connection to database")
        db_up =False

        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except(Psycopg2Error,OperationalError):
                self.stdout.write('cant connect to database, retry in 1 seconde')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Connection Established with Database'))
        