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
    statusTcp = 'iniciado...'
    execSetup = False

    def __init__(self, OEE:oee):
        self.oee = oee
        self.dxm = Modbus(host=self.oee.DXM_Endress,port=502)
        self.dxm.open()
        self.loop_tcp()


    def _readTCP(self):
        linha = self.dxm.read_holding_registers(89,1)[0]
        print(f' linha = {linha}')
        if linha:
            if linha > 0:
                self.oee.alteraLinhas(linha)
            self.oee.emulador = self.dxm.read_holding_registers(88,1)[0]
            for x in range(len(self.oee.linhas)):
                self.oee.linhas[x].insert_dinamics(self.dxm.read_holding_registers(0+x*5,5))
                self.oee.linhas[x].insert_calculadas(self.dxm.read_holding_registers(100+x*13,13))
            self.statusTcp = 'dxm OnLine'
            sleep(1)
        else:
            print('falha na leitura 1')
            self.statusTcp = 'dxm OffLine'
            sleep(2)
       

    def _setupTCP(self):
        print('setupTcp...')
        try:
            self.dxm.host = self.oee.DXM_Endress
            retorno = self.dxm.read_holding_registers(0,1)
            if retorno:
                self.statusTcp = 'dxm OnLine'
            else:
                self.statusTcp = 'dxm OffLine'
        except:
            print('falha no setup')
            sleep(5)
                
    
    def loop_tcp(self):
        print('inicio do loopTCP...')
        self._setupTCP()
        while self.__contProssTCP:
            print('loop >>')
            if self.statusTcp.find('OffLine')>=0 or self.execSetup == True:
               self._setupTCP()
            self._readTCP()
            print('loop <<')

    def close(self):
        self.__contProssTCP = False 
        self.dxm.close()

servico = Servico(oee)


#"""
while True:
    if servico.statusTcp.find('OnLine')>=0:
        print(f'contador 1: {servico.oee.linhas[0].cont_in}')
        print(f'contador 2: {servico.oee.linhas[0].cont_out}')
        print(f'estado: {servico.oee.linhas[0].maq_sts}')   
        print(f'velo esp: {servico.oee.linhas[0].vel_esp}')
        print('')
    print(f'Estado: {servico.statusTcp}',servico.oee.DXM_Endress,sep='\t')
    print('')
    sleep(2)
#"""
