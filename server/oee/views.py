from django.shortcuts import render, HttpResponse
from django.views.generic import View
from core.views import logado, erro, UserPermission
from oee.models import Hist, Linha, HistV
from django.db.models import Q
from dxm_oee_modulo.dxm import Servico, servico, Modbus
from datetime import datetime, timedelta

class ConjuntoView(View):
    def get(self, request):
        linhas = Linha.objects.all()
        dado = []
        for x in linhas:
            dado.append(x)
        print(f'{type(dado)}, {dado}')
        return logado('oee/fabrica.html',request,dados=dado,titulo='Overview',nivel_min=3)

class IndexView(View):
    def get(self,request,valor):
        banco = Linha.objects.get(index=valor)
        qtd = 0
        nome = banco.nome
        dados = servico.oee
        for l in servico.oee.linhas:
            if l.conjunto == valor:
                qtd = qtd+1
        #dados=3
        return logado('oee/index.html',request,dados=dados,titulo='Fabrica',nivel_min=3,context={'conjunto': int(valor),
                                                                                                 'nome':nome,
                                                                                                 'qtd':qtd})

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
            hora = int(h.time.hour) -5
            if hora<0:
                hora+=23             
            h.time = f'{hora}:{h.time.minute} {h.time.day}/{h.time.month}/{h.time.year}'
        for hf in dadof:
            hora = int(hf.time.hour)-5
            if hora<0:
                hora+=23       
            hf.time = f'{hora}:{hf.time.minute} {hf.time.day}/{hf.time.month}/{hf.time.year}'
            hf.t_par = f'{str(int(hf.t_par/60))}:{str(hf.t_par%60)}'
            hf.t_prod = f'{str(int(hf.t_prod/60))}:{str(hf.t_prod%60)}'
        return logado('oee/historico.html',request,titulo=f'historico {servico.oee.linhas[valor].nome}',
                        context={
                            'linha_id':valor,
                            'linha_nome':servico.oee.linhas[valor].nome,
                            'dadosf':dadof,
                            'ini': inis,
                            'fim': fims
                        },dados=dado,nivel_min=2)
    def post(self,request,valor):
        inis = str(request.POST['ini'])
        fims = str(request.POST['fim'])
        ini = datetime(int(inis[0:4]),int(inis[5:7]),int(inis[8:10]),int(inis[11:13]),int(inis[14:16]),0)
        fim = datetime(int(fims[0:4]),int(fims[5:7]),int(fims[8:10]),int(fims[11:13]),int(fims[14:16]),0)
        dado = Hist.objects.filter(Q(linha__exact=valor) & Q(time__gt=ini) & Q(time__lt=fim)).order_by('time')
        dadof = Hist.objects.filter(Q(linha__exact=valor) & Q(time__gt=ini) & Q(time__lt=fim)).order_by('time')
        for h in dado:   
            hora = int(h.time.hour)-5 
            if hora<0:
                hora+=23       
            h.time = f'{hora}:{h.time.minute} {h.time.day}/{h.time.month}/{h.time.year}'
        for hf in dadof:
            hora = int(hf.time.hour)-5
            if hora<0:
                hora+=23  
            hf.time = f'{hora}:{hf.time.minute} {hf.time.day}/{hf.time.month}/{hf.time.year}'
            hf.t_par = f'{str(int(hf.t_par/60))}:{str(hf.t_par%60)}'
            hf.t_prod = f'{str(int(hf.t_prod/60))}:{str(hf.t_prod%60)}'
        return logado('oee/historico.html',request,titulo=f'historico {servico.oee.linhas[valor].nome}',
                        context={
                            'linha_id':valor,
                            'linha_nome':servico.oee.linhas[valor].nome,
                            'dadosf':dadof,
                            'ini': inis,
                            'fim': fims
                        },dados=dado,nivel_min=2)

