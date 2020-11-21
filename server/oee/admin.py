from django.contrib import admin
from .models import Hist

@admin.register(Hist)
class HistAdmin(admin.ModelAdmin):
    list_display = ('id','linha', 'time', 'oee', 'dis', 'q', 'per')
