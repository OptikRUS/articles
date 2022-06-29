from rest_framework.viewsets import ModelViewSet

from api.models import Author
from api.serializers import AuthorModelSerializer


class AuthorModelViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer
