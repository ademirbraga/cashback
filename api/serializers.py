# coding=utf8
from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, ValidationError
from .models import Revendedor, Pedido, CashBackRevendedor, WhiteListPedido
from django.contrib.auth.hashers import make_password
from settings import SALT, STATUS_EM_VALIDACAO, STATUS_APROVADO



class WhiteListPedidoSerializer(ModelSerializer):
    class Meta:
        model  = WhiteListPedido
        fields = '__all__'


class RevendedorSerializer(ModelSerializer):
    class Meta:
        model  = Revendedor
        fields = ('id', 'nome', 'cpf', 'email', 'senha')
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
    data = DateTimeField(format='%Y-%m-%dT%H:%M:%S')

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
        print('STATUS.....................', status)

        pedido = {
            'numero': validated_data['numero'],
            'revendedor_id': revendedor['id'],
            'data': validated_data['data'],
            'valor': validated_data['valor'],
            'status_id': status
        }

        return Pedido.objects.create(**pedido)

        #  cashback_revendedor = validated_data.pop('enderecos')
        # CashBackRevendedor.objects.create(revendedor, **cashback_revendedor)
      


class CashBackRevendedorSerializer(ModelSerializer):
    revendedor   = CharField(source='revendedor.nome')
    pedido       = CharField(source='pedido.numero')
    valor_pedido = CharField(source='pedido.valor')
    class Meta:
        model  = CashBackRevendedor
        fields = ('revendedor', 'pedido', 'valor_pedido', 'perc_cashback', 'valor', 'data')  
