#  -*- coding: utf-8 -*-
import os, sys
import pyasn1
import binascii
import six
from pyasn1_modules import rfc2459, pem
from pyasn1.codec.der import decoder
from datetime import datetime, timedelta

class Certificate:
  cert_full = ''
  cert = ''
  pyver = ''
  formatCert = ''
  def __init__ (self, fileorstr):
    if (self.pyver == '2'):
        b0 = ord(fileorstr[0])
        b1 = ord(fileorstr[1])
    else:
        b0 = fileorstr[0]
        b1 = fileorstr[1]
    self.pyver = sys.version[0]
    if ((b0 == 48 and b1 > 128) or ( not os.path.exists(fileorstr))):
        substrate = fileorstr
        if (b0 == 48 and b1 > 128) :
#Сертификат в DER-кодировке из строки
    	    self.formatCert = 'DER'
        else:
#Сертификат в PEM-кодировке из строки
    	    self.formatCert = 'PEM'
    	    strcert = fileorstr.strip('\n')
    	    if (strcert[0:27] != '-----BEGIN CERTIFICATE-----'):
    	    	return
    	    idx, substrate = pem.readPemBlocksFromFile(six.StringIO(strcert), ('-----BEGIN CERTIFICATE-----', '-----END CERTIFICATE-----'))
        try:
    	    self.cert_full, rest = decoder.decode(substrate, asn1Spec=rfc2459.Certificate())
    	    self.cert = self.cert_full["tbsCertificate"]
    	    self.formatCert = 'PEM'
        except:
            self.pyver = ''
            self.formatCert = ''
        return

    self.pyver = sys.version[0]
    filename = fileorstr
    if (self.pyver == '2'):
        if sys.platform != "win32":
            filename = filename.decode("UTF-8")
        else:
            filename = filename.decode("CP1251")
#Проверяем на DER
    file1 = open(filename, "rb")
    substrate = file1.read()
    if (self.pyver == '2'):
            b0 = ord(substrate[0])
            b1 = ord(substrate[1])
    else:
            b0 = substrate[0]
            b1 = substrate[1]
#Проверка наличия последовательности 0x30, длина сертификата не может быть меньше 127 байт
    if (b0 == 48 and b1 > 128) :
    	self.formatCert = 'DER'
    else:
        self.formatCert = 'PEM'
        file1 = open(filename, "r")
        print ('FILE')
        print (file1)
        idx, substrate = pem.readPemBlocksFromFile(
    	    file1, ('-----BEGIN CERTIFICATE-----',
                '-----END CERTIFICATE-----')
        )
    file1.close()
    try:
        self.cert_full, rest = decoder.decode(substrate, asn1Spec=rfc2459.Certificate())
        self.cert = self.cert_full["tbsCertificate"]
    except:
        self.pyver = ''
        self.formatCert = ''
    
  def notation_OID(self, oidhex_string):
    ''' Input is a hex string and as one byte is 2 charecters i take an 
        empty list and insert 2 characters per element of the list.
        So for a string 'DEADBEEF' it would be ['DE','AD','BE,'EF']. '''
    hex_list = []
    for char in range(0, len(oidhex_string), 2):
        hex_list.append(oidhex_string[char]+oidhex_string[char+1])

    ''' I have deleted the first two element of the list as my hex string
        includes the standard OID tag '06' and the OID length '0D'. 
        These values are not required for the calculation as i've used 
        absolute OID and not using any ASN.1 modules. Can be removed if you
        have only the data part of the OID in hex string. '''
    del hex_list[0]
    del hex_list[0]

    # An empty string to append the value of the OID in standard notation after
    # processing each element of the list.
    OID_str = ''

    # Convert the list with hex data in str format to int format for
    # calculations.
    for element in range(len(hex_list)):
        hex_list[element] = int(hex_list[element], 16)

    # Convert the OID to its standard notation. Sourced from code in other
    # languages and adapted for python.

    # The first two digits of the OID are calculated differently from the rest.
    x = int(hex_list[0] / 40)
    y = int(hex_list[0] % 40)
    if x > 2:
        y += (x-2)*40
        x = 2

    OID_str += str(x)+'.'+str(y)

    val = 0
    for byte in range(1, len(hex_list)):
        val = ((val << 7) | ((hex_list[byte] & 0x7F)))
        if (hex_list[byte] & 0x80) != 0x80:
            OID_str += "."+str(val)
            val = 0

    # print the OID in dot notation.
    return (OID_str)

  def subjectSignTool(self):
    if(self.cert == ''):
        return ('')
    for ext in self.cert["extensions"]:
        #Ищем расширение subjectSignTool
        if(str(ext['extnID']) == "1.2.643.100.111"):
                #Его значение надо возвращать
                ll = ext['extnValue'][1:2].prettyPrint()
                if (int(ll, 16) > 128):
            	    seek = 3
                else:
                    seek = 2
#Проверка версии python-а
                if (self.pyver == '2'):
                    return ext['extnValue'][seek-2:]
                sst = ext['extnValue'][seek:].prettyPrint()
                if (len(sst) > 1 and sst[0] == '0' and sst[1] == 'x'):
            	    sst = binascii.unhexlify(sst[2:])
            	    sst = sst.decode('utf-8')
            	    
                return (sst)
    return ('')

  def issuerSignTool(self):
    if(self.cert == ''):
        return ([])
    for ext in self.cert["extensions"]:
        #Ищем расширение issuerSignTool
        if(str(ext['extnID']) == "1.2.643.100.112"):
                #Его значение надо возвращать
                vv = ext['extnValue']
#                print(vv.prettyPrint())
#Проверка версии python-а
                of2 = 1
                if (self.pyver == '2'):
                    of1 = ord(vv[of2])
                else:
                    of1 = vv[of2]

                if (of1 > 128):
                    of2 += (of1 - 128)
                of2 += 1
#Add for 0x30
                of2 += 1
                if (self.pyver == '2'):
                    of1 = ord(vv[of2])
                else:
                    of1 = vv[of2]

                if (of1 > 128):
                    of2 += (of1 - 128)
#                    of2 += 1
# Поля issuerSignTools		    
                fsbCA = []
