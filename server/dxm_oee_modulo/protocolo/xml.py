#from .mapa import Mapa

class Xml():
    pasta = ""
    nomeArquivo = ""
    arquivo = ""
    mapa = ""
    buffer = ""

    def __init__(self, mapa, pasta="", nomeArquivo="DXM_OEE.xml", nome="base" ):
        self.mapa = mapa
        if self.mapa:
            print('mapa ok')
        else:
            print('mapa falho')
        self.pasta=pasta
        self.nomeArquivo = nomeArquivo
        self._carregaXml()

    def _carregaXml(self):
        file = open(f'{self.pasta}{self.nomeArquivo}','r')
        self.arquivo = file.read()
        file.close()

    def salvaArquivo(self):
        self._compilaArquivo()
        #ar = open(f'{self.pasta}{self.nomeArquivo}','w')
        ar = open(f'{self.pasta}{self.nomeArquivo}','w')
        ar.write(self.buffer)
        ar.close()

    def subArquivoIni(self):
        indexini = self.arquivo.find("<rtu_read>")
        if indexini<0:
            indexini = self.arquivo.find("<rtu_read />")
        if indexini>0 :
            return f'{self.arquivo[:indexini]}\r <rtu_read> \r'
        else:
            return 'falha'

    def subArquivoRegs(self):
        ret = ''
        for x in range(len(self.mapa.blocos)):
            if self.mapa.blocos[x].regList[0].ativo:
                dword = self.mapa.blocos[x].regList[0].dword
                ciclo = str(self.mapa.blocos[x].regList[0].ciclo/1000)
                reg = self.mapa.blocos[x].regList[0].reg
                slave = self.mapa.blocos[x].regList[0].slaveID
                if dword == '2':
                    dxmReg = (x * 5) + 1
                else:
                    dxmReg = (x * 5) + 2
                ret = f'{ret}   <rule count=\"{dword}\" mask=\"0\" name=\"contagem_entrada\" offset=\"0\" poll=\"{ciclo}\" remfmt=\"int\" remreg=\"{str(reg)}\" remtype=\"hold_reg\" scale=\"0\" swapped=\"0\" unit=\"{str(slave)}\" localreg=\"{str(dxmReg)}\" maxfail=\"0\" default=\"0\" />\r'
            if self.mapa.blocos[x].regList[1].ativo:
                dword = self.mapa.blocos[x].regList[1].dword
                ciclo = str(self.mapa.blocos[x].regList[1].ciclo/1000)
                reg = self.mapa.blocos[x].regList[1].reg
                slave = self.mapa.blocos[x].regList[1].slaveID
                if dword == '2':
                    dxmReg = (x * 5) + 3
                else:
                    dxmReg = (x * 5) + 4
                ret = f'{ret}   <rule count=\"{dword}\" mask=\"0\" name=\"contagem_saida\" offset=\"0\" poll=\"{ciclo}\" remfmt=\"int\" remreg=\"{str(reg)}\" remtype=\"hold_reg\" scale=\"0\" swapped=\"0\" unit=\"{str(slave)}\" localreg=\"{str(dxmReg)}\" maxfail=\"0\" default=\"0\" />\r'
            if self.mapa.blocos[x].regList[2].ativo:
                dword = self.mapa.blocos[x].regList[2].dword
                ciclo = str(self.mapa.blocos[x].regList[2].ciclo/1000)
                reg = self.mapa.blocos[x].regList[2].reg
                slave = self.mapa.blocos[x].regList[2].slaveID
                dxmReg = (x * 5) + 5
                ret = f'{ret}   <rule count=\"{dword}\" mask=\"0\" name=\"maquina_parada\" offset=\"0\" poll=\"{ciclo}\" remfmt=\"int\" remreg=\"{str(reg)}\" remtype=\"hold_reg\" scale=\"0\" swapped=\"0\" unit=\"{str(slave)}\" localreg=\"{str(dxmReg)}\" maxfail=\"0\" default=\"0\" />\r'
            ret = f'{ret}\r'    

        ret = f'{ret}</rtu_read>\r'   
        return ret

    def subArquivoEvents(self):
        ret =''
        indexIni = self.arquivo.find('<rtu_write>')
        if indexIni<0:
            indexIni = self.arquivo.find('<rtu_write />')
            ret = '<rtu_write>\r'
        else:
            indexFim = self.arquivo.find('</rtu_write>')
            ret = self.arquivo[indexIni:indexFim]
        ret = f'{ret}</rtu_write>\r <sched_holidays />\r <sched_commands />\r <sched_events>\r'
        for t in self.mapa.turnos:
            ret = f'{ret}{t.getXml()}\r'
        ret = f'{ret} </sched_events>'
        return ret

    def subArquivoFim(self):
        ret =''
        indexIni =  self.arquivo.find('</sched_events>')+15
        if indexIni<15:
            indexIni =self.arquivo.find('<sched_events />')+16
        ret = self.arquivo[indexIni:]
        return ret

    def _compilaArquivo(self):
        temp1 = self.subArquivoIni()
        temp2 = self.subArquivoRegs()
        temp3 = self.subArquivoEvents()
        temp4 = self.subArquivoFim()
        self.buffer = f'{temp1}{temp2}{temp3}{temp4}'

   

    



