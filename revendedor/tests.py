from django.test import TestCase
from .models import Revendedor
from .serializers import RevendedorSerializer
import unittest

from django.contrib.auth.models import User
from django.test import RequestFactory

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from rest_framework.test import APITestCase, force_authenticate
from rest_framework.test import APIRequestFactory

from .views import RevendedorViewSet

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.attributes = {
            'nome': 'Joao Silva',
            'cpf': '24795044090',
            'email': 'joao@silva.com',
            'senha': '123456'
        }

        self.serializer_data = {
            'nome': 'Joao Silva',
            'cpf': '24795044090',
            'email': 'joao@silva.com',
            'senha': '123456'
        }
        revendedor1 = Revendedor.objects.filter(cpf='24795044090')
        if revendedor1:
            revendedor1[0].delete()
        self.revendedor = Revendedor.objects.create(**self.attributes)
        self.serializer = RevendedorSerializer(instance=self.revendedor)

        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')

    def test_get_revendedores(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='jacob')
        view = RevendedorViewSet.as_view({'get': 'list'})

        request = factory.get('/revendedor/')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)




if __name__ == '__main__':
    unittest.main()