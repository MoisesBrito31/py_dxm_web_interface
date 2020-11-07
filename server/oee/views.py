from django.shortcuts import render, HttpResponse
from django.views.generic import View
from core.views import logado, UserPermission
from dxm_oee_modulo.dxm import Servico, servico, Modbus

class IndexView(View):
    def get(self,request):
        dados = servico.oee
        #dados=3
        return logado('oee/index.html',request,dados=dados,titulo='Fabrica',nivel_min=3)

class LinhaView(View):
    def get(self,request,id):
        print(id)
        l = servico.oee.linhas[id]
        return logado('oee/linha.html',request,dados=l,titulo=l.nome, nivel_min=3)

def get_linha(request,id):
    if UserPermission(request, 3):
        l = servico.oee.linhas[id]
        ret = f'{{\"nome\":\"{l.nome}\",\"estado\":\"{l.estado}\",\"oee\":{l.oee},\"dis\":{l.dis},\"q\":{l.q},\"per\":{l.per}, \"t_prod\":{l.t_prod},\"t_par\":{l.t_par},\"t_p_prog\":{l.t_p_prog},\"cont_in\":{l.cont_in},\"cont_out\":{l.cont_out},\"vel_atu\":{l.vel_atu},\"vel_esp\":{l.vel_esp}}}'
        return HttpResponse(ret)
    else:
        return HttpResponse('falha')

def set_vel_esp(request,index,valor):
    if UserPermission(request, 1):
        try:          
            servico.dxm.write_multiple_registers(107+index*13,[valor])
            return HttpResponse('ok')
        except Exception as ex:
            return HttpResponse(str(ex))
    else:
        return HttpResponse('falha') 

def set_forma(request,index,valor):
    if UserPermission(request, 1):
        try:      
            servico.dxm.write_multiple_registers(109+index*13,[valor])
            return HttpResponse('ok')
        except Exception as ex:
            return HttpResponse(str(ex))
    else:
        return HttpResponse('falha') 

def set_t_p_prog(request,index,valor):
    if UserPermission(request, 1):
        try:      
            servico.dxm.write_multiple_registers(110+index*13,[valor])
            return HttpResponse('ok')
        except Exception as ex:
            return HttpResponse(str(ex))
    else:
        return HttpResponse('falha') 

def conjunto_linhas(request):
    if UserPermission(request, 3):
        dado=''
        for l in servico.oee.linhas:
            dado = f'{dado}{{\"nome\":\"{l.nome}\",\"estado\":\"{l.estado}\",\"oee\":{l.oee}}},'
        dado = dado[0:len(dado)-1]
        return HttpResponse('['+dado+']')
    else:
        return HttpResponse('falha')
    
