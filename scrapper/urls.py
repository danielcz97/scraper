from django.urls import path
from .views import fetch_categories

urlpatterns = [
    path('fetch-categories/', fetch_categories, name='fetch_categories'),
]
