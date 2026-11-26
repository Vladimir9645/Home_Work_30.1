from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User
from django.contrib.auth.models import Group


class LmsBaseTestCase(APITestCase):
    def setUp(self):
        self.moder_group, _ = Group.objects.get_or_create(name='moderators')
        self.owner = User.objects.create_user(email='owner@example.com', password='pass12345')
        self.other = User.objects.create_user(email='other@example.com', password='pass12345')
        self.moderator = User.objects.create_user(email='moder@example.com', password='pass12345')
        self.moderator.groups.add(self.moder_group)

        self.course = Course.objects.create(title='Курс 1', owner=self.owner)
        self.lesson = Lesson.objects.create(
            title='Урок 1',
            video_link='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            course=self.course,
            owner=self.owner,
        )
        self.foreign_course = Course.objects.create(title='Чужой курс', owner=self.other)

    def auth(self, user):
        self.client.force_authenticate(user=user)


class LessonCrudTests(LmsBaseTestCase):
    def test_anonymous_get_lessons(self):
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, 401)

    def test_owner_can_create_lesson(self):
        self.auth(self.owner)
        response = self.client.post('/api/lessons/', {
            'title': 'Новый урок',
            'video_link': 'https://www.youtube.com/watch?v=abc',
            'course': self.course.pk,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_youtube_only_validation(self):
        self.auth(self.owner)
        response = self.client.post('/api/lessons/', {
            'title': 'Плохой урок',
            'video_link': 'https://vimeo.com/12345',
            'course': self.course.pk,
        })
        self.assertEqual(response.status_code, 400)

    def test_owner_cannot_edit_foreign_lesson(self):
        self.auth(self.owner)
        response = self.client.patch(f'/api/lessons/{self.lesson.pk}/', {'title': 'Взломано'})
        self.assertEqual(response.status_code, 200)  # свой урок — можно
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Взломано')

    def test_owner_cannot_see_foreign_course(self):
        self.auth(self.owner)
        response = self.client.get(f'/api/courses/{self.foreign_course.pk}/')
        self.assertEqual(response.status_code, 404)

    def test_owner_cannot_delete_foreign_course(self):
        self.auth(self.owner)
        response = self.client.delete(f'/api/courses/{self.foreign_course.pk}/')
        self.assertEqual(response.status_code, 404)

    def test_owner_can_delete_own_lesson(self):
        self.auth(self.owner)
        response = self.client.delete(f'/api/lessons/{self.lesson.pk}/')
        self.assertEqual(response.status_code, 204)


class ModeratorTests(LmsBaseTestCase):
    def test_moderator_sees_all_courses(self):
        self.auth(self.moderator)
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_moderator_can_edit_foreign_course(self):
        self.auth(self.moderator)
        response = self.client.patch(
            f'/api/courses/{self.foreign_course.pk}/', {'description': 'Правка'},
        )
        self.assertEqual(response.status_code, 200)

    def test_moderator_cannot_create_course(self):
        self.auth(self.moderator)
        response = self.client.post('/api/courses/', {'title': 'Новый курс'})
        self.assertEqual(response.status_code, 403)

    def test_moderator_cannot_delete_course(self):
        self.auth(self.moderator)
        response = self.client.delete(f'/api/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, 403)

class SubscriptionTests(LmsBaseTestCase):
    def test_subscribe_toggle(self):
        self.auth(self.owner)
        response = self.client.post('/api/subscriptions/', {'course_id': self.course.pk})
        self.assertEqual(response.json()['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.owner, course=self.course).exists())

        response = self.client.post('/api/subscriptions/', {'course_id': self.course.pk})
        self.assertEqual(response.json()['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.owner, course=self.course).exists())

    def test_is_subscribed_flag_in_detail(self):
        self.auth(self.owner)
        Subscription.objects.create(user=self.owner, course=self.course)
        response = self.client.get(f'/api/courses/{self.course.pk}/')
        self.assertEqual(response.json()['is_subscribed'], True)

    def test_subscription_requires_auth(self):
        response = self.client.post('/api/subscriptions/', {'course_id': self.course.pk})
        self.assertEqual(response.status_code, 401)

class PublicProfileTests(APITestCase):
    def setUp(self):
        self.me = User.objects.create_user(email='me@example.com', password='pass12345')
        self.stranger = User.objects.create_user(
            email='stranger@example.com', password='pass12345', last_name='Чужая фамилия',
        )

    def test_foreign_profile_hides_private_fields(self):
        self.client.force_authenticate(user=self.me)
        response = self.client.get(f'/api/users/profile/{self.stranger.pk}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertNotIn('email', data)
        self.assertNotIn('last_name', data)

    def test_foreign_profile_edit_forbidden(self):
        self.client.force_authenticate(user=self.me)
        response = self.client.patch(
            f'/api/users/profile/{self.stranger.pk}/', {'first_name': 'Хакер'},
        )
        self.assertEqual(response.status_code, 403)
