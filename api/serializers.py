# coding=utf8
from decimal import Decimal
from django.db import IntegrityError, transaction
from rest_framework import status
from django_print_sql import print_sql_decorator
from rest_framework.serializers import ModelSerializer, RelatedField, SerializerMethodField, CharField, DateTimeField, DecimalField, ValidationError
from .models import Revendedor, Pedido, CashBackRevendedor, WhiteListPedido, CashBack
from django.contrib.auth.hashers import make_password
from settings import SALT, STATUS_EM_VALIDACAO, STATUS_APROVADO

import logging
logger = logging.getLogger(__name__)


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class WhiteListPedidoSerializer(ModelSerializer):
    class Meta:
        model  = WhiteListPedido
        fields = '__all__'


class CashBackSerializer(ModelSerializer):
    class Meta:
        model  = CashBack
        fields = '__all__'

    @print_sql_decorator(count_only=False) 
    def get_cash_back(self, valor_pedido):
        try:
            cashback = CashBack.objects.get(valor_min__lte=valor_pedido, valor_max__gte=valor_pedido)
            
            serializer = CashBackSerializer(cashback)
            return serializer.data
        except CashBack.DoesNotExist:
            raise ValidationError("Não foi encontrado percentual de cashback para o valor '%s' informado." % valor_pedido)

class RevendedorSerializer(ModelSerializer):
    class Meta:
        model        = Revendedor
        fields       = ('id', 'nome', 'cpf', 'email', 'senha')
        extra_kwargs = {'senha': {'write_only': True}}

    def create(self, validated_data):
        logger.info('Criacao de novo revendedor: {}'.format(validated_data['nome']))
        if validated_data['senha']:
            validated_data['senha'] = make_password(validated_data['senha'], salt=SALT)
        
        return Revendedor.objects.create(**validated_data)


    def get_revendedor_by_cpf(self, data):
        try:
            revendedor = Revendedor.objects.get(cpf=data['revendedor']['cpf'])
            serializer = RevendedorSerializer(revendedor)
            return serializer.data
        except Revendedor.DoesNotExist:
            logger.error("Revendedor com CPF '%s' não foi encontrado." % data['revendedor']['cpf'])
            raise ValidationError("Revendedor com CPF '%s' não foi encontrado." % data['revendedor']['cpf'])

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

                # cadastrar cashback do revendedor
                cashback       = CashBackSerializer.get_cash_back(self, validated_data['valor'])
                valor_cashback = validated_data['valor'] * (Decimal(cashback['percentual']) / 100)

                cashback_revendedor = {
                    'valor': valor_cashback,
                    'data': validated_data['data'],
                    'pedido_id': pedido_id['id'],
                    'revendedor_id': revendedor['id'],
                    'perc_cashback': cashback['percentual']

                }
                logger.info('Registrando cashback do revendedor {} para o pedido {}'.format(revendedor['nome'], validated_data['numero']))
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

class CashBackRevendedorSerializer(ModelSerializer):
    revendedor   = CharField(source='revendedor.nome')
    pedido       = CharField(source='pedido.numero')
    valor_pedido = CharField(source='pedido.valor')
    class Meta:
        model  = CashBackRevendedor
        fields = ('revendedor', 'pedido', 'valor_pedido', 'perc_cashback', 'valor', 'data')  
