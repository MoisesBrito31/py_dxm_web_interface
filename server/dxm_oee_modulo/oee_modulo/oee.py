from datetime import datetime
import pickle
import os


class Hist():
    id:int
    time:datetime
    oee:int
    dis:int
    q:int
    per:int
    vel_atu:int
    bons:int
    ruins_total:int
    t_prod:int
    t_par:int

    def __init__(self,oee,dis,q,per,produz,id=0,ruins=0,vel=0,bons=0,t_prod=0,t_par=0,time=datetime.now()):
        self.time=time
        self.id=id
        self.oee=oee
        self.dis=dis
        self.q=q
        self.per=per
        self.vel_atu=vel
        self.bons=bons
        self.ruins_total=ruins
        self.t_prod=t_prod
        self.t_par=t_par

class Linha():
    id:int
    nome:str
    estado:str

    #variáveis dinamicas:
    cont_in:int=0
    cont_out:int=0
    maq_sts:bool=False
    h_ini:int=0
    h_fim:int=0

    #variavais calculadas:
    oee:int=0
    per:int=0
    q:int=0
    dis:int=0
    cont_ini:int=0
    cont_fim:int=0
    vel_atu:int=0

    #variaveis escritas:
    vel_esp:int=300
    buffer:int=0
    forma:int=0
    t_par:int=0
    t_prod:int=0
    t_p_prog:int=0

    #variaveis de banco:
    historico:Hist = []
    histFiltro:Hist = []

    filtro_ini:datetime
    filter_fim:datetime

    def insert_dinamics(self,values):
        cont_in_b1 = values[0]
        cont_in_b2 = values[1]
        cont_out_b1 = values[2]
        cont_out_b2 = values[3]
        if cont_in_b1<0:
            cont_in_b1 = 65536+values[0]
        if cont_in_b2<0:
            cont_in_b2 = 65536+values[1]
        if cont_out_b1<0:
            cont_out_b1 = 65536+values[2]
        if cont_out_b2<0:
            cont_out_b2 = 65536+values[3]
        try:
            self.maq_sts = bool(values[4])
        except:
            pass
        self.cont_in = cont_in_b2+(cont_in_b1*65536)
        self.cont_out = cont_out_b2+(cont_out_b1*65536)
        if self.maq_sts:
            self.estado = 'Parado'
        else:
            self.estado = 'Operando'
        if values[4]==100:
            self.estado = 'Estação OffLine'

    def insert_calculadas(self,values:list):
        self.oee = values[0]
        self.per = values[1]
        self.q = values[2]
        self.dis = values[3]
        self.cont_ini = values[4]
        self.cont_fim = values[5]
        self.vel_atu = values[6]
        self.vel_esp = values[7]
        self.buffer = values[8]
        self.forma = values[9]
        self.t_p_prog = values[10]
        self.t_par = values[11]
        self.t_prod = values[12]

    def insert_falha(self):
        self.estado = 'DXM OffLine'

    def get_log_time(self,filtro:bool):
        ret=''
        if not filtro:
            for x in range(len(self.historico)):
                if x == len(self.historico-1):
                    ret = f"\'{ret}{str(self.historico[x].time)}\'"
                else:
                    ret = f"\'{ret}{str(self.historico[x].time)}\',"
        else:
            for x in range(len(self.histFiltro)):
                if x == len(self.histFiltro-1):
                    ret = f"\'{ret}{str(self.histFiltro[x].time)}\'"
                else:
                    ret = f"\'{ret}{str(self.histFiltro[x].time)}\',"
        return ret

    def get_log_oee(self,filtro:bool):
        ret=''
        if not filtro:
            for x in range(len(self.historico)):
                if x == len(self.historico-1):
                    ret = f"\'{ret}{str(self.historico[x].oee)}\'"
                else:
                    ret = f"\'{ret}{str(self.historico[x].oee)}\',"
        else:
            for x in range(len(self.histFiltro)):
                if x == len(self.histFiltro-1):
                    ret = f"\'{ret}{str(self.histFiltro[x].oee)}\'"
                else:
                    ret = f"\'{ret}{str(self.histFiltro[x].oee)}\',"
        return ret

    def get_log_dis(self,filtro:bool):
        ret=''
        if not filtro:
            for x in range(len(self.historico)):
                if x == len(self.historico-1):
                    ret = f"\'{ret}{str(self.historico[x].dis)}\'"
                else:
                    ret = f"\'{ret}{str(self.historico[x].dis)}\',"
        else:
            for x in range(len(self.histFiltro)):
                if x == len(self.histFiltro-1):
                    ret = f"\'{ret}{str(self.histFiltro[x].dis)}\'"
                else:
                    ret = f"\'{ret}{str(self.histFiltro[x].dis)}\',"
        return ret

    def get_log_q(self,filtro:bool):
        ret=''
        if not filtro:
            for x in range(len(self.historico)):
                if x == len(self.historico-1):
                    ret = f"\'{ret}{str(self.historico[x].q)}\'"
                else:
                    ret = f"\'{ret}{str(self.historico[x].q)}\',"
        else:
            for x in range(len(self.histFiltro)):
                if x == len(self.histFiltro-1):
                    ret = f"\'{ret}{str(self.histFiltro[x].q)}\'"
                else:
                    ret = f"\'{ret}{str(self.histFiltro[x].q)}\',"
        return ret

    def get_log_per(self,filtro:bool):
        ret=''
        if not filtro:
            for x in range(len(self.historico)):
                if x == len(self.historico-1):
                    ret = f"\'{ret}{str(self.historico[x].per)}\'"
                else:
                    ret = f"\'{ret}{str(self.historico[x].per)}\',"
        else:
            for x in range(len(self.histFiltro)):
                if x == len(self.histFiltro-1):
                    ret = f"\'{ret}{str(self.histFiltro[x].per)}\'"
                else:
                    ret = f"\'{ret}{str(self.histFiltro[x].per)}\',"
        return ret

    def get_log_t_prod(self,filtro:bool):
        ret=''
        if not filtro:
            for x in range(len(self.historico)):
                if x == len(self.historico-1):
                    ret = f"\'{ret}{str(self.historico[x].t_prod)}\'"
                else:
                    ret = f"\'{ret}{str(self.historico[x].t_prod)}\',"
        else:
            for x in range(len(self.histFiltro)):
                if x == len(self.histFiltro-1):
                    ret = f"\'{ret}{str(self.histFiltro[x].t_prod)}\'"
                else:
                    ret = f"\'{ret}{str(self.histFiltro[x].t_prod)}\',"
        return ret   

    def get_log_t_par(self,filtro:bool):
        ret=''
        if not filtro:
            for x in range(len(self.historico)):
                if x == len(self.historico-1):
                    ret = f"\'{ret}{str(self.historico[x].t_par)}\'"
                else:
                    ret = f"\'{ret}{str(self.historico[x].t_par)}\',"
        else:
            for x in range(len(self.histFiltro)):
                if x == len(self.histFiltro-1):
                    ret = f"\'{ret}{str(self.histFiltro[x].t_par)}\'"
                else:
                    ret = f"\'{ret}{str(self.histFiltro[x].t_par)}\',"
        return ret 

    def get_log_bons(self,filtro:bool):
        ret=''
        if not filtro:
            for x in range(len(self.historico)):
                if x == len(self.historico-1):
                    ret = f"\'{ret}{str(self.historico[x].bons)}\'"
                else:
                    ret = f"\'{ret}{str(self.historico[x].bons)}\',"
        else:
            for x in range(len(self.histFiltro)):
                if x == len(self.histFiltro-1):
                    ret = f"\'{ret}{str(self.histFiltro[x].bons)}\'"
                else:
                    ret = f"\'{ret}{str(self.histFiltro[x].bons)}\',"
        return ret

    def get_log_ruins_total(self,filtro:bool):
        ret=''
        if not filtro:
            for x in range(len(self.historico)):
                if x == len(self.historico-1):
                    ret = f"\'{ret}{str(self.historico[x].ruins_total)}\'"
                else:
                    ret = f"\'{ret}{str(self.historico[x].ruins_total)}\',"
        else:
            for x in range(len(self.histFiltro)):
                if x == len(self.histFiltro-1):
                    ret = f"\'{ret}{str(self.histFiltro[x].ruins_total)}\'"
                else:
                    ret = f"\'{ret}{str(self.histFiltro[x].ruins_total)}\',"
        return ret

    def get_log_vel_atu(self,filtro:bool):
        ret=''
        if not filtro:
            for x in range(len(self.historico)):
                if x == len(self.historico-1):
                    ret = f"\'{ret}{str(self.historico[x].vel_atu)}\'"
                else:
                    ret = f"\'{ret}{str(self.historico[x].vel_atu)}\',"
        else:
            for x in range(len(self.histFiltro)):
                if x == len(self.histFiltro-1):
                    ret = f"\'{ret}{str(self.histFiltro[x].vel_atu)}\'"
                else:
                    ret = f"\'{ret}{str(self.histFiltro[x].vel_atu)}\',"
        return ret

    def setfiltro(self,ini:datetime,fim:datetime):
        self.filtro_ini = ini
        self.filter_fim = fim
        temp = []
        for x in range(len(self.historico)):
            if self.historico[x].time >= ini and self.historico[x].time <=fim:
                temp.append(self.historico[x])
        self.histFiltro = temp

