from django.contrib import admin
from .models import CashBackRevendedor


class CashBackRevendedorAdmin(admin.ModelAdmin):
    list_display    = ['revendedor', 'pedido', 'perc_cashback', 'valor', 'data']
    list_filter     = ('revendedor', 'pedido', 'perc_cashback', 'valor', 'data')
    search_fields   = ('revendedor', 'pedido', 'perc_cashback', 'valor', 'data')
    ordering        = ['revendedor', 'pedido', 'perc_cashback', 'valor', 'data']
    save_as = True

admin.site.register(CashBackRevendedor, CashBackRevendedorAdmin)