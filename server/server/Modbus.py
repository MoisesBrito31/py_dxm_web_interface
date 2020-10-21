from time import sleep
from pyModbusTCP.client import ModbusClient as Modbus


class ModbusDados():
    dados = 'None'

    def __init__(self, ip):
        self.ip = ip
        self.dxm = Modbus(host=ip, port=502)
        self.cicloLeitura()

    def reconect(self):
        try:
            self.dxm = Modbus(host=self.ip, port=502)
            self.dxm.open()
            self.state = 'ok'
        except Exception as ex:
            self.state = f'falha -{str(ex)}'

    def ler(self):
        if self.dxm.is_open():
            self.dados = self.dxm.read_holding_registers(1, 5)
            self.state = 'ok'
        else:
            self.state = 'falha -comunicação perdida'

    def cicloLeitura(self):
        while True:
            if self.dxm.is_open() and self.dados != 'None':
                self.ler()
                print(self.dados)
                sleep(1)
            else:
                self.reconect()
                print('Reconectando...')
                sleep(5)
