from time import sleep
from threading import Thread
from pyModbusTCP.client import ModbusClient as Modbus
from dxm_oee_modulo.oee_modulo.oee import OEE
from dxm_oee_modulo.protocolo.mapa import Mapa
from dxm_oee_modulo.protocolo.protocolo import Protocolo
from datetime import datetime, timedelta
from oee.models import HistV

mapa = Mapa.carrega('','base.mapa')
oee = OEE.carrega('','OEE.data')


class Servico():
    oee = OEE(1)
    __contProssTCP = True
    __controleRead = True
    statusTcp = 'dxm OffLine'
    statusScript = 'ok'
    execSetup = False
    lendo = False

    def __init__(self, OEE:oee, Mapa:mapa):
        self.oee = oee
        self.mapa = mapa

    def ler(self):
        try:
            linha = self.dxm.read_holding_registers(89,1)[0]
            #print(f'linha: {linha}')
            if linha:
                if linha > 0:
                    self.oee.alteraLinhas(linha)
                    if self.mapa.alteraQtdEquip(linha):
                        for x in range(len(self.oee.linhas)):
                            self.mapa.blocos[x].nome = self.oee.linhas[x].nome
                self.oee.emulador = self.dxm.read_holding_registers(88,1)[0]
                for x in range(len(self.oee.linhas)):
                    self.oee.linhas[x].insert_dinamics(self.dxm.read_holding_registers(0+x*5,5))
                    self.oee.linhas[x].insert_calculadas(self.dxm.read_holding_registers(100+x*13,13))            
                sleep(1)
                self.statusScript = 'ok'
                return True
            else:
                self.statusScript = 'falha'
                print('falha na leitura DXM Descalibrado')
                sleep(2)
                return True
        except Exception as ex:
            print(f'falha na leitura 2 - {str(ex)}')
            sleep(2)
            return False

    def _readTCP(self):
        while self.__controleRead== True:
            if self.ler():
                self.statusTcp = 'dxm OnLine'
                self.oee.DXM_insertOnLine()
            else:
                self.statusTcp = 'dxm OffLine'
                self.oee.DXM_insertFalha()
                sleep(3)
       
    def _setupTCP(self):
        print('setupTcp...')
        self.__controleRead = False
        sleep(4)
        try:
            self.dxm = Modbus(host=self.oee.DXM_Endress,port=502,auto_open=True)
            self.dxm.open()
            retorno = self.dxm.read_holding_registers(0,1)
            if retorno:
                self.statusTcp = 'dxm OnLine'
                if self.ler():
                    for l in range(len(self.oee.linhas)):
                        self.oee.linhas[l].id = l
                    self.oee.salva()
                #if not self.lendo:
                self.__controleRead = True
                self.th = Thread(target=self._readTCP)
                self.th.start()    
            else:
                self.statusTcp = 'dxm OffLine'
                sleep(3)
                #if not self.lendo:
                self.__controleRead = True
                self.th = Thread(target=self._readTCP)
                self.th.start()
        except Exception as ex:
            self.statusTcp = 'dxm OffLine'
            print(f'falha no setup:  {str(ex)}')
            sleep(3)
            #if not self.lendo:
            self.__controleRead = True
            self.th = Thread(target=self._readTCP)
            self.th.start()
                
    
    def close(self):
        self.__controleRead = False 
        self.dxm.close()

class Ciclo():
    def __init__(self):
        self.ctl_log = True
        self.Th = Thread(target=self.cicloLog)
    
    def cicloLog(self):
        sleep(10)
        time = 0
        from config.views import Hist, dict_to_obj, json
        while self.ctl_log:
            #print(f'time: {time} precisa: {servico.oee.tickLog*60+60}  CTL: {self.ctl_log}')
            if time > servico.oee.tickLog*60+60:
                time=0
                dxm = Protocolo(servico.oee.DXM_Endress)
                if servico.statusTcp.find('OnLine')>=0:
                    try:
                        if dxm.fileExist('sbfile1.dat') == False:
                            print('falha - Nenhum log existente no dxm')
                        else:
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
                            print(f'executado o log automatico - {datetime.now()}')
                        #dataLog2 contendo o fechamento do turno:
                        if dxm.fileExist('sbfile2.dat') == False:
                            print('falha - Nenhum log de turno existente no dxm')
                        else:
                            dxm.destravar()
                            arqui = dxm.getFile('sbfile2.dat')
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
                            arm = open(f'file2.dat','w')
                            arm.write( dados.replace(',{',',\n{'))
                            arm.close()
                            j = json.loads(dados)
                            banco=[]
                            for x in j:
                                banco.append(dict_to_obj(x))
                            for x in banco:
                                calender = datetime.strptime(x.time,'%Y-%m-%d %H:%M:%S')
                                HV = HistV(equipamento=x.id,data=calender-timedelta(hours=3),valor=int(x.vel_med))                    
                                HV.save()
                                print(f'salvei o historico {HV.id}')
                            dxm.deleteFile('sbfile2.dat')  
                            dxm.travar() 
                            print(f'executado o log automatico - {datetime.now()}') 
                    except Exception as ex:
                        print(f'falha - {str(ex)}')
                else:
                    print('falha, dxm OffLine')
            time+=1
            sleep(1)

    def start(self):
        self.Th.start()

    def close(self):
        self.ctl_log=False

servico = Servico(oee,mapa)

ciclo = Ciclo()

def leitu():
    servico._setupTCP()
    ciclo.start()
    controle = True
    while controle:
        cmd = input()
        if cmd == 'exit':
            ciclo.close()
            servico.close()
            controle = False
        if cmd == 'sts':
            print(servico.statusTcp)
    print('fim...')




l = Thread(target=leitu)
l.start()
