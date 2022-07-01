from rest_framework.serializers import ModelSerializer

from api.models import Author, Article


class AuthorModelSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class ArticleModelSerializer(ModelSerializer):
    author = AuthorModelSerializer()

    class Meta:
        model = Article
        fields = '__all__'


class UnAuthArticleModelSerializer(ModelSerializer):
    author = AuthorModelSerializer()

    class Meta:
        model = Article
        exclude = ('body', )


class AdminAuthorModelSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AdminArticleModelSerializer(ModelSerializer):
    author = AuthorModelSerializer()

    class Meta:
        model = Article
        fields = '__all__'
