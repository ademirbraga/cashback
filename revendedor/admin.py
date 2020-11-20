from django.contrib import admin
from .models import Revendedor

class RevendedorAdmin(admin.ModelAdmin):
    list_display    = ['nome', 'cpf', 'email']
    list_filter     = ('nome', 'cpf', 'email')
    search_fields   = ('nome', 'cpf', 'email')
    ordering        = ['nome', 'cpf', 'email']
    save_as = True

admin.site.register(Revendedor, RevendedorAdmin)
