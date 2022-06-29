from uuid import uuid4

from django.db import models


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=128)
    picture = models.URLField()


"""
{
  "id": "39df53da-542a-3518-9c19-3568e21644fe",
  "author": {
    "id": "2d460e48-a4fa-370b-a2d0-79f2f601988c",
    "name": "Author Name",
    "picture": "https://picture.url"
  },
  "category": "Category",
  "title": "Article title",
  "summary": "This is a summary of the article",
  "firstParagraph": "<p>This is the first paragraph of this article</p>",
  "body": "<div><p>Second paragraph</p><p>Third paragraph</p></div>"
}
"""