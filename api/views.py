# coding=utf8
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions


from .serializers import RevendedorSerializer, PedidoSerializer, CashBackRevendedorSerializer, WhiteListPedidoSerializer
from .models import Revendedor, Pedido, CashBackRevendedor, WhiteListPedido


class RevendedorViewSet(viewsets.ModelViewSet):
    queryset = Revendedor.objects.all().order_by('nome')
    serializer_class = RevendedorSerializer
    # permission_classes = [permissions.IsAuthenticated]



class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('numero')
    serializer_class = PedidoSerializer
    """
    ViewSet para listar as compras cadastradas retornando:
    código, valor, data, % de cashback aplicado para esta compra, 
    valor de cashback para esta compra e status
    """
    def list(self, request, *args, **kwargs):
        pedidos = Pedido.objects.listar_pedidos()
        serializer = self.get_serializer(pedidos, many=True)
        return Response(serializer.data)



class CashBackRevendedorViewSet(viewsets.ModelViewSet):
    queryset = CashBackRevendedor.objects.all().order_by('revendedor')
    serializer_class = CashBackRevendedorSerializer    

class WhiteListPedidoViewSet(viewsets.ModelViewSet):
    queryset = WhiteListPedido.objects.all().order_by('cpf')
    serializer_class = WhiteListPedidoSerializer