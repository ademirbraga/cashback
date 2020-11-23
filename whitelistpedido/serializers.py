# coding=utf8
from rest_framework.serializers import ModelSerializer
from .models import WhiteListPedido


class WhiteListPedidoSerializer(ModelSerializer):
    class Meta:
        model = WhiteListPedido
        fields = '__all__'
