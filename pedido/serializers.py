# coding=utf8
from decimal import Decimal
from django.db import IntegrityError, transaction
from rest_framework.serializers import ModelSerializer, RelatedField, SerializerMethodField, CharField, DateTimeField, DecimalField, ValidationError
from cashbackrevendedor.models import CashBackRevendedor
from whitelistpedido.models import WhiteListPedido
from revendedor.serializers import RevendedorSerializer
from cashbackconfig.serializers import CashBackSerializer
from .models import Pedido
from settings import STATUS_EM_VALIDACAO, STATUS_APROVADO
import sys

import logging
logger = logging.getLogger(__name__)


class StatusField(RelatedField):
    def to_native(self, value):
        return value.status

class PercentualCashBackField(RelatedField):
    def to_native(self, value):
        return value.perc_cashback

class ValorCashBackField(RelatedField):
    def to_native(self, value):
        return value.valor_cashback        

# p.numero,
# p.valor,
# p."data",
# cr.perc_cashback,
# cr.valor as valor_cashback,
# sp.status

class PedidoV2Serializer(ModelSerializer):
    numero = SerializerMethodField()

    def get_numero(self, instance):
        print('**********************\n')
        print(instance)
        print('**********************\n')
        return instance.numero

    # numero = CharField()
    # status = StatusField(many=False, read_only=True)
    perc_cashback = PercentualCashBackField(many=False, read_only=True)
    # valor_cashback = ValorCashBackField(many=False, read_only=True)
    # revendedor = CharField(source='revendedor.cpf')
    # data       = DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    # valor      = DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model  = Pedido
        fields = ['numero', 'perc_cashback']
        #, 'perc_cashback', 'valor_cashback', 'status']


class PedidoSerializer(ModelSerializer):
    revendedor = CharField(source='revendedor.cpf')
    data       = DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    valor      = DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model  = Pedido
        fields = '__all__'

    def get_status_pedido(self, cpf_revendedor):
        cpf_liberado = WhiteListPedido.objects.filter(cpf=cpf_revendedor, ativo=True)
        if cpf_liberado:
            logger.info('O Pedido será APROVADO, pois o CPF do revendedor esta na white list.')
            return STATUS_APROVADO

        logger.info('O Pedido ficara AGUARDANDO APROVACAO, pois o CPF do revendedor nao esta na white list.')
        return STATUS_EM_VALIDACAO

    def create(self, validated_data):
        logger.info('Criacao de novo pedido %s', validated_data['numero'])

        revendedor = RevendedorSerializer.get_revendedor_by_cpf(self, validated_data)
        status = self.get_status_pedido(revendedor['cpf'])

        pedido = {
            'numero': validated_data['numero'],
            'revendedor_id': revendedor['id'],
            'data': validated_data['data'],
            'valor': validated_data['valor'],
            'status_id': status
        }

        try:
            with transaction.atomic():
                pedido = Pedido.objects.create(**pedido)
                pedido_id = PedidoSerializer(pedido)
                pedido_id = pedido_id.data

                # cadastrar cashbackconfig do revendedor
                cashback       = CashBackSerializer.get_cash_back(self, validated_data['valor'])
                valor_cashback = validated_data['valor'] * (Decimal(cashback['percentual']) / 100)

                cashback_revendedor = {
                    'valor': valor_cashback,
                    'data': validated_data['data'],
                    'pedido_id': pedido_id['id'],
                    'revendedor_id': revendedor['id'],
                    'perc_cashback': cashback['percentual']

                }
                logger.info('Registrando cashbackconfig do revendedor {} para o pedido {}'.format(revendedor['nome'], validated_data['numero']))
                CashBackRevendedor.objects.create(**cashback_revendedor)

            return pedido
        except TypeError as err:
            logger.exception('Unexpected error: {0}'.format(err))
            raise ValidationError('Ocorreu algum problema ao cadastrar o novo pedido. Tente novamente mais tarde.', code=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            raise IntegrityError('Não foi possível cadastrar o pedido. Por favor, verifique os parâmetros e tente novamente mais tarde.')
        except:
            logger.exception("Unexpected error: {0}".format(sys.exc_info()[0]))
            raise