class GraficoVView(View):
    def get(self,request,id):
        nomeLinha = Linha.objects.get(index=id).nome
        linhas = []
        equipamentos = []
        dados =[]
        esp = []
        turno = ""
        for l in servico.oee.linhas:
            if l.conjunto == id:
                linhas.append(l.id)
                esp.append(l.vel_esp)
                equipamentos.append({"nome":l.nome,"id":l.id})
        for eq in linhas:
            leitura = HistV.objects.filter(equipamento=eq).first()
            dados.append(leitura)
        data = dados[0].data.time()
        turnoh=[]
        turnoList=[]
        hmaisproximo = datetime.now()
        for even in servico.mapa.turnos:
            turnoList.append(even.nome)
            turnoh.append(even.start)
        hmaisproximo = min(turnoh,key=lambda h: abs(datetime.combine(datetime.min,h.time())-datetime.combine(datetime.min,data)))
        print(turnoList)
        for even in servico.mapa.turnos:
            if even.start.time()==hmaisproximo.time():
                turno = even.nome
        return logado('oee/grafico_v.html',request=request,titulo=nomeLinha,dados=dados,nivel_min=2,context={
            "conjunto":id,
            "turno":turno,
            "turnoList":turnoList,
            "linha":nomeLinha,
            "linhaIndex":id,
            "data":dados[0].data,
            "equipamentos":equipamentos,
            "esp": esp,
            "qtdEquip": len(equipamentos)
        })
    def post(self,request,id):
        turnoList=[]
        inis = str(request.POST['ini'])
        turno = str(request.POST['turno'])
        ini = datetime.strptime(inis,"%Y-%m-%d")
        dataconsulta = datetime.now()
        for eve in servico.mapa.turnos:
            turnoList.append(eve.nome)
            if eve.nome == turno:
                dataconsulta = datetime.combine(ini.date(),eve.start.time())
        consulIni = dataconsulta - timedelta(minutes=3)
        consulFim = dataconsulta + timedelta(minutes=3)
        print(f"ini: {consulIni} - hora: {ini} - fim: {consulFim}  - turno: {turno}")        
        nomeLinha = Linha.objects.get(index=id).nome
        linhas = []
        equipamentos = []
        dados =[]
        esp =[]
        for l in servico.oee.linhas:
            if l.conjunto == id:
                linhas.append(l.id)
                esp.append(l.vel_esp)
                equipamentos.append(l.nome)
        for eq in linhas:
            leitura = HistV.objects.filter(Q(equipamento__exact=eq) & Q(data__gt=consulIni) & Q(data__lt=consulFim)).order_by('data')
            for l in leitura:
                dados.append(l)
        print(turnoList)
        if dados:
            return logado('oee/grafico_v.html',request=request,titulo=nomeLinha,dados=dados,nivel_min=2,context={
                "conjunto":id,
                "inis": inis,
                "turno":turno,
                "turnoList":turnoList,
                "linha":nomeLinha,
                "linhaIndex":id,
                "data":dados[0].data,
                "equipamentos":equipamentos,
            "esp": esp
            })
        else:
            return erro(request,msg="Erro ao acessar o bando de dados, retorno nulo",titulo="Erro no banco")

def relatorio(request,inis,fims,valor):
    if UserPermission(request,nivel_min=2):
        ini = datetime(int(inis[0:4]),int(inis[5:7]),int(inis[8:10]),int(inis[11:13]),int(inis[14:16]),0)
        fim = datetime(int(fims[0:4]),int(fims[5:7]),int(fims[8:10]),int(fims[11:13]),int(fims[14:16]),0)
        dado = Hist.objects.filter(Q(linha__exact=valor) & Q(time__gt=ini) & Q(time__lt=fim)).order_by('time')
        arquiv = f"{servico.oee.linhas[valor].nome};iniciada em :;{ini}; terminado em :; {fim}\n"
        arquiv = f"{arquiv}hora;OEE;Disponibilidade;Qualidade;Preformance;Rodando;Parado;Produzido;ruins/bons;velocidade\n"
        for h in dado:
            hr = h.time.hour-5
            if hr<0:
                hr+=23 
            m = h.time.minute
            y = h.time.year
            mh = h.time.month
            d = h.time.day
            arquiv = f"{arquiv}{d}/{mh}/{y}  {hr}:{m};{h.oee}%;{h.dis}%;{h.q}%;{h.per}%;{int(h.t_prod/60)}:{h.t_prod%60};{int(h.t_par/60)}:{h.t_par%60};{h.bons};{h.ruins_total};{h.vel_atu}p/m\n"
        response = HttpResponse(arquiv,content_type=f'text/csv')
        response['Content-Disposition'] = f'attachment; filename="relatorio.csv"'
        return response
    else:
        return HttpResponse('falha')

def get_linha(request,id):
    if UserPermission(request, 3):
        l = servico.oee.linhas[id]
        ret = f'{{\"nome\":\"{l.nome}\",\"estado\":\"{l.estado}\",\"oee\":{l.oee},\"dis\":{l.dis},\"q\":{l.q},\"per\":{l.per}, \"t_prod\":{l.t_prod},\"t_par\":{l.t_par},\"t_p_prog\":{l.t_p_prog},\"cont_in\":{l.cont_in},\"cont_out\":{l.cont_out},\"vel_atu\":{l.vel_atu},\"vel_esp\":{l.vel_esp}}}'
        return HttpResponse(ret)
    else:
        return HttpResponse('falha')
    
def get_v_aovivo(request,id):
    if UserPermission(request, 3):
        ret = "["
        for l in servico.oee.linhas:
            if l.conjunto == id:
                ret=f'{ret}{{\"nome\":\"{l.nome}\",\"vel_atu\":{l.vel_atu},\"vel_esp\":{l.vel_esp}}},'
        ret = f'{ret[:len(ret)-1]}]'
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
            dado = f'{dado}{{\"id\":{l.id},\"nome\":\"{l.nome}\",\"conjunto\":{l.conjunto},\"estado\":\"{l.estado}\",\"oee\":{l.oee}}},'
        dado = dado[0:len(dado)-1]
        return HttpResponse('['+dado+']')
    else:
        return HttpResponse('falha')
    
