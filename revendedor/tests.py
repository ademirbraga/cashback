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
        revendedor1 = Revendedor.objects.filter(cpf=self.attributes.get('cpf'))
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
            'nome': 'Antonio Silva',
            'cpf': '56972140064',
            'email': 'antonio@silva.com',
            'senha': '123456'
        }
        request = factory.post('/revendedor/', revendedor)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_salvar_revendedor_cpf_vazio(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='jacob')
        view = RevendedorViewSet.as_view({'post': 'create'})

        revendedor = {
            'nome': 'Antonio Silva',
            'cpf': '',
            'email': 'antonio@silva.com',
            'senha': '123456'
        }
        request = factory.post('/revendedor/', revendedor)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_salvar_revendedor_ja_existente(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='jacob')
        view = RevendedorViewSet.as_view({'post': 'create'})

        revendedor = {
            'nome': 'Antonio Silva',
            'cpf': '56972140064',
            'email': 'antonio@silva.com',
            'senha': '123456'
        }
        request = factory.post('/revendedor/', revendedor)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_integracao_salvar_revendedor(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='jacob')
        view = RevendedorViewSet.as_view({'post': 'create'})
        cpf = '11134215096'
        revendedor = {
            'nome': 'Juca Pirama',
            'cpf': cpf,
            'email': 'juca.pirama@gmail.com',
            'senha': '123456'
        }
        request = factory.post('/revendedor/', revendedor)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

        revendedor = Revendedor.objects.get(cpf=cpf)
        revendedor = RevendedorSerializer(revendedor)
        revendedor = revendedor.data

        self.assertEquals(revendedor['cpf'], cpf)


if __name__ == '__main__':
    unittest.main()
