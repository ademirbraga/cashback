from django.contrib import admin
from .models import Pedido


class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'revendedor', 'status', 'valor', 'data']
    list_filter = ('numero', 'revendedor', 'status', 'valor', 'data')
    search_fields = ('numero', 'revendedor', 'status', 'valor', 'data')
    ordering = ['numero', 'revendedor', 'status', 'valor', 'data']
    save_as = True


admin.site.register(Pedido, PedidoAdmin)
