from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tweets', views.TweetViewSet, basename='tweet')
# router.register(r'tweets', views.feed, basename='tweet')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.feed, name='feed'),
    path('trending/', views.trending, name='trending'),
]