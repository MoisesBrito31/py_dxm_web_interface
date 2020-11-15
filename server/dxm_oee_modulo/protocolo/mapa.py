from datetime import datetime
import pickle
import os
from .xml import Xml

class Evento():
    id = 0
    end = datetime.now()
    nome = 'sem nome'
    regControle = 91
    start = datetime.now()
    on = 1
    off = 0
    exclude = 0
    days = "SMTWHFR"

    def __init__(self,nome:str,start:datetime,id=0,regControle=91,on=1,off=0,exclude=0,days="SMTWHFR"):
        self.id = id
        self.nome = nome
        self.regControle = regControle
        self.start = start
        self.end = datetime(start.year,start.month,start.day,start.hour,start.minute,start.second+1)
        self.on = on
        self.off = off
        self.exclude = exclude
        self.days = days

    def getXml(self):
        endH = str(self.end.hour)
        if len(endH)<2:
            endH = f'0{endH}'
        endM = str(self.end.minute)
        if len(str(endM))<2:
            endM = f'0{endM}'
        endS = str(self.end.second)
        if len(str(endS))<2:
            endS = f'0{endS}'
        startH = str(self.start.hour)
        if len(startH)<2:
            startH = f'0{startH}'
        startM = str(self.start.minute)
        if len(str(startM))<2:
            startM = f'0{startM}'
        startS = str(self.start.second)
        if len(str(startS))<2:
            startS = f'0{startS}'
        return f'<event end=\"{endH}:{endM}:{endS}\" name=\"{self.nome}\" reg=\"{str(self.regControle)}\" start=\"{startH}:{startM}:{startS}\" on=\"{str(self.on)}\" exclude=\"{str(self.exclude)}\" days=\"{self.days}\" off=\"{str(self.off)}\" />'

class Bloco():
    id = 0
    nome = "sem nome"
    regList = []

    def __init__(self,nome,regList):
        self.id = 0
        self.nome= nome
        self.regList = regList

class Reg():
    nome = ""
    id = 0
    slaveID = 1
    reg = 1
    ciclo = 1000
    dword = '1'
    ativo = True

    def __init__(self, reg, ciclo=1000,dword='1', ativo=True,id=0,slaveID=1,nome=""):
        self.nome = nome
        self.id = id
        self.slaveID = slaveID
        self.reg = reg
        self.ciclo = ciclo
        self.dword = dword
        self.ativo = ativo

class Mapa():
    nome:str
    pasta:str
    nomeArquivo:str
    blocos:Bloco = []
    turnos:Evento = []
    qntEquip:int = 0
    arquivo = ""
    modo = 0

    def __init__(self, nome='base', nomeArquivo='base.mapa',pasta="",blocos=[],turnos=[],qntEquip=0, inicia=False, modo=0):
        self.pasta = pasta
        self.nome = nome
        self.nomeArquivo = nomeArquivo
        self.blocos =blocos
        self.turnos = turnos
        self.qntEquip = qntEquip
        self.modo = modo
        if inicia:
            self._criarArquivo()

    @staticmethod
    def carrega(pasta,nomeArquivo):
        try:
            arquivo = open(f'{pasta}\{nomeArquivo}','rb')
            pic = pickle.load(arquivo)
            arquivo.close()
            return pic
        except Exception as e:
            print(f'falha ao carregar mapa {str(e)}')
            return Mapa(nomeArquivo=nomeArquivo,pasta=pasta,inicia=True)

    def salva(self):
        try:
            try:
                os.mkdir(self.pasta)
            except:
                pass
            arquivo = open(f'{self.pasta}\{self.nomeArquivo}','wb')
            pickle.dump(self,arquivo)
            arquivo.close()
            xml = Xml(self,pasta='store')
            xml.salvaArquivo()
        except Exception as e:
            print(f'falha ao salvar mapa{str(e)}')

    def alteraQtdEquip(self,num:int):
        if num > self.qntEquip:
            regs=[
                Reg(17,nome='contador de entrada',id=0),
                Reg(18,nome='contador de saída',id=1),
                Reg(19,nome='máquina parada',id=2),
            ]
            for x in range(num-self.qntEquip):
                b = Bloco(f'equipamento {self.qntEquip+x}',regs)
                self.blocos.append(b)
            self.qntEquip = len(self.blocos)
            try:
                for x in range(len(self.blocos)):
                    self.blocos[x].id = x
            except:
                pass
            self.salva()
            return True
        if num < self.qntEquip:
            self.blocos = self.blocos[:num]
            self.qntEquip = len(self.blocos)
            try:
                for x in range(len(self.blocos)):
                    self.blocos[x].id = x
            except:
                pass
            self.salva()
            return True
        try:
            for x in range(len(self.blocos)):
                self.blocos[x].id = x
        except:
            pass
        return False

    def _criarArquivo(self):
        self.blocos = [
            Bloco('Equipamento 1',[
                Reg(17,nome='contador de entrada',id=0),
                Reg(18,nome='contador de saída',id=1),
                Reg(19,nome='máquina parada',id=2),
            ]),
        ]
        self.turnos = [
            Evento('Turno 1',datetime(2000,1,1,0,0,0)),
        ]
        self.qntEquip = 1
        self.salva()


