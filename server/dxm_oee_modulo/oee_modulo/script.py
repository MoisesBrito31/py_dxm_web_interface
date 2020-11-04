from protocolo.mapa import Mapa
from .oee import Linha

class Script:
    def __init__(self):
        self.pasta = ''
        self.nomeArquivo = 'OEE.sb'
        self.arquivo = f'{self.pasta}{self.nomeArquivo}'
        self.buffer = []
        self.linhas = []
        self.mapa:Mapa
        self.log = 60
        self.carregaArquivo()
    
    def carregaArquivo(self):
        try:
            arqui = open(self.arquivo,'r')
            self.buffer = arqui.read()
            arqui.close()
            return True
        except:
            return False

    def salvaArquivo(self):
        try:
            self.copilaBuffer()
            arq = open(self.arquivo,'w')
            arq.write(self.buffer)
            arq.close()
            return True
        except:
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
                ret = f'{ret}NODE[{x}]={int(self.Mapa.blocos[x].regList[0].reg/16)}\r'
            except:
                pass
    def subBufferFim(self):
        index = self.arquivo.find("'inicio")
        return self.arquivo[index:]