#Длина первого поля
                for j in range(0,4):
                    if (self.pyver == '2'):
                        ltek = ord(vv[of2])
                        stek = of2 + 1
                    else:
                        ltek = vv[of2 + 0]
                        stek = of2 + 1
                    fsb = vv[stek: stek+ltek]
                    if (self.pyver == '3'):
                        fsb = vv[stek: stek+ltek].prettyPrint()
                        if (len(fsb) > 1 and fsb[0] == '0' and fsb[1] == 'x'):
                            try:
                                val1 = binascii.unhexlify(fsb[2:])
                                fsb = val1.decode('utf-8')
                            except:
                                fsb = vv[stek: stek+ltek].prettyPrint()
                    fsbCA.append(fsb)
                    of2 += (ltek + 2)
                    if (of2 > len(vv)):
                        break
#Возврат значений issuerSignTools
                return(fsbCA)
    return ([])
    	
  def classUser(self):
    if(self.cert == ''):
        return ('')
    for ext in self.cert["extensions"]:
        #Ищем расширение subjectSignTool
        if(str(ext['extnID']) == "2.5.29.32"):
                #Классы защищенности
#Переводит из двоичной системы счисления (2) в hex
                kc = ext['extnValue'].prettyPrint()
#                print(kc)
#Сдвиг на 0x
#Проверка версии python-а
                if (self.pyver == '2'):
            	    kc_hex = kc[2:]
                else:
            	    kc_hex = kc[2:]
# 4 - длина заголовка 			
                kc_hex = kc_hex[4:]
                i32 = kc_hex.find('300806062a85036471')
                tmp_kc = ''
                while (i32 != -1 ) :
                    #'300806062a85036471' - 10 байт бинарных и 20 hex-овых; 4 - это 3008
#                    print ('НАШЛИ КС i32=' + str(i32))
                    kcc_tek = kc_hex[i32+4: i32 + 20]
#			print (kcc_tek)
                    oid_kc = self.notation_OID(kcc_tek)
#                    print (oid_kc)
                    tmp_kc = tmp_kc + oid_kc + ';;'
                    kc_hex = kc_hex[i32 + 20:]
                    i32 = kc_hex.find('300806062a85036471')
                return (tmp_kc)
    return ('')

  def identKind(self):
    if(self.cert == ''):
        return ('')
    for ext in self.cert["extensions"]:
        #Ищем расширение IdentificationKind
        if(str(ext['extnID']) == "1.2.643.100.114"):
#Переводит из двоичной системы счисления (2) в hex
                kc = ext['extnValue'].prettyPrint()
                kc1 = kc[2:4]
#Проверяем tag integer
                if(kc1 != '02'):
#                    print ('not integer')
                    return (-1)
#Проверяем длину
                kc1 = kc[4:6]
                if(kc1 != '01'):
#                    print ('bad length')
                    return (-1)
                type = kc[6:8]
#Переводим в целое из 16-ной системы счисления
                type = int(type, 16)
                if (type > 3):
#            	    print ('Неизвестный тип идентификации = ' + str(type))
            	    return (-1)
                return (type)
    return (-1)

  def keyPeriod(self):
    validity_key = {}
    validity_key['not_before'] = ''
    validity_key['not_after'] = ''
    if(self.cert == ''):
        return ('')
    for ext in self.cert["extensions"]:
        #Ищем расширение id-ce-privateKeyUsagePeriod
        if(str(ext['extnID']) == "2.5.29.16"):
#Переводит из двоичной системы счисления (2) в hex
                kc = ext['extnValue'].prettyPrint()
                kc = ext['extnValue']
                validity_key['not_before'] = datetime.strptime(str(kc[6:19]), '%y%m%d%H%M%SZ')
                validity_key['not_after'] = datetime.strptime(str(kc[23:37]), '%y%m%d%H%M%SZ')
    return validity_key

  def parse_issuer_subject (self, who):
    if(self.cert == ''):
        return ({})
    infoMap = {
        "1.2.840.113549.1.9.2": "unstructuredName",
        "1.2.643.100.1": "OGRN",
        "1.2.643.100.5": "OGRNIP",
        "1.2.643.3.131.1.1": "INN",
        "1.2.643.100.4": "INNLE",
        "1.2.643.100.3": "SNILS",
        "2.5.4.3": "CN",
        "2.5.4.4": "SN",
        "2.5.4.5": "serialNumber",
        "2.5.4.42": "GN",
        "1.2.840.113549.1.9.1": "E",
        "2.5.4.7": "L",
        "2.5.4.8": "ST",
        "2.5.4.9": "street",
        "2.5.4.10": "O",
        "2.5.4.11": "OU",
        "2.5.4.12": "title",
        "2.5.4.6": "Country",
    }
    issuer_or_subject = {}
#Владелец сертификата: 0 - неизвестно 1 - физ.лицо 2 - юр.лицо
    vlad = 0
    for rdn in self.cert[who][0]:
        if not rdn:
            continue
        oid = str(rdn[0][0])
        value = rdn[0][1]
#INN
        if(oid == '1.2.643.3.131.1.1'):
            vlad = 1
#INNLE
        elif(oid == '1.2.643.100.4'):
            vlad = 2
#Учёт длины
        of2 = 1
        vv = value
        if (self.pyver == '2'):
            of1 = ord(vv[of2])
        else:
            of1 = vv[of2]
        if (of1 > 128):
            of2 += (of1 - 128)
        of2 += 1

        value = value[of2:]
        if (self.pyver == '3'):
            val = value.prettyPrint()
            if (len(val) > 1 and val[0] == '0' and val[1] == 'x'):
                try:
                      val1 = binascii.unhexlify(val[2:])
                      value = val1.decode('utf-8')
                except:
                      pass
        try:
            if not infoMap[oid] == "Type":
                issuer_or_subject[infoMap[oid]] = value
            else:
                try:
                    issuer_or_subject[infoMap[oid]] += ", %s" % value
                except KeyError:
                    issuer_or_subject[infoMap[oid]] = value
        except KeyError:
            issuer_or_subject[oid] = value
    return issuer_or_subject, vlad

  def issuerCert(self):
    return (self.parse_issuer_subject ("issuer"))

  def subjectCert(self):
    return (self.parse_issuer_subject ('subject'))

  def signatureCert(self):
    if(self.cert == ''):
        return ({})
    algosign = self.cert_full["signatureAlgorithm"]['algorithm']
    kk = self.cert_full["signatureValue"].prettyPrint()
    if kk[-3:-1] == "'B":
        #Избавляемся от "' в начале строки и 'B" и конце строки
        kk = kk[2:-3]
