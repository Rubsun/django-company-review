import os
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create companies_schema schema in the database'

    def handle(self, *args, **kwargs):
        sql_path = os.path.join(os.path.dirname(__file__), '../../../create_companies_schema.sql')
        with open(sql_path, 'r') as file:
            sql = file.read()

        with connection.cursor() as cursor:
            cursor.execute(sql)
        
        self.stdout.write(self.style.SUCCESS('Successfully created companies_schema schema'))
