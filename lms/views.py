from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsModer, IsOwner
from lms.paginators import LmsPagination
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, CourseDetailSerializer, LessonSerializer


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
    """CRUD курсов с разграничением прав."""
    serializer_class = CourseSerializer
    pagination_class = LmsPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        if self.request.user.is_authenticated:
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.none()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = (IsAuthenticated, ~IsModer)
        elif self.action == 'destroy':
            permission_classes = (IsAuthenticated, IsOwner)
        elif self.action in ('update', 'partial_update'):
            permission_classes = (IsAuthenticated, IsModer | IsOwner)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListApiView(generics.ListCreateAPIView):
    """GET (список) и POST (создание)."""
    serializer_class = LessonSerializer
    pagination_class = LmsPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        if self.request.user.is_authenticated:
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.none()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), (~IsModer)()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT/PATCH, DELETE одной сущности."""
    serializer_class = LessonSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsOwner()]
        if self.request.method in ('PUT', 'PATCH'):
            return [IsAuthenticated(), (IsModer | IsOwner)()]
        return [IsAuthenticated()]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
        return Response({'message': message})
