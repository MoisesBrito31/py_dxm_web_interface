from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from core.views import logado, UserPermission
from oee.models import Hist
from dxm_oee_modulo.dxm import servico, Modbus, Protocolo
from dxm_oee_modulo.protocolo.mapa import Evento
from dxm_oee_modulo.oee_modulo.script import Script
from time import sleep
from datetime import datetime, timedelta
import json
from collections import namedtuple


class IndexView(View):
    def get(self,request):
        dado = servico.oee
        return logado('config/index.html',request,titulo='configurar DXM',dados=dado,nivel_min=1)

class TurnosView(View):
    def get(self,request):
        dado = servico.mapa.turnos
        return logado('config/turno.html',request,titulo='Turnos',dados=dado,nivel_min=2)

class MapIoView(View):
    def get(self, request):
        dado = servico.mapa.blocos
        s = json.dumps(para_dict(dado))
        return logado('config/mapio.html',request,context={
                'json':s,
                'modo':servico.mapa.modo
            },titulo='Mapa Io',dados=dado,nivel_min=1)
    def post(self,request):
        try:
            ret = request.POST['json']
            dic = json.loads(ret)
            for x in range(len(servico.mapa.blocos)):
                for y in range(len(servico.mapa.blocos[x].regList)):
                    servico.mapa.blocos[x].regList[y].slaveID = dic[x]['regList'][y]['slaveID']
                    servico.mapa.blocos[x].regList[y].reg = dic[x]['regList'][y]['reg']
                    servico.mapa.blocos[x].regList[y].dword = dic[x]['regList'][y]['dword']
                    servico.mapa.blocos[x].regList[y].ativo = dic[x]['regList'][y]['ativo']
            servico.mapa.salva()
            scr = Script(servico.oee.linhas,servico.mapa,servico.oee.tickLog)
            scr.salvaArquivo()
            dado = servico.mapa.blocos
            s = json.dumps(para_dict(dado))
            return logado('config/mapio.html',request,context={
                'json':s,
                'modo':servico.mapa.modo
            },titulo='Mapa Io',dados=dado,nivel_min=1,msg='executado')
        except Exception as ex:
            return logado('config/mapio.html',request,context={
                'json':s,
                'modo':servico.mapa.modo
            },titulo='Mapa Io',dados=dado,nivel_min=1,msg='falha')

class DxmConfigView(View):
    def get(self,request):
        return logado('config/dxmconfig.html',request,titulo='Programar DXM')

class ResetView(View):
    def get(self,request):
        dxm = Protocolo(servico.oee.DXM_Endress)
        estado = 'Bloqueado'
        if dxm.fileExist('OEE.sb'):
            estado = 'Bloqueado'
        else:
            estado = 'Desbloqueado'
        return render(request,'config/reset.html',context={
            'estado':estado
        })

class MapAltModo(View):
    def post(self,request):
        m = int(request.POST['modo'])
        servico.mapa.modo = m
        return redirect('/config/mapio')

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
            servico.mapa.salva()
            return logado('config/turno.html',request,titulo='Turnos', msg='executado', dados=servico.mapa.turnos)
        except:
            return logado('config/turno.html',request,titulo='Turnos', msg='falha', dados=servico.mapa.turnos)

class DeleteTurno(View):
    def post(self,request,value):
        try:
            servico.mapa.turnos.remove(servico.mapa.turnos[value])
            for x in range(len(servico.mapa.turnos)):
                servico.mapa.turnos[x].id = x
            servico.mapa.salva()
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
            servico.mapa.salva()
            return logado('config/turno.html',request,titulo='Turnos', msg='executado', dados=servico.mapa.turnos)
        except:
            return logado('config/turno.html',request,titulo='Turnos', msg='falha', dados=servico.mapa.turnos)

class Set_ip(View):
    def post(self,request):
        valor = str(request.POST['valor'])
        servico.oee.DXM_Endress = valor
        servico.close()
        servico._setupTCP()
        sleep(3)
        return redirect('/config')

class Set_linhas(View):
    def post(self,request):
        valor = int(request.POST['valor'])
        while servico.dxm.read_holding_registers(89,1)[0] != valor:
            servico.dxm.write_multiple_registers(89,[valor])
            sleep(2)
        sleep(3)
        scr = Script(servico.oee.linhas,servico.mapa,servico.oee.tickLog)
        scr.salvaArquivo()
        return redirect('/config')

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
            for x in range(len(servico.oee.linhas)):
                servico.mapa.blocos[x].nome = servico.oee.linhas[x].nome
            servico.oee.salva()
            servico.mapa.salva()
            return logado('config/index.html',request,titulo='configurar DXM', msg='executado', dados=servico.oee)
        except:
            return logado('config/index.html',request,titulo='configurar DXM', msg='falha', dados=servico.oee)

