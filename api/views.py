# coding=utf8
from django.shortcuts import render

from rest_framework import viewsets

from .serializers import RevendedorSerializer, PedidoSerializer, CashBackRevendedorSerializer
from .models import Revendedor, Pedido, CashBackRevendedor


class RevendedorViewSet(viewsets.ModelViewSet):
    queryset = Revendedor.objects.all().order_by('nome')
    serializer_class = RevendedorSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('numero')
    serializer_class = PedidoSerializer


class CashBackRevendedorViewSet(viewsets.ModelViewSet):
    queryset = CashBackRevendedor.objects.all().order_by('revendedor')
    serializer_class = CashBackRevendedorSerializer    