from django.urls import path
from .views import NewsList, NewsDetail, SearchNewsList, PostCreate, PostUpdate, PostDelete, logout_user, \
    IndexView, upgrade_me, CategoryListView, subscribe
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/search/', SearchNewsList.as_view(), name='search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit', PostUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('article/create/', PostCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit', PostUpdate.as_view(), name='article_edit'),
    path('article/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
    # path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('user_page/', IndexView.as_view(template_name="user_page.html"), name='user_page'),
    path('logout/user', logout_user, name='logout_user'),
    path('upgrade/', upgrade_me, name='upgrade_status'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe')
]
