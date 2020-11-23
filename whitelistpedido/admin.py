from django.contrib import admin
from .models import WhiteListPedido


class WhiteListPedidoAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'ativo']
    list_filter = ('cpf', 'ativo')
    search_fields = ('cpf', 'ativo')
    ordering = ['cpf', 'ativo']
    save_as = True


admin.site.register(WhiteListPedido, WhiteListPedidoAdmin)
