"""Module for create custom schema."""
import os

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    """Create companies_schema schema in the database if it doesn't exist."""

    help = 'Create companies_schema schema in the database'

    def handle(self, *args, **kwargs):
        """
        Execute the command to create the schema.

        Args:
            args: args.
            kwargs: kwargs.

        """
        sql_path = os.path.join(os.path.dirname(__file__), '../../../create_companies_schema.sql')
        with open(sql_path, 'r') as sql_file:
            sql = sql_file.read()

        with connection.cursor() as cursor:
            cursor.execute(sql)

        self.stdout.write(self.style.SUCCESS('Successfully created companies_schema schema'))
