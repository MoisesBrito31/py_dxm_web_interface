from django.contrib import admin
from .models import Hist, Linha, HistV

@admin.register(Hist)
class HistAdmin(admin.ModelAdmin):
    list_display = ('id','linha', 'time', 'oee', 'dis', 'q', 'per')

@admin.register(Linha)
class LinhaAdmin(admin.ModelAdmin):
    list_display = ('id','index','nome')

@admin.register(HistV)
class HistVAdmin(admin.ModelAdmin):
    list_display = ('id','data', 'equipamento', 'valor')

