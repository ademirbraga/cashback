from .models import Revendedor
from .serializers import RevendedorSerializer
import unittest
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.test import APIRequestFactory

from .views import PedidoViewSet
from cashbackconfig.models import CashBack
from statuspedido.models import Status
import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = 'jacob'
    email = 'jacob@example.com'

class TestRevendedor(unittest.TestCase):
    def setUp(self):
        self.attributes = {
            'nome': 'Maria Silva',
            'cpf': '30999851047',
            'email': 'maria@silva.com',
            'senha': '123456'
        }

        self.serializer_data = {
            'nome': 'Maria Silva',
            'cpf': '30999851047',
            'email': 'maria@silva.com',
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



    def test_get_pedidos(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='jacob')
        view = PedidoViewSet.as_view({'get': 'listar_pedidos'})

        request = factory.get('/listar-pedidos')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)



    def test_salvar_pedido(self):

        # cadastrar as configs de cashback
        cashback = {
            'valor_min': '0.01',
            'valor_max': '2000',
            'percentual': '20'
        }
        CashBack.objects.create(**cashback)

        # cadastrar status de pedido
        st1 = {
            'id': 1,
            'status': 'Em validação'
        }
        st2 = {
            'id': 2,
            'status': 'Aprovado'
        }
        Status.objects.create(**st1)
        Status.objects.create(**st2)


        factory = APIRequestFactory()
        user = User.objects.get(username='jacob')
        view = PedidoViewSet.as_view({'post': 'create'})

        pedido = {
            "numero": "xpto001",
            "revendedor": self.attributes.get('cpf'),
            "valor": 1100.45,
            "data": "2020-11-18 10:00:00"
        }

        request = factory.post('/cadastrar-pedido/', pedido)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 201)



if __name__ == '__main__':
    unittest.main()