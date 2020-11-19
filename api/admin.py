from django.contrib import admin
from .models import Revendedor, Status, Pedido, CashBack, CashBackRevendedor, WhiteListPedido


class WhiteListPedidoAdmin(admin.ModelAdmin):
    list_display    = ['cpf', 'ativo']
    list_filter     = ('cpf', 'ativo')
    search_fields   = ('cpf', 'ativo')
    ordering        = ['cpf', 'ativo']
    save_as = True
    
admin.site.register(WhiteListPedido, WhiteListPedidoAdmin)
class PedidoAdmin(admin.ModelAdmin):
    list_display    = ['numero', 'revendedor', 'status', 'valor', 'data']
    list_filter     = ('numero', 'revendedor', 'status', 'valor', 'data')
    search_fields   = ('numero', 'revendedor', 'status', 'valor', 'data')
    ordering        = ['numero', 'revendedor', 'status', 'valor', 'data']
    save_as = True
    
admin.site.register(Pedido, PedidoAdmin)


class CashBackAdmin(admin.ModelAdmin):
    list_display    = ['valor_min', 'valor_max', 'percentual']
    list_filter     = ('valor_min', 'valor_max', 'percentual')
    search_fields   = ('valor_min', 'valor_max', 'percentual')
    ordering        = ['valor_min', 'valor_max', 'percentual']
    save_as = True
    
admin.site.register(CashBack, CashBackAdmin)

class CashBackRevendedorAdmin(admin.ModelAdmin):
    list_display    = ['revendedor', 'pedido', 'perc_cashback', 'valor', 'data']
    list_filter     = ('revendedor', 'pedido', 'perc_cashback', 'valor', 'data')
    search_fields   = ('revendedor', 'pedido', 'perc_cashback', 'valor', 'data')
    ordering        = ['revendedor', 'pedido', 'perc_cashback', 'valor', 'data']
    save_as = True

admin.site.register(CashBackRevendedor, CashBackRevendedorAdmin)


admin.site.register(Revendedor)
admin.site.register(Status)