#Переводит из двоичной системы счисления (2) в целое
        kkh=int(kk, 2)
    else:
       kkh=int(kk, 10)
    sign_hex = hex(kkh)
    sign_hex = sign_hex.rstrip('L')
    return (algosign, sign_hex[2:])

  def publicKey(self):
    if(self.cert == ''):
        return ({})
    pubkey = self.cert['subjectPublicKeyInfo']
    tmp_pk = {}
    ff = pubkey['algorithm']
    algo = ff['algorithm']
    tmp_pk['algo'] = str(algo)
#Проверка на ГОСТ
#    if (str(algo).find("1.2.643") == -1):
#        print ('НЕ ГОСТ')
#        return (tmp_pk)
#Проверяем RSA
    if (str(algo).find("1.2.840.113549.1.1") != -1):
        return (tmp_pk)

    param = ff['parameters']
    lh = param.prettyPrint()[2:]
#Общая длина параметров
    if (self.pyver == '2'):
        lall = ord(param[1])
    else:
        lall = param[1]
#Со 2-й по 11 позиции, первые два байта тип и длина hex-oid-а
    l1 = int(lh[7:8], 16)
    lh1 = self.notation_OID(lh [4:4+4+l1*2])
#Есть еже параметры
    lall = lall - 2
    lh2 = ''
    if (lall > l1):
#Длина следующего oid-а
        l2 = int(lh[4+4+l1*2 + 3: 4+4+l1*2  + 4], 16)
#oid из hex в точечную форму
        lh2 = self.notation_OID(lh [4+4+l1*2:4+4+l1*2 + 4 + l2*2])
#Извлекаем публичный ключ

    key_bytes = pubkey['subjectPublicKey']
#Читаем значение открытого ключа как битовую строку
    kk = key_bytes.prettyPrint()
    if kk[-3:-1] == "'B":
#        print(kk[-3:-1])
        #Избавляемся от "' в начале строки и 'B" и конце строки
        kk = kk[2:-3]
#Переводит из двоичной системы счисления (2) в целое
        kkh=int(kk, 2)
    else:
       kkh=int(kk, 10)
#Из целого в HEX
    kk_hex = hex(kkh)
#Значение ключа в hex хранится как 0x440... (длина ключа 512 бит) или 0x48180... (длина ключа 1024 бита)
    if (kk_hex[3] == '4'):
        kk_hex = kk_hex[5:]
    elif (kk_hex[3] == '8'):
        kk_hex = kk_hex[7:]
#Обрезвем концевик
    kk_hex = kk_hex.rstrip('L')
    tmp_pk['curve'] = lh1
    tmp_pk['hash'] = lh2
    tmp_pk['valuepk'] = kk_hex
    return (tmp_pk)

  def prettyPrint(self):
    if(self.cert == ''):
        return ('')
    return (self.cert_full.prettyPrint())

  def serialNumber(self):
    return(self.cert.getComponentByName('serialNumber'))

  def validityCert(self):
    valid_cert = self.cert.getComponentByName('validity')
    validity_cert = {}
    not_before = valid_cert.getComponentByName('notBefore')
    not_before = str(not_before.getComponent())
    not_after = valid_cert.getComponentByName('notAfter')
    not_after = str(not_after.getComponent())
    validity_cert['not_before'] = datetime.strptime(not_before, '%y%m%d%H%M%SZ')
    validity_cert['not_after'] = datetime.strptime(not_after, '%y%m%d%H%M%SZ')
    return validity_cert

  def KeyUsage(self):
    X509V3_KEY_USAGE_BIT_FIELDS = (
	'digitalSignature',
	'nonRepudiation',
	'keyEncipherment',
	'dataEncipherment',
	'keyAgreement',
	'keyCertSign',
	'CRLSign',
	'encipherOnly',
	'decipherOnly',
    )
    if(self.cert == ''):
        return ([])
    ku = []
    for ext in self.cert["extensions"]:
        #Ищем расширение keyUsage
        if(str(ext['extnID']) != "2.5.29.15"):
             continue
        os16 = ext['extnValue'].prettyPrint()
        os16 = '0404' + os16[2:]
        os = binascii.unhexlify(os16[0:])
        octet_strings = os
        e, f= decoder.decode(decoder.decode(octet_strings)[0], rfc2459.KeyUsage())
        n = 0
        while n < len(e):
          if e[n]:
            ku.append(X509V3_KEY_USAGE_BIT_FIELDS[n])
          n += 1
        return(ku)
    return ([])

  def Extensions(self):
    return (self.cert["extensions"])


if __name__ == "__main__":

