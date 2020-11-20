# coding=utf8
from decimal import Decimal
from rest_framework.serializers import ModelSerializer, CharField
from .models import CashBackRevendedor

class CashBackRevendedorSerializer(ModelSerializer):
    revendedor   = CharField(source='revendedor.nome')
    pedido       = CharField(source='pedido.numero')
    valor_pedido = CharField(source='pedido.valor')
    class Meta:
        model  = CashBackRevendedor
        fields = ('revendedor', 'pedido', 'valor_pedido', 'perc_cashback', 'valor', 'data')  
