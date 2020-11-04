from datetime import datetime
import pickle
import os

class Evento():
    id = 0
    end = datetime.now()
    nome = 'sem nome'
    regControle = 91
    start = datetime.now()
    on = 0
    off = 0
    exclude = 0
    days = "SMTWHFR"

    def __init__(self,nome:str,start:datetime,id=0,regControle=91,on=0,off=0,exclude=0,days="SMTWHFR"):
        self.id = id
        self.nome = nome
        self.regControle = regControle
        self.start = start
        self.end = datetime(start.year,start.month,start.day,start.hour,start.minute+1,start.second)
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
    nome = "sem nome"
    regList = []

    def __init__(self,nome,regList):
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

    def __init__(self, nome='base', nomeArquivo='base.mapa',pasta="",blocos=[],turnos=[],qntEquip=0, inicia=False):
        self.pasta = pasta
        self.nome = nome
        self.nomeArquivo = nomeArquivo
        self.blocos =blocos
        self.turnos = turnos
        self.qntEquip = qntEquip
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

        except Exception as e:
            print(f'falha ao salvar mapa{str(e)}')

    def alteraQtdEquip(self,num:int):
        if num > self.qntEquip:
            regs =[]
            a = Reg(17)
            for x in range(3):
                regs.append(a)
            for x in range(num-self.qntEquip):
                b = Bloco(f'equipamento {x}',regs)
                self.blocos.append(b)
            self.qntEquip = len(self.blocos)
            self.salva()
            return True
        if num < self.qntEquip:
            self.blocos = self.blocos[:num]
            self.qntEquip = len(self.blocos)
            self.salva()
            return True
        return False

    def alteraNomeEquip(self,nomes:list):
        for x in range(len(nomes)):
            self.blocos[x].nome = nomes[x]

    def _criarArquivo(self):
        blocos = []
        turnos = []
        e = Evento('Turno 1',datetime(2000,1,1,0,0,0))
        r = Reg(17)
        r1 = Reg(18)
        r2 = Reg(19)
        b = Bloco('Equipamento 1',[r,r1,r2])
        blocos.append(b)
        turnos.append(e)
        self.blocos = blocos
        self.turnos = turnos
        self.qntEquip = 1
        self.salva()


