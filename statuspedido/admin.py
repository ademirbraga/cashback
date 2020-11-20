from django.contrib import admin
from .models import Status

class StatusAdmin(admin.ModelAdmin):
    list_display = ['status']
    save_as = True

admin.site.register(Status, StatusAdmin)