class OEE():
    pasta = ''
    nomeArquivo = 'OEE.bin'
    arquivo = f'{pasta}\{nomeArquivo}'
    linhas:Linha=[]
    quantidade:int
    DXM_Status:str
    DXM_Endress:str = '192.168.0.1'
    DXM_Tcp:bool = True
    emulador:int=0
    tickLog:int=60

    def __init__(self,qtd:int,linhas=[],endereco='192.168.0.4',emulador=0,tickLog=60,pasta='',arquivo='OEE.bin'):
        self.pasta = pasta
        self.nomeArquivo = arquivo
        self.arquivo = f'{pasta}\{arquivo}'
        if len(linhas)<= 0:
            for x in range(qtd):
                l = Linha()
                l.nome = f'Linha {x}'
                l.id = x
                self.linhas.append(l)
            self.quantidade = qtd
        else:
            self.linhas = linhas
            self.quantidade = len(linhas)
        self.DXM_Endress = endereco
        self.emulador = emulador
        self.tickLog = tickLog
        if endereco.find('COM')>0 or endereco.find('com')>0:
            self.DXM_Tcp = False
        else:
            self.DXM_Tcp = True
        self.DXM_Status = 'Iniciando'

    def DXM_insertFalha(self):
        self.DXM_Status = 'DXM OffLine'

    def DXM_insertOnLine(self):
        self.DXM_Status = 'DXM OnLine'

    def alteraLinhas(self, num:int):
        if num == 0:
            num =1
        result = num-self.quantidade
        if result > 0:
            for x in range(result):
                l = Linha()
                l.nome = f'Equipamento {x}'
                l.id = x
                self.linhas.append(l)
        if result < 0:
            self.linhas = self.linhas[0:self.quantidade-num]
               
        self.quantidade = len(self.linhas)
        index = 0
        for l in self.linhas:
            l.id = index
            index+=1

    def flush(self):
        for x in range(len(self.linhas)):
            self.linhas[x].historico = []
            self.linhas[x].histFiltro = []

    def normaliza(self):
        if len(self.linhas) != self.quantidade:
            self.alteraLinhas(self.quantidade) 

    @staticmethod
    def carrega(pasta,nomeArquivo):
        try:
            arquivo = open(f'{pasta}\{nomeArquivo}','rb')
            pic = pickle.load(arquivo)
            arquivo.close()
            return pic
        except Exception as e:
            print(f'falha ao carregar OEE {str(e)}')
            return OEE(1,endereco='192.168.0.100',pasta=pasta, arquivo=nomeArquivo)

    def salva(self):
        try:
            try:
                os.mkdir(self.pasta)
                print(f"criou a pasta {self.pasta}")
            except:
                pass
            arquivo = open(self.arquivo,'wb')
            pickle.dump(self,arquivo)
            arquivo.close()
            print(f'criou o arquivo {self.arquivo}')
        except Exception as e:
            print(f'falha ao salvar OEE{str(e)}')
