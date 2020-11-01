from time import sleep
from threading import Thread
from pyModbusTCP.client import ModbusClient as Modbus


class Servico():
    dados = []
    dadosAux = []
    __contReadTCP = True
    __contSetupTCP = True
    __contProssTCP = True
    statusTcp = 'iniciado...'
    statusSocket = 'iniciado...'
    execSetup = False
    thrTCP = Thread()

    def __init__(self, ip):
        self.ip = ip
        for x in range(240):
            self.dados.append(0)
        self.thr = Thread(target=self._setupTCP)
        self.thr.start()

    def _readTCP(self):
        try:
            self.dadosAux = []
            temp = []
            for x in range(6):
                temp = self.dxm.read_holding_registers(0+(x*40), 40)
                for x in temp:
                    self.dadosAux.append(x)
            if len(self.dadosAux) == 240:
                self.dados = self.dadosAux
                self.statusTcp = 'dxm OnLine'
            else:
                self.statusTcp = 'dxm OffLine'
        except:
            self.statusTcp = 'dxm OffLine'

    def _setupTCP(self):
        while self.statusTcp.find('OnLine') < 0 and self.__contSetupTCP:
            print('setupTcp...', self.statusTcp.find('OnLine'), sep='\t')
            try:
                try:
                    if self.dxm.is_open():
                        self.dxm.close()
                except:
                    pass
                self.dxm = Modbus(host=self.ip, port=502)
                self.dxm.open()
                v = self.dxm.read_holding_registers(0,1)
                print(type(v), 'valor: ',v,sep='\t')
                if v:
                    print('online')
                    self.statusTcp = 'dxm OnLine'
                    self.__contProssTCP = True
                    self.__contReadTCP = True
                    self.__contSetupTCP = False
                    self.thrTCP = Thread(target=self.loop_tcp)
                    self.thrTCP.start()
                else:
                    self.statusTcp = 'dxm OffLine'
                    print('offline')
                    sleep(5)
            except:
                self.statusTcp = 'dxm OffLine'
                print('offline')
                sleep(5)

    def loop_readTCP(self):
        while self.__contReadTCP:
            self._readTCP()
            sleep(1)

    def loop_tcp(self):
        tr = Thread(target=self.loop_readTCP)
        tr.start()
        while self.__contProssTCP:
            if self.execSetup or self.statusTcp.find('OffLine')>=0:
                self.execSetup = False
                self.__contProssTCP = False
                self.__contReadTCP = False
                self.__contSetupTCP = True
                self._setupTCP()

    def close(self):
        self.__contReadTCP = False
        self.__contWriteTCP = False
        self.__contSetupTCP = False
        self.__contProssTCP = False


print('inicio...')

d = Servico('192.168.0.100')
contProg = True
while contProg:
    cmd = input('comando: ')
    if cmd == 'sts':
        # print('sts')
        print(d.statusTcp)
    if cmd == 'exit':
        # print('exit')
        d.close()
        contProg = False
    if cmd.find('ip') >= 0:
        ip = cmd.split(',')[1]
        d.ip = ip
        #print('vc digitou: {}'.format(ip))
        d.execSetup = True
    if cmd.find('rd')>=0:
        start = int(cmd.split(',')[1])
        qtd = int(cmd.split(',')[2])
        print(d.dados[start:start+qtd])
print('fim...')
