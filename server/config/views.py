from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from core.views import logado, UserPermission
from dxm_oee_modulo.dxm import servico, Modbus
from time import sleep


class IndexView(View):
    def get(self,request):
        dado = servico.oee
        return render(request,'configurar/index.html',context={'dados':dado})
        #return logado(,request,titulo='configurar DXM',dados=dado,nivel_min=1)


class Set_ip(View):
    def post(self,request):
        valor = str(request.POST['valor'])
        servico.oee.DXM_Endress = valor
        servico.close()
        servico._setupTCP()
        sleep(3)
        return HttpResponseRedirect('/config')

class Set_linhas(View):
    def post(self,request):
        valor = int(request.POST['valor'])
        while servico.dxm.read_holding_registers(89,1)[0] != valor:
            servico.dxm.write_multiple_registers(89,[valor])
            sleep(2)
        sleep(3)
        return HttpResponseRedirect('/config')

class Set_tickLog(View):
    def post(self,request):
        valor = int(request.POST['valor'])
        print(valor)
        servico.oee.tickLog = valor
        sleep(3)
        return HttpResponseRedirect('/config')

def emula(request,valor):
    if UserPermission(request,nivel_min=1):
        servico.dxm.write_multiple_registers(88,[valor])
        sleep(2)
        return HttpResponse('ok')
    else:
        return HttpResponse('erro')

def zerarLinha(request,valor):
    if UserPermission(request, nivel_min=1):
        servico.dxm.write_multiple_registers(108+valor*13,[1])
        sleep(3)
        return HttpResponse('ok')
    else:
        return HttpResponse('você não possui permissão')

def online(request):
    if UserPermission(request,nivel_min=3):
        if servico.statusTcp.find('OnLine')>=0:
            return HttpResponse(f'{{\"dxm_online\":\"True\"}}')
        else:
            return HttpResponse(f'{{\"dxm_online\":\"False\"}}')
    else:
        return HttpResponse('falha')
