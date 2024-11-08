from django.urls import path
from . import views

urlpatterns = [
    path('', views.scrape_city, name='scrape_city'),
]