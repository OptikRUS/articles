from uuid import uuid4

from django.db import models


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=128)
    picture = models.URLField()


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    author = models.ForeignKey(Author, models.CASCADE)
    category = models.CharField(max_length=32)
    title = models.CharField(max_length=128)
    summary = models.TextField()
    first_paragraph = models.TextField()
    body = models.TextField()
