# coding=utf8
from django.db import models

class CashBack(models.Model):
    class Meta:
        verbose_name = u'Config. CashBack'
        verbose_name_plural = u'Config. CashBack'
        db_table = 'cashback'
        ordering = ['percentual'] 

    valor_min  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Valor Mínimo', null=True, blank=True)
    valor_max  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Valor Máximo', null=True, blank=True)
    percentual = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Percentual', null=True, blank=True)
