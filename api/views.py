from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser

from api.models import Author, Article
from api.serializers import AuthorModelSerializer, ArticleModelSerializer, AdminAuthorModelSerializer, \
    AdminArticleModelSerializer, UnAuthArticleModelSerializer
from api.filters import ArticleFilter


class AuthorModelViewSet(ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer


class ArticleModelViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
    filterset_class = ArticleFilter

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return ArticleModelSerializer
        return UnAuthArticleModelSerializer


class AdminAuthorsViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AdminAuthorModelSerializer
    permission_classes = [IsAdminUser]


class AdminArticlesViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = AdminArticleModelSerializer
    filterset_class = ArticleFilter
    permission_classes = [IsAdminUser]
