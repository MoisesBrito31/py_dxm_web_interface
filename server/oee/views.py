from django.shortcuts import render
from django.views.generic import View
from core.views import logado
from dxm_oee_modulo.dxm import Servico, servico

class IndexView(View):
    def get(self,request):
        dados = servico.oee
        #dados=3
        return logado('oee/index.html',request,dados=dados,titulo='Fabrica',nivel_min=3)
