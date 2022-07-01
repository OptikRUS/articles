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

    def create(self, validated_data):
        data = validated_data
        author_name = Author.objects.get_or_create(name=data['author']['name'])
        author_picture = Author.objects.get_or_create(name=data['author']['picture'])
        if author_name:
            author = author_name
        elif author_picture:
            author = author_picture
        else:
            author = Author.objects.get_or_create(id=data['author']['id'])

        article = Article.objects.create(
            author=author[0],
            category=data['category'],
            title=data['title'],
            summary=data['summary'],
            first_paragraph=data['first_paragraph'],
            body=data['body'],)
        return article

    def update(self, instance, validated_data):
        data = validated_data
        author_name = Author.objects.get_or_create(name=data['author']['name'])
        author_picture = Author.objects.get_or_create(name=data['author']['picture'])
        if author_name:
            author = author_name
        elif author_picture:
            author = author_picture
        else:
            author = Author.objects.get_or_create(id=data['author']['id'])

        article = Article.objects.create(
            author=author[0],
            category=data['category'],
            title=data['title'],
            summary=data['summary'],
            first_paragraph=data['first_paragraph'],
            body=data['body'],)
        return article

    class Meta:
        model = Article
        fields = '__all__'
