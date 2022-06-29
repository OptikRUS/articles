from django.core.management.base import BaseCommand
from django.db import transaction

import factory
from factory.django import DjangoModelFactory

from api.models import Article, Author


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Article

    author = factory.Iterator([i for i in Author.objects.all()])
    category = factory.Faker('word')
    title = factory.Faker('sentence', nb_words=4)
    summary = factory.Faker('text')
    first_paragraph = factory.Faker('text')
    body = factory.Faker('text')


class Command(BaseCommand):
    help = 'Create articles'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old articles data...")
        Article.objects.all().delete()
        count = options['count']
        self.stdout.write("Creating new articles...")

        for _ in range(count):
            article = AuthorFactory()
            print(f'Article "{article.title}" with category {article.category} added')
        print('Done!')
