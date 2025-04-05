from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog-details/', views.blog_details, name='blog_details'),
    path('class-details/', views.class_details, name='class_details'),
    path('class-schedule/', views.class_schedule, name='class_schedule'),
    path('classes/', views.classes, name='classes'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_handler, name='contact_handler'),
    path('gallery/', views.gallery, name='gallery'),
    path('pricing/', views.pricing, name='pricing'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('trainers/', views.trainers, name='trainers'),
]
