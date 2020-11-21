from django.shortcuts import render, HttpResponse
from django.views.generic import View
from core.views import logado, UserPermission
from oee.models import Hist
from django.db.models import Q
from dxm_oee_modulo.dxm import Servico, servico, Modbus
from datetime import datetime, timedelta

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

class HistoricoView(View):
    def get(self, request, valor):
        ago = datetime.now()
        ini = datetime(ago.year,ago.month,ago.day,0,0,0)
        inis = f'{ago.year}-{ago.month}-{ago.day}T00:00:00'
        fim = datetime(ago.year,ago.month,ago.day,23,59,0)
        fims = f'{ago.year}-{ago.month}-{ago.day}T23:59:00'
        dado = Hist.objects.filter(Q(linha__exact=valor) & Q(time__gt=ini) & Q(time__lt=fim)).order_by('time')
        dadof = Hist.objects.filter(Q(linha__exact=valor) & Q(time__gt=ini) & Q(time__lt=fim)).order_by('time')
        for h in dado:      
            hora = int(h.time.hour)-3 
            if hora<0:
                hora+=23             
            h.time = f'{hora}:{h.time.minute} {h.time.day}/{h.time.month}/{h.time.year}'
        for hf in dadof:
            hora = int(hf.time.hour)-3 
            if hora<0:
                hora+=23       
            hf.time = f'{hora}:{hf.time.minute} {hf.time.day}/{hf.time.month}/{hf.time.year}'
            hf.t_par = f'{str(int(hf.t_par/60))}:{str(hf.t_par%60)}'
            hf.t_prod = f'{str(int(hf.t_prod/60))}:{str(hf.t_prod%60)}'
        return render(request,'oee/historico.html',context={
            'titulo':f'historico {servico.oee.linhas[valor].nome}',
            'linha_id':valor,
            'linha_nome':servico.oee.linhas[valor].nome,
            'dados':dado,
            'dadosf':dadof,
            'ini': inis,
            'fim': fims
        })
    def post(self,request,valor):
        inis = str(request.POST['ini'])
        fims = str(request.POST['fim'])
        ini = datetime(int(inis[0:4]),int(inis[5:7]),int(inis[8:10]),int(inis[11:13]),int(inis[14:16]),0)
        fim = datetime(int(fims[0:4]),int(fims[5:7]),int(fims[8:10]),int(fims[11:13]),int(fims[14:16]),0)
        dado = Hist.objects.filter(Q(linha__exact=valor) & Q(time__gt=ini) & Q(time__lt=fim)).order_by('time')
        dadof = Hist.objects.filter(Q(linha__exact=valor) & Q(time__gt=ini) & Q(time__lt=fim)).order_by('time')
        for h in dado:   
            hora = int(h.time.hour)-3 
            if hora<0:
                hora+=23       
            h.time = f'{hora}:{h.time.minute} {h.time.day}/{h.time.month}/{h.time.year}'
        for hf in dadof:
            hora = int(hf.time.hour)-3 
            if hora<0:
                hora+=23  
            hf.time = f'{hora}:{hf.time.minute} {hf.time.day}/{hf.time.month}/{hf.time.year}'
            hf.t_par = f'{str(int(hf.t_par/60))}:{str(hf.t_par%60)}'
            hf.t_prod = f'{str(int(hf.t_prod/60))}:{str(hf.t_prod%60)}'
        return render(request,'oee/historico.html',context={
            'titulo':f'historico {servico.oee.linhas[valor].nome}',
            'linha_id':valor,
            'linha_nome':servico.oee.linhas[valor].nome,
            'dados':dado,
            'dadosf':dadof,
            'ini': inis,
            'fim': fims
        })

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
    
