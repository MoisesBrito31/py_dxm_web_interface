from django.shortcuts import render
from django.views.generic import View
from core.views import logado

class IndexView(View):
    def get(self,request):
        return logado('oee/index.html',request,titulo='Fabrica',nivel_min=3)
