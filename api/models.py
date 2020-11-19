# coding=utf8
from django.db import models
from django.db.models import BooleanField
from cpf_field.models import CPFField
from settings import STATUS_EM_VALIDACAO


class Revendedor(models.Model):
    class Meta:
        verbose_name = u'Revendedor'
        verbose_name_plural = u'Revendedores'
        db_table = 'revendedor'
        ordering = ['nome']


    nome  = models.CharField(max_length=60, verbose_name=u'Nome')
    cpf   = CPFField('cpf', unique=True)
    email = models.EmailField(max_length=60, verbose_name=u'Email', unique=True)
    senha = models.CharField(max_length=100, verbose_name=u'Senha')

    def __str__(self):
        return self.nome

    def __unicode__(self):
        return u'%s' % (self.nome)


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

    numero        = models.CharField(max_length=60, verbose_name=u'Número', unique=True)
    revendedor    = models.ForeignKey(Revendedor, verbose_name=u'Revendedor', related_name='revendedor_pedido', null=False, blank=False, on_delete=models.RESTRICT)
    status        = models.ForeignKey(Status, verbose_name=u'Status', default=STATUS_EM_VALIDACAO, related_name='status_pedido', null=False, blank=False, on_delete=models.RESTRICT)
    valor         = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Valor', null=False, blank=False)
    data          = models.DateTimeField(verbose_name=u'Data/Hora Pedido', null=False, blank=False, auto_now_add=False)

    def __str__(self):
        return self.numero        
    
    def __unicode__(self):
        return u'%s' % (self.numero)



class CashBack(models.Model):
    class Meta:
        verbose_name = u'Config. CashBack'
        verbose_name_plural = u'Config. CashBack'
        db_table = 'cashback'
        ordering = ['percentual'] 

    valor_min  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Valor Mínimo', null=True, blank=True)
    valor_max  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Valor Máximo', null=True, blank=True)
    percentual = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Percentual', null=True, blank=True)


class CashBackRevendedor(models.Model):
    class Meta:
        verbose_name = u'CashBack Revendedor'
        verbose_name_plural = u'CashBack Revendedores'
        db_table = 'cashback_revendedor'
        ordering = ['data']
        unique_together = ['revendedor', 'pedido']
        constraints = [
            models.CheckConstraint(check=models.Q(perc_cashback__lte=20), name='perc_cashback_lte_20'),
        ]

    revendedor    = models.ForeignKey(Revendedor, verbose_name=u'Revendedor', related_name='revendedor_cashback_pedido', null=False, blank=False, on_delete=models.RESTRICT)
    pedido        = models.ForeignKey(Pedido, verbose_name=u'Pedido', related_name='cashback_pedido', null=False, blank=False, on_delete=models.RESTRICT)
    valor         = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Valor CashBack', null=True, blank=True)
    data          = models.DateTimeField(verbose_name=u'Data/Hora Pedido', null=True, blank=True)
    perc_cashback = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Perc. CashBack Aplicado', null=True, blank=True)

    def __str__(self):
        return str(self.revendedor)
    
    def __unicode__(self):
        return u'%s' % (self.revendedor)        