#For test
    certpem_O = """
-----BEGIN CERTIFICATE-----
MIIG3DCCBougAwIBAgIKE8/KkAAAAAAC4zAIBgYqhQMCAgMwggFKMR4wHAYJKoZI
hvcNAQkBFg9kaXRAbWluc3Z5YXoucnUxCzAJBgNVBAYTAlJVMRwwGgYDVQQIDBM3
NyDQsy4g0JzQvtGB0LrQstCwMRUwEwYDVQQHDAzQnNC+0YHQutCy0LAxPzA9BgNV
BAkMNjEyNTM3NSDQsy4g0JzQvtGB0LrQstCwLCDRg9C7LiDQotCy0LXRgNGB0LrQ
sNGPLCDQtC4gNzEsMCoGA1UECgwj0JzQuNC90LrQvtC80YHQstGP0LfRjCDQoNC+
0YHRgdC40LgxGDAWBgUqhQNkARINMTA0NzcwMjAyNjcwMTEaMBgGCCqFAwOBAwEB
EgwwMDc3MTA0NzQzNzUxQTA/BgNVBAMMONCT0L7Qu9C+0LLQvdC+0Lkg0YPQtNC+
0YHRgtC+0LLQtdGA0Y/RjtGJ0LjQuSDRhtC10L3RgtGAMB4XDTE4MDcwOTE1MjYy
NFoXDTI3MDcwOTE1MjYyNFowggFVMR4wHAYJKoZIhvcNAQkBFg9jb250YWN0QGVr
ZXkucnUxITAfBgNVBAMMGNCe0J7QniDCq9CV0LrQtdC5INCj0KbCuzEwMC4GA1UE
Cwwn0KPQtNC+0YHRgtC+0LLQtdGA0Y/RjtGJ0LjQuSDRhtC10L3RgtGAMSEwHwYD
VQQKDBjQntCe0J4gwqvQldC60LXQuSDQo9CmwrsxCzAJBgNVBAYTAlJVMRgwFgYD
VQQIDA83NyDQnNC+0YHQutCy0LAxRDBCBgNVBAkMO9Cj0JvQmNCm0JAg0JjQm9Cs
0JjQndCa0JAsINCULjQsINCQ0J3QotCgIDMg0K3Qojsg0J/QntCcLjk0MRgwFgYD
VQQHDA/Qsy7QnNC+0YHQutCy0LAxGDAWBgUqhQNkARINMTE0Nzc0NjcxNDYzMTEa
MBgGCCqFAwOBAwEBEgwwMDc3MTA5NjQzNDgwYzAcBgYqhQMCAhMwEgYHKoUDAgIk
AAYHKoUDAgIeAQNDAARAW3hfhvDdUxa6N8hEDjmOg/LsDDRHj5DanAyARtNB/2b5
BEzQCg4lUwrO/VHmvoUtvsrLqrxV6Ae+jh+GFli9WKOCA0AwggM8MBIGA1UdEwEB
/wQIMAYBAf8CAQAwHQYDVR0OBBYEFMQYnG5GfYRnj2ehEQ5tv8Fso/qBMAsGA1Ud
DwQEAwIBRjAdBgNVHSAEFjAUMAgGBiqFA2RxATAIBgYqhQNkcQIwKAYFKoUDZG8E
Hwwd0KHQmtCX0JggwqvQm9CY0KDQodCh0JstQ1NQwrswggGLBgNVHSMEggGCMIIB
foAUi5g7iRhR6O+cAni46sjUILJVyV2hggFSpIIBTjCCAUoxHjAcBgkqhkiG9w0B
CQEWD2RpdEBtaW5zdnlhei5ydTELMAkGA1UEBhMCUlUxHDAaBgNVBAgMEzc3INCz
LiDQnNC+0YHQutCy0LAxFTATBgNVBAcMDNCc0L7RgdC60LLQsDE/MD0GA1UECQw2
MTI1Mzc1INCzLiDQnNC+0YHQutCy0LAsINGD0LsuINCi0LLQtdGA0YHQutCw0Y8s
INC0LiA3MSwwKgYDVQQKDCPQnNC40L3QutC+0LzRgdCy0Y/Qt9GMINCg0L7RgdGB
0LjQuDEYMBYGBSqFA2QBEg0xMDQ3NzAyMDI2NzAxMRowGAYIKoUDA4EDAQESDDAw
NzcxMDQ3NDM3NTFBMD8GA1UEAww40JPQvtC70L7QstC90L7QuSDRg9C00L7RgdGC
0L7QstC10YDRj9GO0YnQuNC5INGG0LXQvdGC0YCCEDRoHkDLQe8zqaC3yHaSmikw
WQYDVR0fBFIwUDAmoCSgIoYgaHR0cDovL3Jvc3RlbGVjb20ucnUvY2RwL2d1Yy5j
cmwwJqAkoCKGIGh0dHA6Ly9yZWVzdHItcGtpLnJ1L2NkcC9ndWMuY3JsMIHGBgUq
hQNkcASBvDCBuQwj0J/QkNCa0JwgwqvQmtGA0LjQv9GC0L7Qn9GA0L4gSFNNwrsM
INCf0JDQmiDCq9CT0L7Qu9C+0LLQvdC+0Lkg0KPQpsK7DDbQl9Cw0LrQu9GO0YfQ
tdC90LjQtSDihJYgMTQ5LzMvMi8yLTk5OSDQvtGCIDA1LjA3LjIwMTIMONCX0LDQ
utC70Y7Rh9C10L3QuNC1IOKEliAxNDkvNy8xLzQvMi02MDMg0L7RgiAwNi4wNy4y
MDEyMAgGBiqFAwICAwNBALvjFGhdFE9llvlvKeQmZmkI5J+yO2jFWTh8nXPjIpiL
OutUew2hIZv15pJ1QM/VgRO3BTBGDOoIrq8LvgC+3kA=
-----END CERTIFICATE-----
"""
    certpem_N = """
-----BEGIN CERTIFICATE-----
MIIDhDCCAy+gAwIBAgIEYX0MYzAMBggqhQMHAQEDAgUAMIHtMQswCQYDVQQGEwJS
VTEsMCoGA1UECAwj0JzQvtGB0LrQvtCy0YHQutCw0Y8g0L7QsdC70LDRgdGC0Ywx
JzAlBgNVBAMMHtCi0LXRgdGC0JrRgNC40L/RgtC+0JDQoNCcUEtDUzEnMCUGA1UE
Cgwe0KLQtdGB0YLQmtGA0LjQv9GC0L7QkNCg0JxQS0NTMR4wHAYJKoZIhvcNAQkB
Fg92b3JsaXZAbGlzc2kucnUxDTALBgNVBAsMBNCj0KYxGDAWBgUqhQNkARINMTEx
MTExMTExMTExMTEVMBMGBSqFA2QEEgoxMjM0NTY3ODkwMB4XDTIxMTAzMDA5MTg1
OFoXDTIyMTExODA5MTg1OFowge0xCzAJBgNVBAYTAlJVMSwwKgYDVQQIDCPQnNC+
0YHQutC+0LLRgdC60LDRjyDQvtCx0LvQsNGB0YLRjDEnMCUGA1UEAwwe0KLQtdGB
0YLQmtGA0LjQv9GC0L7QkNCg0JxQS0NTMScwJQYDVQQKDB7QotC10YHRgtCa0YDQ
uNC/0YLQvtCQ0KDQnFBLQ1MxHjAcBgkqhkiG9w0BCQEWD3ZvcmxpdkBsaXNzaS5y
dTENMAsGA1UECwwE0KPQpjEYMBYGBSqFA2QBEg0xMTExMTExMTExMTExMRUwEwYF
KoUDZAQSCjEyMzQ1Njc4OTAwZjAfBggqhQMHAQEBATATBgcqhQMCAiMDBggqhQMH
AQECAgNDAARASdV+gfqtSJQnGcgUOzi50fAD5/OvyGLw7d7HENbGqz9gu7Sej2VI
huJ1rAit/7R/lEX9d4IOdLDMc9/ogdy4IKOBqzCBqDASBgNVHRMBAQAECDAGAQH/
AgEAMAsGA1UdDwQEAwIC9DBFBgUqhQNkbwQ8DDrQndCw0LjQvNC10L3QvtCy0LDQ
vdC40LUg0KHQmtCX0Jgg0L/QvtC70YzQt9C+0LLQsNGC0LXQu9GPMB0GA1UdDgQW
BBQ+zDiOCPEpTDgYnBoJFTolAtFf0jAfBgNVHSMEGDAWgBQ+zDiOCPEpTDgYnBoJ
FTolAtFf0jAMBggqhQMHAQEDAgUAA0EAOo69wGBN6fs1FUxw4nUaNw6igyq5g9mY
a7nxmIiodzeG0vto/1Dn8YeNK7Fj4sq+0UFCEBUdoy23ORxQABZdMA==
-----END CERTIFICATE-----
"""

    certpem = """
-----BEGIN CERTIFICATE-----
MIIIqDCCCFWgAwIBAgIKXy4gEAACAALvDzAKBggqhQMHAQEDAjCCAVgxGDAWBgUq
hQNkARINMTE2Nzc0Njg0MDg0MzEaMBgGCCqFAwOBAwEBEgwwMDc3MTQ0MDc1NjMx
CzAJBgNVBAYTAlJVMRwwGgYDVQQIDBM3NyDQsy4g0JzQvtGB0LrQstCwMRUwEwYD
VQQHDAzQnNC+0YHQutCy0LAxaDBmBgNVBAkMX9Cj0JvQmNCm0JAgOCDQnNCQ0KDQ
otCQLCDQlNCe0JwgMSwg0KHQotCg0J7QldCd0JjQlSAxMiwg0JrQntCc0J3QkNCi
0JAgMyzQn9Ce0JzQldCpIFhMSUks0K3QoiA3MTAwLgYDVQQLDCfQo9C00L7RgdGC
0L7QstC10YDRj9GO0YnQuNC5INGG0LXQvdGC0YAxIDAeBgNVBAoMF9Ce0J7QniAi
0JDQudGC0LjQmtC+0LwiMSAwHgYDVQQDDBfQntCe0J4gItCQ0LnRgtC40JrQvtC8
IjAeFw0yMTA5MzAxNjU2MDZaFw0yMjA5MzAxNzA2MDZaMIIBaDEfMB0GCSqGSIb3
DQEJAgwQSU5OPTUwNTQwMTAyMTI5NzEiMCAGCSqGSIb3DQEJARYTa29zdHQxOTcz
QHlhbmRleC5ydTEaMBgGCCqFAwOBAwEBEgw1MDU0MDEwMjEyOTcxFjAUBgUqhQNk
AxILMTkxNzI5MTYyOTIxFzAVBgNVBAcMDtCa0L7RgNC+0LvQtdCyMS8wLQYDVQQI
DCY1MCDQnNC+0YHQutC+0LLRgdC60LDRjyDQvtCx0LvQsNGB0YLRjDELMAkGA1UE
BhMCUlUxODA2BgNVBCoML9Ca0L7QvdGB0YLQsNC90YLQuNC9INCQ0LvQtdC60YHQ
sNC90LTRgNC+0LLQuNGHMRUwEwYDVQQEDAzQqNCy0LXRhtC+0LIxRTBDBgNVBAMM
PNCo0LLQtdGG0L7QsiDQmtC+0L3RgdGC0LDQvdGC0LjQvSDQkNC70LXQutGB0LDQ
vdC00YDQvtCy0LjRhzBmMB8GCCqFAwcBAQEBMBMGByqFAwICJAAGCCqFAwcBAQIC
A0MABEA8Ca0IJSg8mUn3OqzLrBlWsix0dGK4yHrOx3WWPMC5ro/Gkhx53ByzVkQw
q02Cv73+uYPHCXaVFbs/+4Dn5HF0o4IE5DCCBOAwPgYDVR0lBDcwNQYIKwYBBQUH
AwQGByqFAwICIgYGCCsGAQUFBwMCBgUqhQMGNQYHKoUDA4IoDAYGKoUDA4IoMA4G
A1UdDwEB/wQEAwIE8DAfBgkrBgEEAYI3FQcEEjAQBggqhQMCAi4ACAIBAQIBADAh
BgUqhQNkbwQYDBbQmtGA0LjQv9GC0L7Qn9Cg0J4gQ1NQMAwGBSqFA2RyBAMCAQAw
UAYJKwYBBAGCNxUKBEMwQTAKBggrBgEFBQcDBDAJBgcqhQMCAiIGMAoGCCsGAQUF
BwMCMAcGBSqFAwY1MAkGByqFAwOCKAwwCAYGKoUDA4IoMHQGCCsGAQUFBwEBBGgw
ZjA2BggrBgEFBQcwAYYqaHR0cDovL3NlcnZpY2UuaXRrMjMucnUvaXRjb20yMDIw
L29jc3Auc3JmMCwGCCsGAQUFBzAChiBodHRwOi8vaXRrMjMucnUvY2EvaXRjb20y
MDIwLmNlcjAdBgNVHSAEFjAUMAgGBiqFA2RxATAIBgYqhQNkcQIwKwYDVR0QBCQw
IoAPMjAyMTA5MzAxNjU2MDVagQ8yMDIyMDkzMDE3MDYwNVowggE6BgUqhQNkcASC
AS8wggErDCsi0JrRgNC40L/RgtC+0J/RgNC+IENTUCIgKNCy0LXRgNGB0LjRjyA0
LjApDCwi0JrRgNC40L/RgtC+0J/RgNC+INCj0KYiICjQstC10YDRgdC40LggMi4w
KQxp0KHQtdGA0YLQuNGE0LjQutCw0YIg0YHQvtC+0YLQstC10YLRgdGC0LLQuNGP
INCk0KHQkSDQoNC+0YHRgdC40Lgg0KHQpC8xMjQtMzk2NiDQvtGCIDE1INGP0L3Q
stCw0YDRjyAyMDIxDGPQodC10YDRgtC40YTQuNC60LDRgiDRgdC+0L7RgtCy0LXR
gtGB0YLQstC40Y8g0KTQodCRINCg0L7RgdGB0LjQuCDihJYg0KHQpC8xMjgtMzU5
MiDQvtGCIDE3LjEwLjIwMTgwZwYDVR0fBGAwXjAtoCugKYYnaHR0cDovL2NkcDIu
aXRrMjMucnUvaXRjb20yMDEyLTIwMjAuY3JsMC2gK6AphidodHRwOi8vY2RwMS5p
dGsyMy5ydS9pdGNvbTIwMTItMjAyMC5jcmwwggFgBgNVHSMEggFXMIIBU4AUXLeC
VuGgdIOZQ4QE8vqseYAxeU+hggEspIIBKDCCASQxHjAcBgkqhkiG9w0BCQEWD2Rp
dEBtaW5zdnlhei5ydTELMAkGA1UEBhMCUlUxGDAWBgNVBAgMDzc3INCc0L7RgdC6
0LLQsDEZMBcGA1UEBwwQ0LMuINCc0L7RgdC60LLQsDEuMCwGA1UECQwl0YPQu9C4
0YbQsCDQotCy0LXRgNGB0LrQsNGPLCDQtNC+0LwgNzEsMCoGA1UECgwj0JzQuNC9
0LrQvtC80YHQstGP0LfRjCDQoNC+0YHRgdC40LgxGDAWBgUqhQNkARINMTA0Nzcw
MjAyNjcwMTEaMBgGCCqFAwOBAwEBEgwwMDc3MTA0NzQzNzUxLDAqBgNVBAMMI9Cc
0LjQvdC60L7QvNGB0LLRj9C30Ywg0KDQvtGB0YHQuNC4ggsArGsYjQAAAAAE+zAd
BgNVHQ4EFgQUfbTOaI2YbC4qyFjOWrEgyr2FWiMwCgYIKoUDBwEBAwIDQQDPeewv
j8mpj2KTE2doICsDWvjPJZGlpYyub0LqTJyMNRBrw61ou/uek4dqCVIzsu3yAiEM
yY5ekzckO4QtX6va
-----END CERTIFICATE-----
"""

    certpem_32 = """
-----BEGIN CERTIFICATE-----
MIIIqDCCCFWgAwIBAgIKXy4gEAACAALvDzAKBggqhQMHAQEDAjCCAVgxGDAWBgUq
hQNkARINMTE2Nzc0Njg0MDg0MzEaMBgGCCqFAwOBAwEBEgwwMDc3MTQ0MDc1NjMx
CzAJBgNVBAYTAlJVMRwwGgYDVQQIDBM3NyDQsy4g0JzQvtGB0LrQstCwMRUwEwYD
VQQHDAzQnNC+0YHQutCy0LAxaDBmBgNVBAkMX9Cj0JvQmNCm0JAgOCDQnNCQ0KDQ
otCQLCDQlNCe0JwgMSwg0KHQotCg0J7QldCd0JjQlSAxMiwg0JrQntCc0J3QkNCi
0JAgMyzQn9Ce0JzQldCpIFhMSUks0K3QoiA3MTAwLgYDVQQLDCfQo9C00L7RgdGC
0L7QstC10YDRj9GO0YnQuNC5INGG0LXQvdGC0YAxIDAeBgNVBAoMF9Ce0J7QniAi
0JDQudGC0LjQmtC+0LwiMSAwHgYDVQQDDBfQntCe0J4gItCQ0LnRgtC40JrQvtC8
IjAeFw0yMTA5MzAxNjU2MDZaFw0yMjA5MzAxNzA2MDZaMIIBaDEfMB0GCSqGSIb3
DQEJAgwQSU5OPTUwNTQwMTAyMTI5NzEiMCAGCSqGSIb3DQEJARYTa29zdHQxOTcz
QHlhbmRleC5ydTEaMBgGCCqFAwOBAwEBEgw1MDU0MDEwMjEyOTcxFjAUBgUqhQNk
AxILMTkxNzI5MTYyOTIxFzAVBgNVBAcMDtCa0L7RgNC+0LvQtdCyMS8wLQYDVQQI
DCY1MCDQnNC+0YHQutC+0LLRgdC60LDRjyDQvtCx0LvQsNGB0YLRjDELMAkGA1UE
BhMCUlUxODA2BgNVBCoML9Ca0L7QvdGB0YLQsNC90YLQuNC9INCQ0LvQtdC60YHQ
sNC90LTRgNC+0LLQuNGHMRUwEwYDVQQEDAzQqNCy0LXRhtC+0LIxRTBDBgNVBAMM
PNCo0LLQtdGG0L7QsiDQmtC+0L3RgdGC0LDQvdGC0LjQvSDQkNC70LXQutGB0LDQ
vdC00YDQvtCy0LjRhzBmMB8GCCqFAwcBAQEBMBMGByqFAwICJAAGCCqFAwcBAQIC
A0MABEA8Ca0IJSg8mUn3OqzLrBlWsix0dGK4yHrOx3WWPMC5ro/Gkhx53ByzVkQw
q02Cv73+uYPHCXaVFbs/+4Dn5HF0o4IE5DCCBOAwPgYDVR0lBDcwNQYIKwYBBQUH
AwQGByqFAwICIgYGCCsGAQUFBwMCBgUqhQMGNQYHKoUDA4IoDAYGKoUDA4IoMA4G
A1UdDwEB/wQEAwIE8DAfBgkrBgEEAYI3FQcEEjAQBggqhQMCAi4ACAIBAQIBADAh
BgUqhQNkbwQYDBbQmtGA0LjQv9GC0L7Qn9Cg0J4gQ1NQMAwGBSqFA2RyBAMCASAw
UAYJKwYBBAGCNxUKBEMwQTAKBggrBgEFBQcDBDAJBgcqhQMCAiIGMAoGCCsGAQUF
BwMCMAcGBSqFAwY1MAkGByqFAwOCKAwwCAYGKoUDA4IoMHQGCCsGAQUFBwEBBGgw
ZjA2BggrBgEFBQcwAYYqaHR0cDovL3NlcnZpY2UuaXRrMjMucnUvaXRjb20yMDIw
L29jc3Auc3JmMCwGCCsGAQUFBzAChiBodHRwOi8vaXRrMjMucnUvY2EvaXRjb20y
MDIwLmNlcjAdBgNVHSAEFjAUMAgGBiqFA2RxATAIBgYqhQNkcQIwKwYDVR0QBCQw
IoAPMjAyMTA5MzAxNjU2MDVagQ8yMDIyMDkzMDE3MDYwNVowggE6BgUqhQNkcASC
AS8wggErDCsi0JrRgNC40L/RgtC+0J/RgNC+IENTUCIgKNCy0LXRgNGB0LjRjyA0
LjApDCwi0JrRgNC40L/RgtC+0J/RgNC+INCj0KYiICjQstC10YDRgdC40LggMi4w
KQxp0KHQtdGA0YLQuNGE0LjQutCw0YIg0YHQvtC+0YLQstC10YLRgdGC0LLQuNGP
INCk0KHQkSDQoNC+0YHRgdC40Lgg0KHQpC8xMjQtMzk2NiDQvtGCIDE1INGP0L3Q
stCw0YDRjyAyMDIxDGPQodC10YDRgtC40YTQuNC60LDRgiDRgdC+0L7RgtCy0LXR
gtGB0YLQstC40Y8g0KTQodCRINCg0L7RgdGB0LjQuCDihJYg0KHQpC8xMjgtMzU5
MiDQvtGCIDE3LjEwLjIwMTgwZwYDVR0fBGAwXjAtoCugKYYnaHR0cDovL2NkcDIu
aXRrMjMucnUvaXRjb20yMDEyLTIwMjAuY3JsMC2gK6AphidodHRwOi8vY2RwMS5p
dGsyMy5ydS9pdGNvbTIwMTItMjAyMC5jcmwwggFgBgNVHSMEggFXMIIBU4AUXLeC
VuGgdIOZQ4QE8vqseYAxeU+hggEspIIBKDCCASQxHjAcBgkqhkiG9w0BCQEWD2Rp
dEBtaW5zdnlhei5ydTELMAkGA1UEBhMCUlUxGDAWBgNVBAgMDzc3INCc0L7RgdC6
0LLQsDEZMBcGA1UEBwwQ0LMuINCc0L7RgdC60LLQsDEuMCwGA1UECQwl0YPQu9C4
0YbQsCDQotCy0LXRgNGB0LrQsNGPLCDQtNC+0LwgNzEsMCoGA1UECgwj0JzQuNC9
0LrQvtC80YHQstGP0LfRjCDQoNC+0YHRgdC40LgxGDAWBgUqhQNkARINMTA0Nzcw
MjAyNjcwMTEaMBgGCCqFAwOBAwEBEgwwMDc3MTA0NzQzNzUxLDAqBgNVBAMMI9Cc
0LjQvdC60L7QvNGB0LLRj9C30Ywg0KDQvtGB0YHQuNC4ggsArGsYjQAAAAAE+zAd
BgNVHQ4EFgQUfbTOaI2YbC4qyFjOWrEgyr2FWiMwCgYIKoUDBwEBAwIDQQDPeewv
j8mpj2KTE2doICsDWvjPJZGlpYyub0LqTJyMNRBrw61ou/uek4dqCVIzsu3yAiEM
yY5ekzckO4QtX6va
-----END CERTIFICATE-----
"""

    certpem_M = """
-----BEGIN CERTIFICATE-----
MIIJZDCCCRGgAwIBAgIQAdbNbgBattAAAABUEu8AATAKBggqhQMHAQEDAjCCAVMx
KDAmBgNVBAMMH9CT0KPQmNChINCh0LXQstCw0YHRgtC+0L/QvtC70Y8xKDAmBgNV
BAoMH9CT0KPQmNChINCh0LXQstCw0YHRgtC+0L/QvtC70Y8xCzAJBgNVBAYTAlJV
MS0wKwYDVQQIDCQ5MiDQs9C+0YDQvtC0INCh0LXQstCw0YHRgtC+0L/QvtC70Ywx
IzAhBgNVBAcMGtCzLiDQodC10LLQsNGB0YLQvtC/0L7Qu9GMMRwwGgYJKoZIhvcN
AQkBFg1jYUBzZXYuZ292LnJ1MUgwRgYDVQQJDD/Qv9GA0L7RgdC/0LXQutGCINCT
0LXQvdC10YDQsNC70LAg0J7RgdGC0YDRj9C60L7QstCwLCDQtNC+0LwgMTMxGjAY
BggqhQMDgQMBARIMMDA5MjA0MDAzODYzMRgwFgYFKoUDZAESDTExNDkyMDQwMDcz
MjUwHhcNMjAxMjA4MTQyNTMzWhcNMjExMjA4MTQyNTMzWjCCAfIxgZgwgZUGA1UE
AwyBjdCg0LXQs9C40L7QvdCw0LvRjNC90LDRjyDQuNC90YTQvtGA0LzQsNGG0LjQ
vtC90L3QsNGPINGB0LjRgdGC0LXQvNCwINCz0L7RgNC+0LTQsCDQodC10LLQsNGB
0YLQvtC/0L7Qu9GPINCyINGB0YTQtdGA0LUg0L7QsdGA0LDQt9C+0LLQsNC90LjR
jzFnMGUGA1UECgxe0JTQtdC/0LDRgNGC0LDQvNC10L3RgiDRhtC40YTRgNC+0LLQ
vtCz0L4g0YDQsNC30LLQuNGC0LjRjyDQs9C+0YDQvtC00LAg0KHQtdCy0LDRgdGC
0L7Qv9C+0LvRjzELMAkGA1UEBhMCUlUxIjAgBgNVBAgMGTkyINCh0LXQstCw0YHR
gtC+0L/QvtC70YwxHzAdBgNVBAcMFtCh0LXQstCw0YHRgtC+0L/QvtC70Y8xHjAc
BgkqhkiG9w0BCQEWD3Jpc29Ac2V2Lmdvdi5ydTFEMEIGA1UECQw70J/RgNC+0YHQ
v9C10LrRgiDQk9C10L3QtdGA0LDQu9CwINCe0YHRgtGA0Y/QutC+0LLQsCwg0LQu
MTMxGjAYBggqhQMDgQMBARIMMDA5MjA0MDAzODYzMRgwFgYFKoUDZAESDTExNDky
MDQwMDczMjUwZjAfBggqhQMHAQEBATATBgcqhQMCAiQABggqhQMHAQECAgNDAARA
whzW2msXsyNxNlqBPkgeN+TAy/CpuyFwrFje6sQ0qYxHjtCoyYjwbnKUSS9CsvPr
5Z4QRfoeyaqwHO2Crh4EZIEJADEyRUYwMDAxo4IFCjCCBQYwCwYDVR0PBAQDAgP4
MC4GA1UdJQQnMCUGCCsGAQUFBwMEBgYqhQNkAgIGByqFAwICIgYGCCsGAQUFBwMC
MAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFAeL+uVrEtx9teLo8FKNZUS5HnCKMIGb
BgUqhQNkbwSBkQyBjtCh0YDQtdC00YHRgtCy0L4g0LrRgNC40L/RgtC+0LPRgNCw
0YTQuNGH0LXRgdC60L7QuSDQt9Cw0YnQuNGC0Ysg0LjQvdGE0L7RgNC80LDRhtC4
0LggIlZpUE5ldCBDU1AgNC4yIiAo0LLQsNGA0LjQsNC90YIg0LjRgdC/0L7Qu9C9
0LXQvdC40Y8gMikwggHVBgUqhQNkcASCAcowggHGDIGO0KHRgNC10LTRgdGC0LLQ
viDQutGA0LjQv9GC0L7Qs9GA0LDRhNC40YfQtdGB0LrQvtC5INC30LDRidC40YLR
iyDQuNC90YTQvtGA0LzQsNGG0LjQuCAiVmlQTmV0IENTUCA0LjIiICjQstCw0YDQ
uNCw0L3RgiDQuNGB0L/QvtC70L3QtdC90LjRjyAyKQxt0J/RgNC+0LPRgNCw0LzQ
vNC90YvQuSDQutC+0LzQv9C70LXQutGBICJWaVBOZXQg0KPQtNC+0YHRgtC+0LLQ
tdGA0Y/RjtGJ0LjQuSDRhtC10L3RgtGAIDQgKNCy0LXRgNGB0LjRjyA0LjYpIgxe
0KHQtdGA0YLQuNGE0LjQutCw0YIg0YHQvtC+0YLQstC10YLRgdGC0LLQuNGPIOKE
liDQodCkLzEyNC0zNDMzINC+0YIgMDYg0LjRjtC70Y8gMjAxOCDQs9C+0LTQsAxk
0KHQtdGA0YLQuNGE0LjQutCw0YIg0YHQvtC+0YLQstC10YLRgdGC0LLQuNGPIOKE
liDQodCkLzExOC0zNTEwINC+0YIgMjUg0L7QutGC0Y/QsdGA0Y8gMjAxOCDQs9C+
0LTQsDBsBggrBgEFBQcBAQRgMF4wKwYIKwYBBQUHMAGGH2h0dHA6Ly9jcmwuc2V2
Lmdvdi5ydTo4Nzc3L29jc3AwLwYIKwYBBQUHMAKGI2h0dHA6Ly9jcmwuc2V2Lmdv
di5ydS91Y3BzLTIwMTkuY2VyMDMGA1UdHwQsMCowKKAmoCSGImh0dHA6Ly9jcmwu
c2V2Lmdvdi5ydS9zYXMtMjAxOS5jcmwwggFfBgNVHSMEggFWMIIBUoAU5u9DiAcy
LUutFOAwDPu/JmRVaXehggEspIIBKDCCASQxHjAcBgkqhkiG9w0BCQEWD2RpdEBt
aW5zdnlhei5ydTELMAkGA1UEBhMCUlUxGDAWBgNVBAgMDzc3INCc0L7RgdC60LLQ
sDEZMBcGA1UEBwwQ0LMuINCc0L7RgdC60LLQsDEuMCwGA1UECQwl0YPQu9C40YbQ
sCDQotCy0LXRgNGB0LrQsNGPLCDQtNC+0LwgNzEsMCoGA1UECgwj0JzQuNC90LrQ
vtC80YHQstGP0LfRjCDQoNC+0YHRgdC40LgxGDAWBgUqhQNkARINMTA0NzcwMjAy
NjcwMTEaMBgGCCqFAwOBAwEBEgwwMDc3MTA0NzQzNzUxLDAqBgNVBAMMI9Cc0LjQ
vdC60L7QvNGB0LLRj9C30Ywg0KDQvtGB0YHQuNC4ggpcmoPpAAAAAAN/MB0GA1Ud
IAQWMBQwCAYGKoUDZHEBMAgGBiqFA2RxAjAKBggqhQMHAQEDAgNBAOwwJkZvNIoK
dlb7odyldvX+B0fnIPgsdg9xX0m/kOqJsG02NwkHScgvLeVa9od9/rTUFdOGgL7n
OI0Qr5xTfGoK
-----END CERTIFICATE-----
"""

