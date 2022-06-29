from django.core.management.base import BaseCommand
from django.db import transaction

import factory
from factory.django import DjangoModelFactory

from api.models import Author


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker('name')
    picture = factory.Faker('url')


class Command(BaseCommand):
    help = 'Create authors'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old authors data...")
        Author.objects.all().delete()
        count = options['count']
        self.stdout.write("Creating new authors...")

        for _ in range(count):
            author = AuthorFactory()
            print(f'Author "{author.name}" added')
        print('Done!')
