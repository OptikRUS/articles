from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from api.models import Article


class ArticleFilter(FilterSet):
    category = CharFilter(lookup_expr='contains')

    class Meta:
        model = Article
        fields = ['category']