#Если задан параметр, то читаем сертификат из файла
    if len(sys.argv) == 2:
        c1 = Certificate(sys.argv[1])
    else:
        c1 = Certificate(certpem)

    if (c1.pyver == ''):
        print('Context for certificate not create')
        exit(-1)
    print('=================formatCert================================')
    print(c1.formatCert)
    print('=================subjectSignTool================================')
    res = c1.subjectSignTool()
    print (res)
    print('=================issuerSignTool================================')
    res1 = c1.issuerSignTool()
    for ist in range(len(res1)):
        print ('СТРОКА_' + str(ist) + '=' + res1[ist])
    print('=================classUser================================')
    res3 = c1.classUser()
    print (res3)
    print('=================issuerCert================================')
    iss, vlad_is = c1.issuerCert()
    print ('vlad_is=' + str(vlad_is))
    for key in iss.keys():
        print (key + '=' + iss[key])
    print('=================subjectCert================================')
    sub, vlad_sub = c1.subjectCert()
    print ('vlad_sub=' + str(vlad_sub))
    for key in sub.keys():
        print (key + '=' + sub[key])
    print('=================publicKey================================')
    key_info = c1.publicKey()
    if (key_info['algo'].find("1.2.840.113549.1.1") != -1):
        print ('Public key algorithm: ' + key_info['algo'])
        print ('The RSA')
    elif(len(key_info) > 0):
        print ('Public key algorithm: ' + key_info['algo'])
        print ('Parametr key (curve): ' + key_info['curve'])
        if (key_info['hash'] != ''):
    	    print ('Parametr hash: ' + key_info['hash'])
        print ('Value public key: ' + key_info['valuepk'])
    print('=================serialNumber================================')
    print(c1.serialNumber())
    print('=================validityCert================================')
    valid = c1.validityCert()
    print(valid['not_after'])
    print(valid['not_before'])
    print('=================signatureCert================================')
    algosign, value = c1.signatureCert()
    print(algosign)
    print(value)
    print('================KeyUsage=================================')
    ku = c1.KeyUsage()
    for key in ku:
        print (key)
    print('================IdentificationKind=================================')
    idkind = c1.identKind()
    print('type identification kind=' + str(idkind))
    print('================Private Key Usage Period=================================')
    period = c1.keyPeriod()
    print('not_before='  + str(period['not_before']))
    print('not_after=' + str(period['not_after']))
    print('================END=================================')
    