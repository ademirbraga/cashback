# coding=utf8
from rest_framework import viewsets
from .serializers import RevendedorSerializer
from .models import Revendedor


class RevendedorViewSet(viewsets.ModelViewSet):
    queryset = Revendedor.objects.all().order_by('nome')
    serializer_class = RevendedorSerializer
