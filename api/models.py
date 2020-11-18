# coding=utf8
from django.db import models
from cpf_field.models import CPFField


class Revendedor(models.Model):
    class Meta:
        verbose_name = u'Revendedor'
        verbose_name_plural = u'Revendedores'
        db_table = 'revendedor'
        ordering = ['nome']


    nome  = models.CharField(max_length=60, verbose_name=u'Nome')
    cpf   = CPFField('cpf', unique=True)
    email = models.EmailField(max_length=60, verbose_name=u'Email', unique=True)
    senha = models.CharField(max_length=60, verbose_name=u'Senha')

    def __str__(self):
        return self.nome

    def __unicode__(self):
        return u'%s' % (self.nome)


class Status(models.Model):
    class Meta:
        verbose_name = u'Status'
        verbose_name_plural = u'Status'
        db_table = 'status_pedido' 
        ordering = ['status']   

    status = models.CharField(max_length=60, verbose_name=u'Status')

    def __str__(self):
        return self.status

    def __unicode__(self):
        return u'%s' % (self.status)


class Pedido(models.Model):
    class Meta:
        verbose_name = u'Pedido'
        verbose_name_plural = u'Pedidos'
        db_table = 'pedido'
        ordering = ['data']   

    numero     = models.CharField(max_length=60, verbose_name=u'Número')
    revendedor = models.ForeignKey(Revendedor, verbose_name=u'Revendedor', related_name='revendedor_pedido', null=False, blank=False, on_delete=models.RESTRICT)
    status     = models.ForeignKey(Status, verbose_name=u'Status', related_name='status_pedido', null=False, blank=False, on_delete=models.RESTRICT)
    valor      = models.DecimalField(max_digits=10, decimal_places=6, verbose_name=u'Valor', null=True, blank=True)
    data       = models.DateTimeField(verbose_name=u'Data/Hora Pedido', null=True, blank=True)

    def __str__(self):
        return self.numero        
    
    def __unicode__(self):
        return u'%s' % (self.numero)



class CashBack(models.Model):
    class Meta:
        verbose_name = u'CashBack'
        verbose_name_plural = u'CashBack'
        db_table = 'cashback'
        ordering = ['percentual'] 

    valor_min  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Valor Mínimo', null=True, blank=True)
    valor_max  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Valor Máximo', null=True, blank=True)
    percentual = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Percentual', null=True, blank=True)


class CashBackRevendedor(models.Model):
    class Meta:
        verbose_name = u'CashBack Revendedor'
        verbose_name_plural = u'CashBack'
        db_table = 'cashback_revendedor'
        ordering = ['data']

    revendedor = models.ForeignKey(Revendedor, verbose_name=u'Revendedor', related_name='revendedor_cashback_pedido', null=False, blank=False, on_delete=models.RESTRICT)
    pedido     = models.ForeignKey(Pedido, verbose_name=u'Pedido', related_name='cashback_pedido', null=False, blank=False, on_delete=models.RESTRICT)
    valor      = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Valor CashBack', null=True, blank=True)
    data       = models.DateTimeField(verbose_name=u'Data/Hora Pedido', null=True, blank=True)

    def __str__(self):
        return str(self.revendedor)
    
    def __unicode__(self):
        return u'%s' % (self.revendedor)        