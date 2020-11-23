# coding=utf8
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Revendedor
from django.contrib.auth.hashers import make_password
from cashback.settings import SALT

import logging

logger = logging.getLogger(__name__)


class RevendedorSerializer(ModelSerializer):
    class Meta:
        model = Revendedor
        fields = ('id', 'nome', 'cpf', 'email', 'senha')
        extra_kwargs = {'senha': {'write_only': True}}

    def create(self, validated_data):
        logger.info('Criacao de novo revendedor: {}'.format(validated_data['nome']))
        if validated_data['senha']:
            validated_data['senha'] = make_password(validated_data['senha'], salt=SALT)

        result = Revendedor.objects.create(**validated_data)
        logger.info('Cadastro de revendedor realizado com sucesso.')
        return result

    def get_revendedor_by_cpf(self, data):
        try:
            revendedor = Revendedor.objects.get(cpf=data['revendedor']['cpf'])
            serializer = RevendedorSerializer(revendedor)
            return serializer.data
        except Revendedor.DoesNotExist:
            logger.error("Revendedor com CPF '%s' não foi encontrado." % data['revendedor']['cpf'])
            raise ValidationError("Revendedor com CPF '%s' não foi encontrado." % data['revendedor']['cpf'])
