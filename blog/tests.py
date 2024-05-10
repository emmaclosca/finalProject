from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Category

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some test categories
        self.general_category = Category.objects.create(name='General')
        self.educational_category = Category.objects.create(name='Educational')

        # Create some test posts
        self.blog_post = Post.objects.create(title='Test Blog Post', content='Test content', author=self.user, category=self.general_category, is_blog_post=True)
        self.forum_post = Post.objects.create(title='Test Forum Post', content='Test content', author=self.user, category=self.general_category, is_blog_post=False)

    # def test_index_view_authenticated(self):
    #     client = Client()
    #     client.force_login(self.user)
    #     response = client.get(reverse('index'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Welcome, testuser')

    # def test_index_view_unauthenticated(self): 
    #     client = Client()
    #     response = client.get(reverse('index'))
    #     self.assertEqual(response.status_code, 302)  # Redirects to sign up page for unauthenticated users

    def test_blog_view(self):
        client = Client()
        response = client.get(reverse('blogContent', kwargs={'pk': self.blog_post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Blog Post')

    def test_forum_view(self):
        client = Client()
        response = client.get(reverse('forumDetail', kwargs={'pk': self.forum_post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Forum Post')



