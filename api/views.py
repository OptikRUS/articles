from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser
from django_auto_prefetching import AutoPrefetchViewSetMixin

from api.models import Author, Article
from api.serializers import AuthorModelSerializer, ArticleModelSerializer, AdminAuthorModelSerializer, \
    AdminArticleModelSerializer, UnAuthArticleModelSerializer
from api.filters import ArticleFilter


class AuthorModelViewSet(AutoPrefetchViewSetMixin, ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer


class ArticleModelViewSet(AutoPrefetchViewSetMixin, ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
    filterset_class = ArticleFilter

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return ArticleModelSerializer
        return UnAuthArticleModelSerializer


class AdminAuthorsViewSet(AutoPrefetchViewSetMixin, ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AdminAuthorModelSerializer
    permission_classes = [IsAdminUser]


class AdminArticlesViewSet(AutoPrefetchViewSetMixin, ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = AdminArticleModelSerializer
    filterset_class = ArticleFilter
    permission_classes = [IsAdminUser]
