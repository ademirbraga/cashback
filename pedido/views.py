# coding=utf8
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django_print_sql import print_sql_decorator
import logging
from .models import Pedido
from .serializers import PedidoSerializer

logger = logging.getLogger(__name__)


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('numero')
    serializer_class = PedidoSerializer
    """
    ViewSet para listar as compras cadastradas retornando:
    1: código, 
    2: valor, 
    3: data, % de cashbackconfig aplicado para esta compra, 
    4: valor de cashbackconfig para esta compra
    5: status
    """
    @print_sql_decorator(count_only=False) 
    def listar_pedidos(self, request, *args, **kwargs):
        pedidos = Pedido.pedidos.listar_pedidos()
        return Response(pedidos)
