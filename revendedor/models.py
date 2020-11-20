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
    senha = models.CharField(max_length=100, verbose_name=u'Senha')

    def __str__(self):
        return self.nome

    def __unicode__(self):
        return u'%s' % (self.nome)