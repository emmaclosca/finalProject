from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

# Unit testing
class PostTestCase(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(title="Test Post", content="This is a test post", author=self.user, is_blog_post=True)
        self.client = Client()

    def test_like_view_toggle_like(self):
        # Test case for toggling a like on a post:
        # Log in with the user created in setUp
        self.client.login(username='testuser', password='12345')
        # Make a GET request to the like post URL and pass the post's primary key
        response = self.client.get(reverse('likePosts', args=[self.post.pk]))
        self.post.refresh_from_db()
        # Assert that the user's like is present 
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())
        self.assertEqual(response.status_code, 302)

    def test_index_view_only_blog_posts(self):
        # Ensure that the IndexView only returns blog posts:
        # Make a GET request to the index URL
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        expected_format = f'{self.post.title} | {self.post.author.username}'
        self.assertQuerysetEqual(response.context['blog_post'], [expected_format], transform=str)

    def test_add_post_form_valid(self):
        self.client.login(username='testuser', password='12345')
        # Make a POST request to add a new post and check if the form is processed correctly
        response = self.client.post(reverse('addPost'), {
            'title': 'New Post',
            'content': 'Content of the new post',
            'is_blog_post': True
        })
        # This indicates a successful post creation and redirection
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 2)

# System testing
class SystemTests(TestCase):
    def test_like_and_unlike_post(self):
        user = User.objects.create_user(username='testuser2', password='54321')
        post = Post.objects.create(title="Test Like", content="Test like content", author=user, is_blog_post=True)
        self.client.login(username='testuser2', password='54321')

        # Like the post
        response = self.client.get(reverse('likePosts', args=[post.id]), follow=True)
        self.assertEqual(post.likes.count(), 1)  # Like is added

        # Unlike the post
        response = self.client.get(reverse('likePosts', args=[post.id]), follow=True)
        self.assertEqual(post.likes.count(), 0)  # Like is removed

    def test_homepage_accessibility(self):
        # URL for the homepage
        homepage_url = reverse('index')
        
        # Make a GET request to the homepage
        response = self.client.get(homepage_url)
        
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
      