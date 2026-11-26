import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from lms.models import Course, Lesson
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает тестовые платежи'

    def handle(self, *args, **kwargs):
        users = list(User.objects.all())
        courses = list(Course.objects.all())
        lessons = list(Lesson.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR('Нет пользователей — сначала создайте их'))
            return

        for i in range(10):
            obj = random.choice(courses + lessons)
            Payment.objects.create(
                user=random.choice(users),
                payment_date=timezone.now() - timedelta(days=i),
                paid_course=obj if isinstance(obj, Course) else None,
                paid_lesson=obj if isinstance(obj, Lesson) else None,
                amount=random.choice([500, 1000, 1500, 3000, 5000]),
                payment_method=random.choice(['cash', 'transfer']),
            )
        self.stdout.write(self.style.SUCCESS('Платежи созданы'))
