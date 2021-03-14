from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

"""for view set"""
router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name = 'hello-viewset')
router.register('profile', views.UserProfileViewSet)
"""We have provided queryset object under views.py ModelViewSet class"""

urlpatterns = [
            path('hello-view/', views.HelloAPIView.as_view()),
            path('login/', views.UserLoginApiView.as_view()),
            path('', include(router.urls))
]
