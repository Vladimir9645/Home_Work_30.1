from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Payment, User
from lms.models import Course


def get_jwt(user):
    return {'HTTP_AUTHORIZATION': 'Bearer ' + str(RefreshToken.for_user(user).access_token)}


class RegistrationTests(APITestCase):
    def test_registration(self):
        response = self.client.post('/api/users/register/', {
            'email': 'new@example.com',
            'password': 'StroN9pa$$',
            'first_name': 'Новый',
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email='new@example.com').exists())

    def test_token_obtain(self):
        User.objects.create_user(email='me@example.com', password='pass12345')
        response = self.client.post('/api/users/token/', {
            'email': 'me@example.com', 'password': 'pass12345',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

    def test_wrong_password(self):
        User.objects.create_user(email='me@example.com', password='pass12345')
        response = self.client.post('/api/users/token/', {
            'email': 'me@example.com', 'password': 'wrong',
        })
        self.assertEqual(response.status_code, 401)


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='me@example.com', password='pass12345')
        self.other = User.objects.create_user(email='other@example.com', password='pass12345')

    def test_own_profile(self):
        self.client.credentials(**get_jwt(self.user))
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], 'me@example.com')

    def test_profile_requires_auth(self):
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, 401)


class PaymentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='me@example.com', password='pass12345')
        self.other = User.objects.create_user(email='other@example.com', password='pass12345')
        course = Course.objects.create(title='Курс', owner=self.other)
        Payment.objects.create(
            user=self.user, paid_course=course, amount='1000.00', payment_method='cash',
        )
        Payment.objects.create(
            user=self.other, paid_course=course, amount='5000.00', payment_method='transfer',
        )

    def test_sees_only_own_payments(self):
        self.client.credentials(**get_jwt(self.user))
        response = self.client.get('/api/users/payments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)

    def test_filter_by_method(self):
        self.client.credentials(**get_jwt(self.user))
        response = self.client.get('/api/users/payments/?payment_method=cash')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)
