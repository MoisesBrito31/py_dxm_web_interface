import libscrc
import crcmod

def _crc16(dados):
        b = bytes(dados,'ASCII')
        valor= str(hex(libscrc.modbus(b))).upper()[2:]
        while len(valor)<4:
            valor=f'0{valor}'
        hi = valor[2:]
        lo = valor[:2]
        return hi+lo

def _crc16mod(dados):
        b = bytes(dados,'ASCII')
        crc16 = crcmod.mkCrcFun(0x18005, initCrc=0xFFFF, xorOut=0x0000)
        valor= str(hex(crc16(b))).upper()[2:]
        while len(valor)<4:
            valor=f'0{valor}'
        hi = valor[2:]
        lo = valor[:2]
        return hi+lo

valor = "moises brito"

print(_crc16(valor))


print(_crc16mod(valor))