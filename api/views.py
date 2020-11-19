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


class CashBackRevendedorViewSet(viewsets.ModelViewSet):
    queryset = CashBackRevendedor.objects.all().order_by('revendedor')
    serializer_class = CashBackRevendedorSerializer    

class WhiteListPedidoViewSet(viewsets.ModelViewSet):
    queryset = WhiteListPedido.objects.all().order_by('cpf')
    serializer_class = WhiteListPedidoSerializer