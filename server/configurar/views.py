from django.shortcuts import render, HttpResponse
from django.views.generic import View
from core.views import logado, UserPermission
from dxm_oee_modulo.dxm import servico, Modbus


class IndexView(View):
    def get(self,request):
        dado = servico.oee
        return logado('configurar/index.html',request,titulo='configurar DXM',dados=dado,nivel_min=1)


def online(request):
    if UserPermission(request,nivel_min=3):
        if servico.statusTcp.find('OnLine')>=0:
            return HttpResponse(f'{{\"dxm_online\":\"True\"}}')
        else:
            return HttpResponse(f'{{\"dxm_online\":\"False\"}}')
    else:
        return HttpResponse('falha')
