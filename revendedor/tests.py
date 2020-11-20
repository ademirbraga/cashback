from django.test import TestCase
from .models import Revendedor
from .serializers import RevendedorSerializer
import unittest

from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from .views import RevendedorViewSet

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.attributes = {
            'npme': 'Joao Silva',
            'cpf': '24795044090',
            'email': 'joao@silva.com',
            'senha': '123456'
        }

        self.serializer_data = {
            'npme': 'Joao Silva',
            'cpf': '24795044090',
            'email': 'joao@silva.com',
            'senha': '123456'
        }

        self.revendedor = Revendedor.objects.create(**self.attributes)
        self.serializer = RevendedorSerializer(instance=self.revendedor)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/customer/details')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        # response = my_view(request)
        # Use this syntax for class-based views.
        response = RevendedorViewSet.as_view()(request)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()