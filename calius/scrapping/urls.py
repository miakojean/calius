from django.urls import path
from . import views

urlpatterns = [
    path('', views.scrape_city, name='scrape_city'),
    path('search-facebook-ads/', views.search_facebook_ads, name='search_facebook_ads'),
    path('meta-test/', views.meta_test, name='meta_test'),
    path('test_business_api/', views.test_business_api, name='test_business_api')
]