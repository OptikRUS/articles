from rest_framework.viewsets import ModelViewSet

from api.models import Author, Article
from api.serializers import AuthorModelSerializer, ArticleModelSerializer


class AuthorModelViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer


class ArticleModelViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
