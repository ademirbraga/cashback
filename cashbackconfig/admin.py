from django.contrib import admin
from .models import CashBack

class CashBackAdmin(admin.ModelAdmin):
    list_display    = ['valor_min', 'valor_max', 'percentual']
    list_filter     = ('valor_min', 'valor_max', 'percentual')
    search_fields   = ('valor_min', 'valor_max', 'percentual')
    ordering        = ['valor_min', 'valor_max', 'percentual']
    save_as = True

admin.site.register(CashBack, CashBackAdmin)
