from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('category/<slug:category_slug>/', views.category_view, name='category'),
    path('<slug:post_slug>/', views.blog_detail, name='blog_detail'),
]
