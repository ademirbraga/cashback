from .models import Revendedor
from .serializers import RevendedorSerializer
import unittest
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.test import APIRequestFactory

from .views import RevendedorViewSet
import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'jacob'
    email = 'jacob@example.com'

class TestRevendedor(unittest.TestCase):
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

        try:
            self.user = User.objects.get(username='jacob')
        except:
            self.user = UserFactory.create()
            self.user.set_password('secret')
            self.user.save()



    def test_get_revendedores(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='jacob')
        view = RevendedorViewSet.as_view({'get': 'list'})

        request = factory.get('/revendedor/')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)



    def test_salvar_revendedor(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='jacob')
        view = RevendedorViewSet.as_view({'post': 'create'})

        revendedor = {
            'nome': 'Maria Silva',
            'cpf': '26621630034',
            'email': 'maria@silva.com',
            'senha': '123456'
        }

        request = factory.post('/revendedor/', revendedor)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 201)



if __name__ == '__main__':
    unittest.main()