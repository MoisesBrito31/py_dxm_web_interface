from time import sleep
from threading import Thread
from pyModbusTCP.client import ModbusClient as Modbus
from dxm_oee_modulo.oee_modulo.oee import OEE
from dxm_oee_modulo.protocolo.mapa import Mapa



mapa = Mapa.carrega('store','base.mapa')
oee = OEE.carrega('store','OEE.bin')




class Servico():
    oee = OEE(1)
    __contProssTCP = True
    __controleRead = True
    statusTcp = 'iniciado...'
    execSetup = False
    lendo = False

    def __init__(self, OEE:oee):
        self.oee = oee
        self.dxm = Modbus(host=self.oee.DXM_Endress,port=502,auto_open=True)
        self.dxm.open()
        self._setupTCP()


    def ler(self):
        try:
            linha = self.dxm.read_holding_registers(89,1)[0]
            #print(f'linha: {linha}')
            if linha:
                if linha > 0:
                    self.oee.alteraLinhas(linha)
                self.oee.emulador = self.dxm.read_holding_registers(88,1)[0]
                for x in range(len(self.oee.linhas)):
                    self.oee.linhas[x].insert_dinamics(self.dxm.read_holding_registers(0+x*5,5))
                    self.oee.linhas[x].insert_calculadas(self.dxm.read_holding_registers(100+x*13,13))            
                sleep(1)
                return True
            else:
                print('falha na leitura 1')
                sleep(2)
                return False
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
                sleep(5)
       
    def _setupTCP(self):
        print('setupTcp...')
        self.__controleRead = False
        sleep(4)
        try:
            """
            try:
                if self.dxm.is_open():
                    self.dxm.close()
            except:
                pass
            
            self.dxm = Modbus(host=self.oee.DXM_Endress,port=502)
            self.dxm.open()
            """
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
                sleep(5)
                #if not self.lendo:
                self.__controleRead = True
                self.th = Thread(target=self._readTCP)
                self.th.start()
        except Exception as ex:
            self.statusTcp = 'dxm OffLine'
            print(f'falha no setup:  {str(ex)}')
            sleep(5)
            #if not self.lendo:
            self.__controleRead = True
            self.th = Thread(target=self._readTCP)
            self.th.start()
                
    
    def close(self):
        self.__controleRead = False 
        self.dxm.close()

servico = Servico(oee)



def leitu():
    controle = True
    while controle:
        cmd = input()
        if cmd == 'exit':
            servico.close()
            controle = False
        if cmd == 'sts':
            print(servico.statusTcp)
    print('fim...')


l = Thread(target=leitu)
l.start()
