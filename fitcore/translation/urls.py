from django.urls import path
from . import views

app_name = 'translation'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_translation, name='add_translation'),
    path('edit/<int:pk>/', views.edit_translation, name='edit_translation'),
    path('delete/<int:pk>/', views.delete_translation, name='delete_translation'),
    path('api/translate/', views.translate_text, name='translate_text'),
]
