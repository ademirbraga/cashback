# coding=utf8
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import json, requests
from .serializers import CashBackRevendedorSerializer
from .models import CashBackRevendedor
from cashback.settings import CASHBACK_RETRIEVE_URL, CASHBACK_RETRIEVE_TOKEN

import logging
logger = logging.getLogger(__name__)

class CashBackRevendedorViewSet(viewsets.ModelViewSet):
    queryset = CashBackRevendedor.objects.all().order_by('revendedor')
    serializer_class = CashBackRevendedorSerializer  

    def cashback_acumulado(self, request, *args, **kwargs):
        logger.info('Buscando cashback acumulado do revendedor em uma API externa.')
        headers = {
            'token': CASHBACK_RETRIEVE_TOKEN
        }

        if 'cpf' not in kwargs:
            return Response({"error": "Favor informar um CPF válido."}, status=status.HTTP_404_NOT_FOUND)

        url = '{}?cpf={}'.format(CASHBACK_RETRIEVE_URL, kwargs['cpf'])
        response = requests.get(url, headers=headers)
        logger.info(response)

        if response.status_code == status.HTTP_200_OK:
            return Response(json.loads(response.content))
        logger.error('Nao foi possivel recuperar o cashback acumulado devido a um erro externo. Erro: {}'.format(response.text))
        return Response({"error": "Request failed"}, status=response.status_code) 
