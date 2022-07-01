import json
from uuid import uuid4
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APITestCase
from mixer.backend.django import mixer
from django.contrib.auth.models import User

from api.views import AdminAuthorsViewSet, AdminArticlesViewSet
from api.models import Author, Article
from users.models import User


class TestAuthorModelViewSet(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='django', email='django@ft.local', password='fortech')
        self.user = User.objects.create_user('test_user', 'test_user@ft.local', 'fortech')
        self.author = Author.objects.create(name='test_name', picture='https://www.test.com/')
        self.author_data = {"name": "test_name", "picture": "https://www.test.com/"}
        self.author_data_upd = {'name': 'test_name_upd', 'picture': 'https://www.test.upd.com/'}

    """List authors"""
    def test_get_list_guest(self):
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_auth(self):
        self.client.login(username='test_user', password='fortech')
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_admin(self):
        self.client.login(username='django', password='fortech')
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """Detail author"""
    def test_get_detail_author_for_guest(self):
        response = self.client.get(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_author_auth(self):
        self.client.force_login(user=self.user)
        response = self.client.get(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_author = json.loads(response.content)
        self.assertEqual(response_author['name'], 'test_name')
        self.assertEqual(response_author['picture'], 'https://www.test.com/')

    def test_get_detail_author_for_admin(self):
        self.client.force_login(user=self.superuser)
        response = self.client.get(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_author = json.loads(response.content)
        self.assertEqual(response_author['name'], 'test_name')
        self.assertEqual(response_author['picture'], 'https://www.test.com/')

    """Create author"""
    def test_create_author_for_guest(self):
        client = APIClient()
        response = client.post('/api/authors/', self.author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_author_for_admin(self):
        client = APIClient()
        response = client.post('/api/authors/', self.author_data, format='json')
        force_authenticate(response, user=self.superuser)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_author_for_user(self):
        client = APIClient()
        response = client.post('/api/authors/', self.author_data, format='json')
        force_authenticate(response, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    """Delete author"""
    def test_delete_author_for_guest(self):
        author = mixer.blend(Author)
        client = APIClient()
        response = client.delete(f'/api/authors/{author.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_author_for_admin(self):
        author = mixer.blend(Author)
        client = APIClient()
        client.login(username='django', password='fortech')
        response = client.delete(f'/api/authors/{author.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        client.logout()

    def test_delete_author_for_user(self):
        author = mixer.blend(Author)
        client = APIClient()
        client.login(username='test_user', password='fortech')
        response = client.delete(f'/api/authors/{author.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        client.logout()

    """Edit author"""
    def test_edit_author_for_guest(self):
        response = self.client.put(f'/api/authors/{self.author.id}/', self.author_data_upd)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_edit_author_for_admin(self):
        author = mixer.blend(Author)
        self.client.force_login(user=self.superuser)
        response = self.client.put(f'/api/authors/{author.id}/', self.author_data_upd, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_edit_author_for_user(self):
        author = mixer.blend(Author)
        self.client.force_login(user=self.user)
        response = self.client.put(f'/api/authors/{author.id}/', self.author_data_upd, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    """List authors for admin url"""
    def test_get_list_guest_admin_panel(self):
        response = self.client.get('/api/admin/authors/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_user_admin_panel(self):
        self.client.login(username='test_user', password='fortech')
        response = self.client.get('/api/admin/authors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_authors_admin_admin_panel(self):
        self.client.login(username='django', password='fortech')
        response = self.client.get('/api/admin/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """Detail author for admin url"""
    def test_get_detail_author_for_guest_admin_panel(self):
        response = self.client.get(f'/api/admin/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_author_user_admin_panel(self):
        self.client.force_login(user=self.user)
        response = self.client.get(f'/api/admin/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_detail_author_for_admin_admin_panel(self):
        self.client.force_login(user=self.superuser)
        response = self.client.get(f'/api/admin/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_author = json.loads(response.content)
        self.assertEqual(response_author['name'], 'test_name')
        self.assertEqual(response_author['picture'], 'https://www.test.com/')

    """Create author for admin url"""
    def test_create_author_for_guest_admin_panel(self):
        client = APIClient()
        response = client.post('/api/admin/authors/', self.author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_author_for_admin_admin_panel(self):
        factory = APIRequestFactory()
        request = factory.post('/api/admin/authors/', self.author_data, format='json')
        force_authenticate(request, user=self.superuser)
        view = AdminAuthorsViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_author_for_user_admin_panel(self):
        factory = APIRequestFactory()
        request = factory.post('/api/admin/authors/', self.author_data, format='json')
        force_authenticate(request, user=self.user)
        view = AdminAuthorsViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """Delete author for admin url"""
    def test_delete_author_for_guest_admin_panel(self):
        author = mixer.blend(Author)
        client = APIClient()
        response = client.delete(f'/api/admin/authors/{author.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_author_for_admin_admin_panel(self):
        author = mixer.blend(Author)
        client = APIClient()
        client.login(username='django', password='fortech')
        response = client.delete(f'/api/admin/authors/{author.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        client.logout()

    def test_delete_author_for_user_admin_panel(self):
        author = mixer.blend(Author)
        client = APIClient()
        client.login(username='test_user', password='fortech')
        response = client.delete(f'/api/admin/authors/{author.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        client.logout()

    """Edit author for admin url"""
    def test_edit_author_for_guest_admin_panel(self):
        response = self.client.put(f'/api/admin/authors/{self.author.id}/', self.author_data_upd)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_author_for_admin_admin_panel(self):
        author = mixer.blend(Author)
        self.client.force_login(user=self.superuser)
        response = self.client.put(f'/api/admin/authors/{author.id}/', self.author_data_upd, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_author_for_user_admin_panel(self):
        author = mixer.blend(Author)
        self.client.force_login(user=self.user)
        response = self.client.put(f'/api/admin/authors/{author.id}/', self.author_data_upd, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestArticleModelViewSet(APITestCase):
    def setUp(self):
        self.author_uid = uuid4()
        self.superuser = User.objects.create_superuser('django', 'django@ft.local', 'fortech')
        self.user = User.objects.create_user('test_user', 'test_user@ft.local', 'fortech')
        self.author = Author.objects.create(id=self.author_uid, name='test_name', picture='https://www.test.com/')
        self.author_data = {"id": self.author_uid, "name": "test_name", "picture": "https://www.test.com/"}
        self.author_data_upd = {'name': 'test_name_upd', 'picture': 'https://www.test.upd.com/'}
        self.article = Article.objects.create(
            author=self.author,
            category='test_category',
            title='test_title',
            summary='test_summary',
            first_paragraph='test_paragraph',
            body='test_body'
        )
        self.article_data = {
            'name': self.author_data['name'],
            'picture': self.author_data['picture'],
            'category': 'test_category',
            'title': 'test_title',
            'summary': 'test_summary',
            'first_paragraph': 'test_paragraph',
            'body': 'test_body',
        }

        self.article_data_upd = {
            'name': self.author_data_upd['name'],
            'picture': self.author_data_upd['picture'],
            'category': 'test_category_upd',
            'title': 'test_title_upd',
            'summary': 'test_summary_upd',
            'first_paragraph': 'test_paragraph_upd',
            'body': 'test_body_upd',
        }

    """List articles"""
    def test_get_list_guest(self):
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_auth(self):
        self.client.login(username='test_user', password='fortech')
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_admin(self):
        self.client.login(username='django', password='fortech')
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """Detail article"""
    def test_get_detail_article_for_guest(self):
        client = APIClient()
        response = client.get(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_article_for_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_article = json.loads(response.content)
        self.assertEqual(response_article['category'], 'test_category')
        self.assertEqual(response_article['title'], 'test_title')
        self.assertEqual(response_article['summary'], 'test_summary')
        self.assertEqual(response_article['firstParagraph'], 'test_paragraph')
        self.assertEqual(response_article['body'], 'test_body')

    def test_get_detail_article_for_admin(self):
        self.client.force_login(user=self.superuser)
        response = self.client.get(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_article = json.loads(response.content)
        self.assertEqual(response_article['category'], 'test_category')
        self.assertEqual(response_article['title'], 'test_title')
        self.assertEqual(response_article['summary'], 'test_summary')
        self.assertEqual(response_article['firstParagraph'], 'test_paragraph')
        self.assertEqual(response_article['body'], 'test_body')

    """Create article"""
    def test_create_article_for_guest(self):
        client = APIClient()
        response = client.post('/api/articles/', self.author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_article_for_admin(self):
        client = APIClient()
        response = client.post('/api/articles/', self.author_data, format='json')
        force_authenticate(response, user=self.superuser)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_article_for_user(self):
        client = APIClient()
        response = client.post('/api/articles/', self.author_data, format='json')
        force_authenticate(response, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    """Edit articles"""
    def test_edit_article_for_guest(self):
        client = APIClient()
        response = client.patch(f'/api/articles/{self.article.id}/', self.author_data_upd)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_edit_article_for_user(self):
        article = mixer.blend(Article)
        self.client.force_login(user=self.user)
        response = self.client.patch(f'/api/articles/{article.id}/', self.author_data_upd)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_edit_article_for_admin(self):
        article = mixer.blend(Article)
        self.client.force_login(user=self.superuser)
        response = self.client.patch(f'/api/articles/{article.id}/', self.author_data_upd)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    """Delete articles"""
    def test_delete_articles_for_guest(self):
        response = self.client.delete(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_articles_for_user(self):
        article = mixer.blend(Article)
        self.client.force_login(user=self.user)
        response = self.client.delete(f'/api/articles/{article.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_articles_for_admin(self):
        article = mixer.blend(Article)
        self.client.force_login(user=self.superuser)
        response = self.client.delete(f'/api/articles/{article.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    """List articles for admin url"""
    def test_get_list_guest_admin_panel(self):
        response = self.client.get('/api/admin/articles/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_user_admin_panel(self):
        self.client.login(username='test_user', password='fortech')
        response = self.client.get('/api/admin/articles/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_articles_for_admin_admin_panel(self):
        self.client.login(username='django', password='fortech')
        response = self.client.get('/api/admin/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """Detail article for admin url"""
    def test_get_detail_article_for_guest_admin_panel(self):
        response = self.client.get(f'/api/admin/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_article_user_admin_panel(self):
        self.client.force_login(user=self.user)
        response = self.client.get(f'/api/admin/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_detail_article_for_admin_admin_panel(self):
        self.client.force_login(user=self.superuser)
        response = self.client.get(f'/api/admin/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_article = json.loads(response.content)
        self.assertEqual(response_article['category'], 'test_category')
        self.assertEqual(response_article['title'], 'test_title')
        self.assertEqual(response_article['summary'], 'test_summary')
        self.assertEqual(response_article['firstParagraph'], 'test_paragraph')
        self.assertEqual(response_article['body'], 'test_body')

    """Create article for admin url"""
    def test_create_article_for_guest_admin_panel(self):
        client = APIClient()
        response = client.post('/api/admin/articles/', self.article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_article_for_user_admin_panel(self):
        factory = APIRequestFactory()
        request = factory.post('/api/admin/articles/', self.author_data, format='json')
        force_authenticate(request, user=self.user)
        view = AdminArticlesViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_article_for_admin_admin_panel(self):
        article = mixer.blend(Article)
        self.client.force_login(user=self.superuser)
        response = self.client.post(f'/api/articles/{article.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    """Delete article for admin url"""
    def test_delete_article_for_guest_admin_panel(self):
        article = mixer.blend(Article)
        client = APIClient()
        response = client.delete(f'/api/admin/articles/{article.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_article_for_admin_admin_panel(self):
        article = mixer.blend(Article)
        client = APIClient()
        client.login(username='django', password='fortech')
        response = client.delete(f'/api/admin/articles/{article.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        client.logout()

    def test_delete_article_for_user_admin_panel(self):
        article = mixer.blend(Author)
        client = APIClient()
        client.login(username='test_user', password='fortech')
        response = client.delete(f'/api/admin/articles/{article.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        client.logout()

    """Edit article for admin url"""
    def test_edit_article_for_guest_admin_panel(self):
        response = self.client.put(f'/api/admin/articles/{self.article.id}/', self.author_data_upd)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_article_for_admin_admin_panel(self):
        article = mixer.blend(Article)
        self.client.force_login(user=self.superuser)
        response = self.client.put(f'/api/articles/{article.id}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_edit_article_for_user_admin_panel(self):
        article = mixer.blend(Article)
        self.client.force_login(user=self.user)
        response = self.client.put(f'/api/admin/articles/{article.id}/', self.article_data_upd, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
