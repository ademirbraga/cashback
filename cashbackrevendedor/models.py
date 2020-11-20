# coding=utf8
from django.db import models

from pedido.models import Pedido
from revendedor.models import Revendedor


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