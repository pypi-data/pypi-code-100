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
#    	    print (self.cert_full["signatureAlgorithm"])
#    	    print (self.cert_full["signatureAlgorithm"]['algorithm'])
#    	    print (self.cert_full["signatureValue"].prettyPrint())
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
                if sys.platform != "win32":
                    seek = 4
                else:
                    seek = 4
#Проверка версии python-а
                if (self.pyver == '2'):
#                    print ('V==2')
                    return ext['extnValue'][seek-2:]
                seek = seek - 2
#                print ('V!=2')
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
        #Ищем расширение subjectSignTool
        if(str(ext['extnID']) == "1.2.643.100.112"):
                #Его значение надо возвращать
                vv = ext['extnValue']
#                print(vv)
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
                    of2 += 1
# Поля issuerSignTools		    
                fsbCA = []
#Длина первого поля
#                print(of2)
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
                            
#                            fsb = val1
#                    print(fsb)
                    fsbCA.append(fsb)
                    of2 += (ltek + 2)
#Возврат значений issuerSignTools
                return(fsbCA)
    return ([])
    	
  def classUser(self):
    if(self.cert == ''):
        return ('')
    for ext in self.cert["extensions"]:
        #Ищем расширение subjectSignTool
        if(str(ext['extnID']) == "2.5.29.32"):
                print ('2.5.29.32')
                #Классы защищенности
                #		    print (ext['extnValue'])
#Переводит из двоичной системы счисления (2) в hex
                kc = ext['extnValue'].prettyPrint()
#                print(kc)
#Сдвиг на 0x
#Проверка версии python-а
                if (self.pyver == '2'):
            	    kc_hex = kc[2:]
                else:
            	    kc_hex = kc[2:]
#                print(kc_hex)
# 4 - длина заголовка 			
                kc_hex = kc_hex[4:]
#                print(kc_hex)
                i32 = kc_hex.find('300806062a85036471')
                tmp_kc = ''
                while (i32 != -1 ) :
                    #'300806062a85036471' - 10 байт бинарных и 20 hex-овых; 4 - это 3008
#                    print ('НАШЛИ КС i32=' + str(i32))
                    kcc_tek = kc_hex[i32+4: i32 + 20]
#			print (kcc_tek)
                    oid_kc = self.notation_OID(kcc_tek)
#                    print (oid_kc)
                    tmp_kc = tmp_kc + oid_kc +';;'
                    kc_hex = kc_hex[i32 + 20:]
                    i32 = kc_hex.find('300806062a85036471')

#		    for ext1 in ext:
#			    print (ext1)
#                print ('2.5.29.32 END')
#		    print (ext['extnID'])
#		    print (ext['extnValue'])
                return (tmp_kc)
    return ('')


  def parse_issuer_subject (self, who):
    if(self.cert == ''):
        return ({})
    infoMap = {
        "1.2.840.113549.1.9.2": "unstructuredName",
        "1.2.643.100.1": "OGRN",
        "1.2.643.100.5": "OGRNIP",
        "1.2.643.3.131.1.1": "INN",
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
    vlad_o = 0
    for rdn in self.cert[who][0]:
        if not rdn:
            continue
        oid = str(rdn[0][0])
#            oid = str(rdn[0]['type'])
        value = rdn[0][1]
#            value = rdn[0]['value']
#SNILS
        if(oid == '1.2.643.100.3'):
            vlad = 1
#OGRN
        elif(oid == '1.2.643.100.1'):
            vlad = 2
#O
        elif(oid == '2.5.4.10'):
            vlad_o = 1
        value = value[2:]
#        print(value)
        if (self.pyver == '3'):
#    	    value = str(value).encode('raw_unicode_escape').decode('utf8')
            val = value.prettyPrint()
#            if (len(val) > 2 and val[1] != '\''):
#            if ((len(val) > 1 and val[1] != '\'') or (len(val) == 2 and (val[0] == '\xD0' or val[0] == '\xD1'))):
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
        if(vlad_o == 1):
            vlad = 2
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
#        print(kk[-3:-1])
        #Избавляемся от "' в начале строки и 'B" и конце строки
        kk = kk[2:-3]
#Переводит из двоичной системы счисления (2) в целое
        kkh=int(kk, 2)
##    else: 
        #В MS из десятичной системы в целое
##        kkh=int(kk, 10)
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
##    if sys.platform != "win32":
    if kk[-3:-1] == "'B":
#        print(kk[-3:-1])
        #Избавляемся от "' в начале строки и 'B" и конце строки
        kk = kk[2:-3]
#Переводит из двоичной системы счисления (2) в целое
        kkh=int(kk, 2)
##    else: 
        #В MS из десятичной системы в целое
##        kkh=int(kk, 10)
    else:
       kkh=int(kk, 10)
#    print (kkh)
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
#    if isinstance(not_before, GeneralizedTime):
#        not_before = datetime.strptime(not_before, '%Y%m%d%H%M%SZ')
#    else:
    validity_cert['not_before'] = datetime.strptime(not_before, '%y%m%d%H%M%SZ')

#    if isinstance(not_after, GeneralizedTime):
#        not_after = datetime.strptime(not_after, '%Y%m%d%H%M%SZ')
#    else:
    validity_cert['not_after'] = datetime.strptime(not_after, '%y%m%d%H%M%SZ')

#    print (validity_cert) 
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
        print ('2.5.29.15')
        os16 = ext['extnValue'].prettyPrint()
#        print(os16)
        os16 = '0404' + os16[2:]
#        print(os16)
        os = binascii.unhexlify(os16[0:])
        octet_strings = os
        e, f= decoder.decode(decoder.decode(octet_strings)[0], rfc2459.KeyUsage())
#        print (e)
        n = 0
        while n < len(e):
          if e[n]:
            ku.append(X509V3_KEY_USAGE_BIT_FIELDS[n])
#            print(X509V3_KEY_USAGE_BIT_FIELDS[n])
          n += 1
        return(ku)
    return ([])

  def Extensions(self):
    return (self.cert["extensions"])


if __name__ == "__main__":

#For test
    certpem = """
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
    res = c1.subjectSignTool()
    print('=================subjectSignTool================================')
    print (res)
    print('=================issuerSignTool================================')
    res1 = c1.issuerSignTool()
    for ist in range(len(res1)):
        print (str(ist) + '=' + res1[ist])
    print('=================classUser================================')
    res2 = c1.prettyPrint()
#    print(res2)
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
#    print(ku)
    print('================END=================================')
    
    