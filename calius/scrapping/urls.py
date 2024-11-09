from django.urls import path
from . import views

urlpatterns = [
    path('', views.scrape_city, name='scrape_city'),
    path('search-facebook-ads/', views.search_facebook_ads, name='search_facebook_ads'),
]