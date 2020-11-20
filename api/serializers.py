# coding=utf8
from decimal import Decimal
from django.db import IntegrityError, transaction
from rest_framework import status
from django_print_sql import print_sql_decorator
from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, DecimalField, ValidationError
from .models import Revendedor, Pedido, CashBackRevendedor, WhiteListPedido, CashBack
from django.contrib.auth.hashers import make_password
from settings import SALT, STATUS_EM_VALIDACAO, STATUS_APROVADO


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
        if validated_data['senha']:
            validated_data['senha'] = make_password(validated_data['senha'], salt=SALT)

        return Revendedor.objects.create(**validated_data)


    def get_revendedor_by_cpf(self, data):
        try:
            revendedor = Revendedor.objects.get(cpf=data['revendedor']['cpf'])
            serializer = RevendedorSerializer(revendedor)
            return serializer.data
        except Revendedor.DoesNotExist:
            raise ValidationError("Revendedor com CPF '%s' não foi encontrado." % data['revendedor']['cpf'])

        


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
            return STATUS_APROVADO
        return STATUS_EM_VALIDACAO

    def create(self, validated_data):
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
                CashBackRevendedor.objects.create(**cashback_revendedor)
            return pedido
        except TypeError:
            raise ValidationError('Ocorreu algum problema ao cadastrar o novo pedido. Tente novamente mais tarde.', code=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            raise IntegrityError('Não foi possível cadastrar o pedido. Por favor, verifique os parâmetros e tente novamente mais tarde.')


class CashBackRevendedorSerializer(ModelSerializer):
    revendedor   = CharField(source='revendedor.nome')
    pedido       = CharField(source='pedido.numero')
    valor_pedido = CharField(source='pedido.valor')
    class Meta:
        model  = CashBackRevendedor
        fields = ('revendedor', 'pedido', 'valor_pedido', 'perc_cashback', 'valor', 'data')  
