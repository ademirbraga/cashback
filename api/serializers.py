# coding=utf8
from rest_framework.serializers import ModelSerializer, CharField
from .models import Revendedor, Pedido, CashBackRevendedor

class RevendedorSerializer(ModelSerializer):
    class Meta:
        model  = Revendedor
        fields = ('nome', 'cpf', 'email')

class PedidoSerializer(ModelSerializer):
    status     = CharField(source='status.status')
    revendedor = CharField(source='revendedor.nome')

    class Meta:
        model  = Pedido
        fields = ('numero', 'revendedor', 'status', 'valor', 'data')        


class CashBackRevendedorSerializer(ModelSerializer):
    revendedor = CharField(source='revendedor.nome')
    pedido     = CharField(source='pedido.numero')
    class Meta:
        model  = CashBackRevendedor
        fields = ('revendedor', 'pedido', 'valor', 'data')  