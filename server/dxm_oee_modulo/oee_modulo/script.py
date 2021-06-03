#from protocolo.mapa import Mapa
#from .oee import Linha

class Script:
    def __init__(self, linhas, mapa, log, pasta='', nomeArquivo='OEE.sb'):
        self.pasta = pasta
        self.nomeArquivo = nomeArquivo
        self.arquivo = f'{self.pasta}{self.nomeArquivo}'
        self.buffer = []
        self.linhas = linhas
        self.mapa = mapa
        self.log = log
        self.carregaArquivo()
    
    def carregaArquivo(self):
        try:
            arqui = open(self.arquivo,'r')
            self.buffer = arqui.read()
            arqui.close()
            return True
        except:
            print('Falha ao carregar o arquivo OEE.sb')
            return False

    def salvaArquivo(self):
        try:
            self.copilaBuffer()
            arq = open(self.arquivo,'w')
            arq.write(self.buffer)
            arq.close()
            return True
        except:
            print('falha ao salvar o arquivo OEE.sb')
            return False

    def copilaBuffer(self):
        temp1 = self.subBufferIni()
        temp2 = self.subBufferFim()
        self.buffer = temp1+temp2

    def subBufferIni(self):
        ret = f'linhas={len(self.linhas)}\r'
        for x in range(len(self.linhas)):
            ret = f'{ret}vel_esp[{x}]={self.linhas[x].vel_esp}\r'
            ret = f'{ret}forma[{x}]={self.linhas[x].forma}\r'
            ret = f'{ret}t_p_prog[{x}]={self.linhas[x].t_p_prog}\r'
            try:
                ret = f'{ret}NODE[{x}]={int(self.mapa.blocos[x].regList[0].reg/16)}\r'
                ret = f'{ret}SID0[{x}]={int(self.mapa.blocos[x].regList[0].slaveID)}\r'
                ret = f'{ret}REG0[{x}]={int(self.mapa.blocos[x].regList[0].reg)}\r'
                ret = f'{ret}DW0[{x}]={int(self.mapa.blocos[x].regList[0].dword)}\r'
                ret = f'{ret}SID1[{x}]={int(self.mapa.blocos[x].regList[1].slaveID)}\r'
                ret = f'{ret}REG1[{x}]={int(self.mapa.blocos[x].regList[1].reg)}\r'
                ret = f'{ret}DW1[{x}]={int(self.mapa.blocos[x].regList[1].dword)}\r'
                ret = f'{ret}DW2[{x}]={int(self.mapa.blocos[x].regList[2].dword)}\r'
                """
                ret = f'{ret}REG0[{x}]={int(self.mapa.blocos[x].regList[0].reg)+int(self.mapa.blocos[x].regList[0].slaveID)*10000}\r'
                ret = f'{ret}DWORD0[{x}]={int(self.mapa.blocos[x].regList[0].dword)}\r'
                ret = f'{ret}REG1[{x}]={int(self.mapa.blocos[x].regList[1].reg)+int(self.mapa.blocos[x].regList[1].slaveID)*10000}\r'
                ret = f'{ret}DWORD1[{x}]={int(self.mapa.blocos[x].regList[1].dword)}\r'
                """
                
            except:
                pass
        ret = f'{ret}trig_log={self.log}\r'
        return ret
    def subBufferFim(self):
        index = self.buffer.find("'inicio")
        return self.buffer[index:]
