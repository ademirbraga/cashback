from django.db import models

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



