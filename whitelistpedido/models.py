# coding=utf8
from django.db import models
from django.db.models import BooleanField
from cpf_field.models import CPFField

class WhiteListPedido(models.Model):
    class Meta:
        verbose_name = u'White List Pedido'
        verbose_name_plural = u'White List Pedido'
        db_table = 'white_list_pedido' 
        ordering = ['cpf']   

    cpf   = CPFField('cpf', unique=True)
    ativo = BooleanField(verbose_name=u'Ativo?', default=True, null=False, blank=False)

    def __str__(self):
        return self.cpf

    def __unicode__(self):
        return u'%s' % (self.cpf)

      