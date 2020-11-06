from django.shortcuts import render, HttpResponse
from django.views.generic import View
from core.views import logado, UserPermission
from dxm_oee_modulo.dxm import Servico, servico

class IndexView(View):
    def get(self,request):
        dados = servico.oee
        #dados=3
        return logado('oee/index.html',request,dados=dados,titulo='Fabrica',nivel_min=3)

def conjunto_linhas(request):
    if UserPermission(request, 3):
        dado = ''
        for l in servico.oee.linhas:
            dado = f'{dado}{{\"nome\":\"{l.nome}\",\"estado\":\"{l.estado}\",\"oee\":{l.oee}}},'
        dado = dado[0:len(dado)-1]
        print(dado)
        return HttpResponse('['+dado+']')
    else:
        return HttpResponse('falha')
    
