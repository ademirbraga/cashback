# coding=utf8
from django.db import models

from revendedor.models import Revendedor
from statuspedido.models import Status
from cashback.settings import STATUS_EM_VALIDACAO


class PedidoQuerySet(models.QuerySet):
    def dictfetchall(self, cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    def listar_pedidos(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                select
                    p.numero,
                    p.valor,
                    p."data",
                    cr.perc_cashback,
                    cr.valor as valor_cashback,
                    sp.status
                from
                    pedido p 
                    inner join cashback_revendedor cr on cr.pedido_id = p.id
                    inner join status_pedido sp on sp.id = p.status_id
                """)
            result_list = self.dictfetchall(cursor)
        return result_list


class PedidoManager(models.Manager):
    def get_queryset(self):
        return PedidoQuerySet(self.model, using=self._db)

    def listar_pedidos(self):
        return self.get_queryset().listar_pedidos()


class Pedido(models.Model):
    class Meta:
        verbose_name = u'Pedido'
        verbose_name_plural = u'Pedidos'
        db_table = 'pedido'
        ordering = ['data']

    objects = models.Manager()
    pedidos = PedidoManager()  # PedidoQuerySet.as_manager()

    numero = models.CharField(max_length=60, verbose_name=u'Número', unique=True)
    revendedor = models.ForeignKey(Revendedor, verbose_name=u'Revendedor', related_name='revendedor_pedido', null=False,
                                   blank=False, on_delete=models.RESTRICT)
    status = models.ForeignKey(Status, verbose_name=u'Status', default=STATUS_EM_VALIDACAO,
                               related_name='status_pedido', null=False, blank=False, on_delete=models.RESTRICT)
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Valor', null=False, blank=False)
    data = models.DateTimeField(verbose_name=u'Data/Hora Pedido', null=False, blank=False, auto_now_add=False)

    def __str__(self):
        return self.numero

    def __unicode__(self):
        return u'%s' % (self.numero)
