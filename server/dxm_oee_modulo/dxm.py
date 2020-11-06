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
            else:
                self.statusTcp = 'dxm OffLine'
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
        self.__contProssTCP = False 
        self.dxm.close()

servico = Servico(oee)


#"""
def leitu():
    while True:
        if servico.statusTcp.find('OnLine')>=0:
            print(f'contador 1: {servico.oee.linhas[0].cont_in}')
            print(f'contador 2: {servico.oee.linhas[0].cont_out}')
            print(f'estado: {servico.oee.linhas[0].maq_sts}')   
            print(f'velo esp: {servico.oee.linhas[0].vel_esp}')
            print('')
        else:
            sleep(4)
        print(f'Estado: {servico.statusTcp}',servico.oee.DXM_Endress,sep='\t')
        print('')
        sleep(2)
#"""

#l = Thread(target=leitu)
#l.start()
#leitu()