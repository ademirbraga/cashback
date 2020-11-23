# coding=utf8
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import WhiteListPedidoSerializer
from .models import WhiteListPedido


class WhiteListPedidoViewSet(viewsets.ModelViewSet):
    queryset = WhiteListPedido.objects.all().order_by('cpf')
    serializer_class = WhiteListPedidoSerializer
