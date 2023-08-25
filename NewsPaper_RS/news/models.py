from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class Author(models.Model):
    author_rating = models.IntegerField(default=0)
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username

    def update_rating(self):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(
            posts_rating_sum=Coalesce(Sum('post_rating'), 0))['posts_rating_sum']
        author_comments_rating = Comment.objects.filter(user_id=self.author).aggregate(
            comments_rating_sum=Coalesce(Sum('comment_rating'), 0))['comments_rating_sum']
        comments_rating_to_author_posts = Comment.objects.filter(post__author__author=self.author).aggregate(
            comments_rating_to_posts_sum=Coalesce(Sum('comment_rating'), 0))['comments_rating_to_posts_sum']

        self.author_rating = author_posts_rating * 3 + author_comments_rating + comments_rating_to_author_posts
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.category_name


class Post(models.Model):
    article = 'AR'
    news = 'NW'

    POST_TYPE = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    post_type = models.CharField(max_length=2,
                                 choices=POST_TYPE)
    post_date_time = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    category = models.ManyToManyField('Category', through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:125] + '...'

    def __str__(self):
        return f'{self.post_title.title()}: {self.post_text[:20]}... (Автор: {self.author})'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('CATEGORY', on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = models.TextField()
    comment_date_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
