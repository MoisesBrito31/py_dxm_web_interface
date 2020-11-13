from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from core.views import logado, UserPermission
from dxm_oee_modulo.dxm import servico, Modbus, Protocolo
from dxm_oee_modulo.protocolo.mapa import Evento
from time import sleep
from datetime import datetime
import json


class IndexView(View):
    def get(self,request):
        dado = servico.oee
        return logado('config/index.html',request,titulo='configurar DXM',dados=dado,nivel_min=1)

class TurnosView(View):
    def get(self,request):
        dado = servico.mapa.turnos
        return render(request,'config/turno.html',context={'dados':dado})
        #return logado('config/turno.html',request,titulo='Turnos',dados=dado,nivel_min=2)

class MapIoView(View):
    def get(self, request):
        dado = servico.mapa.blocos
        s = json.dumps(para_dict(dado))
        #s = s.replace('&quot;','\"')
        print(s)
        return render(request,'config/mapio.html',context={
            'json':s,
            'dados':dado,
            'msg':'ok'
        })
        #return logado('config/mapio.html',request,context={'json':json},titulo='Mapa Io',dados=dado,nivel_min=1)

class AddTurno(View):
    def post(self,request):
        try:
            recb = str(request.POST['time']).split(':') 
            h = int(recb[0])
            m = int(recb[1])
            time = datetime(1,1,1,h,m,0)
            nome = str(request.POST['nome'])
            index = int(request.POST['index'])
            e = Evento(nome,time,id=index)
            servico.mapa.turnos.append(e)
            #servico.mapa.salva()
            return logado('config/turno.html',request,titulo='Turnos', msg='executado', dados=servico.mapa.turnos)
        except:
            return logado('config/turno.html',request,titulo='Turnos', msg='falha', dados=servico.mapa.turnos)

class DeleteTurno(View):
    def post(self,request,value):
        try:
            servico.mapa.turnos.remove(servico.mapa.turnos[value])
            for x in range(len(servico.mapa.turnos)):
                servico.mapa.turnos[x].id = x
            #servico.mapa.salva()
            return logado('config/turno.html',request,titulo='Turnos', msg='executado', dados=servico.mapa.turnos)
        except:
            return logado('config/turno.html',request,titulo='Turnos', msg='falha', dados=servico.mapa.turnos)

class EditTurno(View):
    def post(self,request,value):
        try:
            recb = str(request.POST['time']).split(':') 
            h = int(recb[0])
            m = int(recb[1])
            time = datetime(1,1,1,h,m,0)
            nome = str(request.POST['nome'])
            servico.mapa.turnos[value].nome = nome
            servico.mapa.turnos[value].start = time
            #servico.mapa.salva()
            return logado('config/turno.html',request,titulo='Turnos', msg='executado', dados=servico.mapa.turnos)
        except:
            return logado('config/turno.html',request,titulo='Turnos', msg='falha', dados=servico.mapa.turnos)

def getRelogio(request):
    if UserPermission(request,nivel_min=1):
        dxm = Protocolo(servico.oee.DXM_Endress)
        ret = dxm.getRelogio()
        return HttpResponse(f'{ret.day}/{ret.month}/{ret.year}  {ret.hour}:{ret.minute}:{ret.second}')
    else:
        return HttpResponse('falha')

def setRelogio(request):
    if UserPermission(request,nivel_min=1):
        dxm = Protocolo(servico.oee.DXM_Endress)
        ret = dxm.setRelogio()
        if ret == True:
            return HttpResponse('ok')
        else:
            return HttpResponse('falha')
    else:
        return HttpResponse('falha')


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

class Set_dados(View):
    def post(self,request,valor):
        try:
            recb = str(request.POST['agendado']).split(':') 
            h = int(recb[0])
            m = int(recb[1])
            agendado = h*60+m
            forma = int(request.POST['forma'])
            nome = str(request.POST['nome'])
            vel_esp = int(request.POST['vel_esp'])
            print(f'{valor}: {agendado}, {forma}, {nome}, {vel_esp}')
            servico.dxm.write_multiple_registers(107+valor*13,[vel_esp])
            sleep(1)
            servico.dxm.write_multiple_registers(109+valor*13,[forma])
            sleep(1)
            servico.dxm.write_multiple_registers(110+valor*13,[agendado])
            sleep(1)
            servico.oee.linhas[valor].nome = nome
            servico.oee.salva()
            return logado('config/index.html',request,titulo='configurar DXM', msg='executado', dados=servico.oee)
        except:
            return logado('config/index.html',request,titulo='configurar DXM', msg='falha', dados=servico.oee)

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

def para_dict(obj):
    # Se for um objeto, transforma num dict
    if hasattr(obj, '__dict__'):
        obj = obj.__dict__

    # Se for um dict, lê chaves e valores; converte valores
    if isinstance(obj, dict):
        return { k:para_dict(v) for k,v in obj.items() }
    # Se for uma lista ou tupla, lê elementos; também converte
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [para_dict(e) for e in obj]
    # Se for qualquer outra coisa, usa sem conversão
    else: 
        return obj