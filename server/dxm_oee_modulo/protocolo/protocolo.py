import socket
from datetime import datetime, timedelta
import crcmod
from time import sleep

class Protocolo():
    HEADERSIZE = 1024
    PORT = 8844
    ip = "192.168.0.100"
    

    def __init__(self, _ip):
        self.ip = _ip
        self.trans = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.trans.connect((self.ip,self.PORT))

    def getMAC(self):
        return self._comandoSimples("CMD0112",True)

    def getRelogio(self):
        ret = datetime(2000,1,1,0,0,0)
        try:
            resposta = self._comandoSimples("CMD0102",True)
            ret = datetime.strptime(resposta,'%Y-%m-%d %H:%M:%S')      
            return ret - timedelta(hours=3)
        except:
            return ret

    def setRelogio(self):
        now = datetime.now() + timedelta(hours=3)
        cmd = f'CMD0101{now.year},{now.month},{now.day},{now.hour},{now.minute},{now.second}'
        ret = self._comandoSimples(cmd,False)
        if ret == 'RSP0101':
            return True
        else:
            return False

    def getSerialumber(self):
        return self._comandoSimples("CMD0113",True)

    def reset(self):
        return self._comandoSemRetorno("CMD0200")

    def reboot(self):
        return self._comandoSemRetorno("CMD020055S")

    def travar(self):
        resp = self._comandoSimples("CMD0449",False,close=False)        
        if resp != "RSP04490":
            if resp == "RSP04491":
                return True
            return False
        resp = self._comandoSimples("CMD045055YmV0aW01MTY=",False,conect=False)
        if resp != "RSP0450":
            return False
        return True
        
    def destravar(self):
        resp = self._comandoSimples("CMD0449",False,close=False)  
        if resp != "RSP04491":
            if resp == "RSP04490":
                return True
            return False
        resp = self._comandoSimples("CMD0451YmV0aW01MTY=",False,conect=False,close=False)
        if resp != "RSP0451":
            return False
        resp = self._comandoSimples("CMD0452",False,conect=False)
        if resp != "RSP0452":
            return False
        return True

    def readReg(self, start, qtd, slaveID=0, modbus=0, timeout=0, open=True, close=True):
        msg = self._comandoSimples(f'CMD0001 {start},{qtd},{slaveID},{modbus},{timeout}',False,close=close,conect=open)
        ret = msg.split(',')
        return ret[1:len(ret)-1]

    def writeReg(self, start, dados:list, slaveID=0, modbus=0, timeout=0, open=True, close=True):
        cmd = f'CMD0002 {start},{len(dados)},{slaveID},{modbus},{timeout}'
        for x in dados:
            cmd = f'{cmd},{x}'
        msg = self._comandoSimples(cmd,False, close=close, conect=open)
        if msg == 'RSP0002':
            return True
        else:
            return False

    def fileExist(self, nome):
        msg = self._comandoSimples(f"CMD1005 {nome}",True)
        if msg == '1':
            return True
        else:
            return False

    def deleteFile(self, nome):
        return self._comandoSemRetorno(f"CMD1006 {nome}")

    def getFile(self, nome):
        ret = []
        msg = self._comandoSimples("CMD1003",False,close=False)
        if msg != "RSP1003":
            return ret
        msg = self._comandoSimples(f"CMD1001/{nome},0,0,1",False,close=False,conect=False)
        if msg[:7] != "RSP1001":
            return ret

        index = 1

        while msg != "RSP10020,ffff,EOF":
            msg = self._comandoSimples(f"CMD1002{index}",False,close=False,conect=False)           
            if msg != "RSP10020,ffff,EOF":
                valor = self._tratamentoString(msg)
                if valor > 0:
                    ret.append(self._stringTrocaQuebraL(msg[valor:]))
                    index+=1
                else:
                    return ['falha crc']

        msg = self._comandoSimples("CMD1003",False,conect=False)
        if msg != "RSP1003":
            return ret
        return ret

    def enviaArquivo(self,nome,pasta):
        #out = open("output.txt",'w')
        colecao = self._estruturaArquivo(nome,pasta)
        msg = self._comandoSimples("CMD1003",False,close=False)
        if msg != "RSP1003":
            return False
        msg = self._comandoSimples(colecao[0],False,close=False,conect=False)
        if msg != "RSP1001OK":
            return False
        for x in range(len(colecao)):
            #out.write(f'{colecao[x]}\r')
            if x != 0:
                msg = self._comandoSimples(colecao[x],False,close=False,conect=False)
                if msg != "RSP1002":
                    return False
        msg = self._comandoSimples("CMD1003",False,close=False,conect=False)
        if msg != "RSP1003":
            return False
        
        if nome.find(".xml")>0:
            msg = self._comandoSimples("CMD020055S",False,conect=False)
        else:
            msg = self._comandoSimples("CMD0112",True,conect=False)
        return True

    def _comandoSimples(self,cmd,format,close=True,conect=True):
        ret = "falha"
        try:
            if conect:
                if self.trans._closed:
                    self.trans = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    self.trans.connect((self.ip,self.PORT))
            msg = bytes(cmd,"utf-8")
            self.trans.send(msg)
            resposta_bytes = self.trans.recv(self.HEADERSIZE)
            resposta = resposta_bytes.decode('utf-8')
            if format:
                ret = resposta[7:]
            else:
                ret = resposta
            if close:
                self.trans.close() 
        except Exception as e:
            print(f'{ret} {str(e)}')
            return f'{ret} {str(e)}'
        return ret

    def _comandoSemRetorno(self,cmd):
        try:
            if self.trans._closed:
                self.trans = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.trans.connect((self.ip,self.PORT))
            msg = bytes(cmd,"utf-8")
            self.trans.send(msg)
            self.trans.close() 
            return True
        except:
            return False

    def _tratamentoString(self,rcp:str):
        try:
            index = rcp.split(',')
            ponto = rcp.find(',',14)+1
            crc_ok = index[1].upper()
            crc_lido = self._crc16(rcp[ponto:])
            if crc_ok != crc_lido:
                return -1
            else:
                return ponto
        except:
            return -1

    def _stringTrocaQuebraL(self,dados:str,decode=True):
        result = ""
        for x in dados:
            temp=x
            if decode:
                if x == '':
                    temp=''
                if x == '':
                    temp = u'\u000A'
            else:
                if x == u'\u000A':
                    temp = ''
            result+=temp
        return result

    def _estruturaArquivo(self,nome,pasta):
        colecao = []
        arquivo = open(f'{pasta}{nome}','r')
        dados = self._stringTrocaQuebraL(arquivo.read(),decode=False)
        arquivo.close()
        tamanho = len(dados)
        loops = int(tamanho/512)
        resto = int(tamanho%512)
        nomeArquivo = nome

        if nome.find(".xml")>0:
            nomeArquivo = "WLConfig.xml"

        colecao.append(f'CMD1001{nomeArquivo},1,{str(tamanho)},0')
       
        for x in range(loops):
            temp = dados[x*512:(x*512)+512]
            size = str(len(temp))
            crc = self._crc16(temp)
            colecao.append(f'CMD1002{size},{crc},{x+1},{temp}')
        temp = dados[tamanho-resto:]
        size = str(len(temp))
        crc = self._crc16(temp)
        colecao.append(f'CMD1002{size},{crc},{loops+1},{temp}')

        return colecao
    

    def _crc16(self,dados):
        b = bytes(dados,'ASCII')
        crc16 = crcmod.mkCrcFun(0x18005, initCrc=0xFFFF, xorOut=0x0000)
        valor= str(hex(crc16(b))).upper()[2:]
        while len(valor)<4:
            valor=f'0{valor}'
        hi = valor[2:]
        lo = valor[:2]
        return hi+lo