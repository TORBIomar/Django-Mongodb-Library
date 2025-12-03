from django.core.management.base import BaseCommand
from db import books_col


class Command(BaseCommand):
    help = 'Create a MongoDB text index on title, authors and publisher fields (useful for full-text search)'

    def handle(self, *args, **options):
        # Create a text index; if it exists, create_index is idempotent
        idx_name = books_col.create_index([
            ('title', 'text'),
            ('authors', 'text'),
            ('publisher', 'text')
        ], default_language='english')
        self.stdout.write(self.style.SUCCESS(f'Created/ensured text index: {idx_name}'))
