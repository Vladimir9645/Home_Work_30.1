from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonListApiView,
    LessonDetailApiView,
    index,
)

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('', index, name='index'),
    path('lessons/', LessonListApiView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetailApiView.as_view(), name='lesson-detail'),
] + router.urls