class Set_tickLog(View):
    def post(self,request):
        valor = int(request.POST['valor'])
        servico.oee.tickLog = valor
        servico.oee.salva()
        sleep(3)
        print(len(servico.oee.linhas))
        scr = Script(servico.oee.linhas,servico.mapa,valor)
        scr.salvaArquivo()
        return redirect('/config')

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
            return HttpResponse(f'{{\"dxm_online\":\"True\",\"script\":\"{servico.statusScript}\"}}')
        else:
            return HttpResponse(f'{{\"dxm_online\":\"False\",\"script\":\"{servico.statusScript}\"}}')
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

class dict_to_obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)

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

def travar(request):
    if UserPermission(request,nivel_min=1):
        dxm = Protocolo(servico.oee.DXM_Endress)
        if dxm.travar():
            return HttpResponse('ok')
        else:
            return HttpResponse('falha')
    else:
        return HttpResponse('falha')

def destravar(request):
    if UserPermission(request,nivel_min=1):
        dxm = Protocolo(servico.oee.DXM_Endress)
        if dxm.destravar():
            return HttpResponse('ok')
        else:
            return HttpResponse('falha')
    else:
        return HttpResponse('falha')

def sendScript(request):
    if UserPermission(request,nivel_min=1):
        dxm = Protocolo(servico.oee.DXM_Endress)
        if dxm.enviaArquivo('OEE.sb',''):
            return HttpResponse('ok')
        else:
            return HttpResponse('falha')
    else:
        return HttpResponse('falha')

def sendXml(request):
    if UserPermission(request,nivel_min=1):
        dxm = Protocolo(servico.oee.DXM_Endress)
        if dxm.enviaArquivo('DXM_OEE.xml',''):
            return HttpResponse('ok')
        else:
            return HttpResponse('falha')
    else:
        return HttpResponse('falha')

def fileExist(request,file):
    if UserPermission(request,nivel_min=1):
        dxm = Protocolo(servico.oee.DXM_Endress)
        if dxm.fileExist(file):
            return HttpResponse('ok')
        else:
            return HttpResponse('falha')
    else:
        return HttpResponse('falha')

def fileDelete(request,file):
    if UserPermission(request,nivel_min=1):
        dxm = Protocolo(servico.oee.DXM_Endress)
        if dxm.deleteFile(file):
            return HttpResponse('ok')
        else:
            return HttpResponse('falha')
    else:
        return HttpResponse('falha')

def fileDownload(request,file:str):
    if UserPermission(request,nivel_min=1):
        dxm = Protocolo(servico.oee.DXM_Endress)
        tipo = str(file.split('.')[1])
        arquiv = dxm.getFile(file)
        response = HttpResponse(arquiv,content_type=f'text/{tipo}')
        response['Content-Disposition'] = f'attachment; filename="{file}"'
        return response
    else:
        return HttpResponse('falha')

def baixaLog(request):
    if UserPermission(request, nivel_min=1):
        dxm = Protocolo(servico.oee.DXM_Endress)
        if servico.statusTcp.find('OnLine')>=0:
            try:
                if dxm.fileExist('sbfile1.dat') == False:
                    return HttpResponse('falha - Nenhum log existente no dxm')
                dxm.destravar()
                arqui = dxm.getFile('sbfile1.dat')
                dados = ''
                for x in arqui:
                    dados=f'{dados}{x}'
                dados = dados.replace('\n',',')
                dados = '[' + dados + ']'
                dados = dados.replace('\t','')
                dados = dados.replace(':,',':0,')
                dados = dados.replace('\'','')
                dados = dados.replace('\n','')
                dados = dados.replace(',}','}')
                dados = dados.replace(',]',']')
                arm = open(f'file.dat','w')
                arm.write( dados.replace(',{',',\n{'))
                arm.close()
                j = json.loads(dados)
                banco=[]
                for x in j:
                    banco.append(dict_to_obj(x))
                for x in banco:
                    calender = datetime.strptime(x.time,'%Y-%m-%d %H:%M:%S')
                    H = Hist(linha=x.id,time=calender-timedelta(hours=3),
                    oee=x.oee,dis=x.dis,q=x.q,per=x.per,vel_atu=x.vel_atu,bons=x.bons,
                    ruins_total=x.ruins_total,t_par=x.t_par,t_prod=x.t_prod)                    
                    H.save()
                    print(f'salvei o historico {H.id}')
                dxm.deleteFile('sbfile1.dat')  
                dxm.travar()         
                return HttpResponse('ok')
            except Exception as ex:
                return HttpResponse(f'falha - {str(ex)}')
        else:
            return HttpResponse('falha - DXM esta desconectado')
    else:
        return HttpResponse('falha - Você não permissão para executar esta ação')