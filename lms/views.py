from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from django.http import HttpResponse


def index(request):
    return HttpResponse("""
        <h1>LMS API Ready</h1>
        <p>Доступные эндпоинты:</p>
        <ul>
            <li><a href="/admin/">Админка Django</a></li>
            <li><a href="/api/courses/">Курсы (DRF)</a></li>
            <li><a href="/api/lessons/">Уроки (DRF)</a></li>
        </ul>
    """)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListApiView(generics.ListCreateAPIView):
    """GET (список) и POST (создание)."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT/PATCH, DELETE одной сущности."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
