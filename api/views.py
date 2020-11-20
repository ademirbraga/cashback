# coding=utf8
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions
import json, requests
from django_print_sql import print_sql_decorator
import logging
from settings import CASHBACK_RETRIEVE_URL, CASHBACK_RETRIEVE_TOKEN
from .serializers import RevendedorSerializer, PedidoSerializer, CashBackRevendedorSerializer, WhiteListPedidoSerializer, PedidoV2Serializer
from .models import Revendedor, Pedido, CashBackRevendedor, WhiteListPedido
logger = logging.getLogger(__name__)


class RevendedorViewSet(viewsets.ModelViewSet):
    queryset = Revendedor.objects.all().order_by('nome')
    serializer_class = RevendedorSerializer
    # permission_classes = [permissions.IsAuthenticated]



class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('numero')
    serializer_class = PedidoSerializer
    """
    ViewSet para listar as compras cadastradas retornando:
    1: código, 
    2: valor, 
    3: data, % de cashback aplicado para esta compra, 
    4: valor de cashback para esta compra
    5: status
    """
    @print_sql_decorator(count_only=False) 
    def listar_pedidos(self, request, *args, **kwargs):
        pedidos = Pedido.pedidos.listar_pedidos()
        serializer = PedidoV2Serializer(pedidos)
        return Response(serializer.data)


class CashBackRevendedorViewSet(viewsets.ModelViewSet):
    queryset = CashBackRevendedor.objects.all().order_by('revendedor')
    serializer_class = CashBackRevendedorSerializer  

    def cashback_acumulado(self, request, *args, **kwargs):
        logger.info('Buscando cashback acumulado do revendedor em uma API externa.')
        headers = {
            'token': CASHBACK_RETRIEVE_TOKEN
        }
        url = '{}?cpf={}'.format(CASHBACK_RETRIEVE_URL, kwargs['cpf'])
        response = requests.get(url, headers=headers)

        if response.status_code == status.HTTP_200_OK:
            return Response(json.loads(response.content))
        logger.error('Nao foi possivel recuperar o cashback acumulado devido a um erro externo. Erro: {}'.format(response.text))
        return Response({"error": "Request failed"}, status=response.status_code) 

class WhiteListPedidoViewSet(viewsets.ModelViewSet):
    queryset = WhiteListPedido.objects.all().order_by('cpf')
    serializer_class = WhiteListPedidoSerializer