from .models import Revendedor
import unittest
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.test import APIRequestFactory

from .views import PedidoViewSet
from .serializers import PedidoSerializer
from cashbackrevendedor.models import CashBackRevendedor
from cashbackrevendedor.serializers import CashBackRevendedorSerializer
from cashbackconfig.models import CashBack
from statuspedido.models import Status
from .models import Pedido
import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = 'jacob'
    email = 'jacob@example.com'

class TestPedido(unittest.TestCase):
    def setUp(self):
        self.attributes = {
            'nome': 'Maria Silva',
            'cpf': '30999851047',
            'email': 'maria@silva.com',
            'senha': '123456'
        }

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
        #cadastrar revendedor
        self.revendedor = Revendedor.objects.create(**self.attributes)


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

        nro_pedido = 'xpto001'
        valor = 1100.45
        pedido = {
            "numero": nro_pedido,
            "revendedor": self.attributes.get('cpf'),
            "valor": valor,
            "data": "2020-11-18 10:00:00"
        }

        request = factory.post('/cadastrar-pedido/', pedido)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        nro_pedido

        pedido = Pedido.objects.get(numero=nro_pedido)
        pedido = PedidoSerializer(pedido)
        pedido = pedido.data
        self.assertEquals(pedido['numero'], nro_pedido)
        self.assertEquals(str(pedido['valor']), str(valor))

        cashback_revendedor = CashBackRevendedor.objects.get(pedido_id=pedido['id'])
        cashback_revendedor = CashBackRevendedorSerializer(cashback_revendedor)
        cashback_revendedor = cashback_revendedor.data
        self.assertIsNotNone(cashback_revendedor)


    def test_salvar_pedido_sem_status_casdastrado(self):
        # remover config de cashback cadastrados anteriormente
        st1 = CashBack.objects.filter(id=1)
        if st1:
            st1[0].delete()

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
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()