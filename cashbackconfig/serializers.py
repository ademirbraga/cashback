
# coding=utf8
from django_print_sql import print_sql_decorator
from rest_framework.serializers import ModelSerializer
from .models import CashBack

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
            raise ValidationError("Não foi encontrado percentual de cashbackconfig para o valor '%s' informado." % valor_pedido)

