import unittest
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.test import APIRequestFactory

from .views import CashBackRevendedorViewSet
import factory
from unittest.mock import Mock, patch

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'jacob'
    email = 'jacob@example.com'

class TestCashBackRevendedor(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        try:
            self.user = User.objects.get(username='jacob')
        except:
            self.user = UserFactory.create()
            self.user.set_password('secret')
            self.user.save()



    def test_get_cashback_acumulado(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='jacob')

        view = CashBackRevendedorViewSet.as_view({'get': 'cashback_acumulado'})

        cpf = '01287210651'
        url = '/cashback-acumulado/%s' % cpf
        request = factory.get(url)

        force_authenticate(request, user=user)
        response = view(request, cpf=cpf)

        self.assertEqual(response.status_code, 200)


    def test_get_cashback_acumulado_erro_404(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='jacob')
        view = CashBackRevendedorViewSet.as_view({'get': 'cashback_acumulado'})

        request = factory.get('/cashback-acumulado/')
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()