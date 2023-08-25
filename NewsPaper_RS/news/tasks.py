from celery import shared_task
from django.core.mail import send_mail
import datetime
from news.models import Post, Category
from django.conf import settings
from django.template.loader import render_to_string


@shared_task
def last_week_news():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_date_time__gte=last_week)
    categories = set(posts.values_list('category__category_name', flat=True))
    subscribers = set(
        Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    send_mail(
        "Статьи за неделю в вашей любимой категории",
        html_content,
        settings.DEFAULT_FROM_EMAIL,
        subscribers,
        fail_silently=False,
    )


@shared_task
def article_creation_notice(preview, pk, post_title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    send_mail(
        post_title,
        html_content,
        settings.DEFAULT_FROM_EMAIL,
        subscribers,
        fail_silently=False,
    )
