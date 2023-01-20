import pysnmp
from pysnmp.hlapi import *
import time

def get_data(router_ip, oid_kutuphanesi):
    veri = {}
    for anahtar, deger in oid_kutuphanesi.items():
        hataGostergesi, hataDurumu, hataDizini, tamsayi = next(
            getCmd(SnmpEngine(), 
            CommunityData('Community', mpModel=0),
            UdpTransportTarget((router_ip,161)),
            ContextData(),
            ObjectType(ObjectIdentity(deger[1]))
            )
        )
        if hataGostergesi:
            print(hataGostergesi)
        else:
            if hataDurumu:
                print('%s at %s' % (hataDurumu.prettyPrint(),hataDizini and tamsayi[int(hataDizini)-1][0] or '?'))
            else:
                for varBind in tamsayi:
                    oid, deger = varBind
                    veri[anahtar] = deger
    return veri

while True:
    ipadresi = "ip address"
 #Bu oid kütüphanesi cisco 3725 router içindir
    oidkutuphanesi = {
                    "Model":("SNMPv2-MIB::sysDescr.0", "1.3.6.1.2.1.1.1.0"),
                    "Çalışma Zamanı":("SNMPv2-MIB::sysUpTime.0", "1.3.6.1.2.1.1.3.0"),
                    "Bağlı Arayüzler":("SNMPv2-SMI::mib-2.2.1.0", "1.3.6.1.2.1.2.1.0"),
                    "Alinan Voltaj":("null","1.3.6.1.4.1.14988.1.1.3.8.0"),
                    "Derece":("null","1.3.6.1.4.1.14988.1.1.3.10.0"),
                    "Bağlı Arayüz-1":("null","1.3.6.1.2.1.2.2.1.2.2"),
                    "Bağlı Arayüz-2":("null","1.3.6.1.2.1.2.2.1.2.1"),
                    "Bağlı Arayüz-3":("null","1.3.6.1.2.1.2.2.1.2.3"),
                    "Varsayılan Ağ Geçidi":("null","1.3.6.1.2.1.4.21.1.7" )
                    }
    
    veri = get_data(ipadresi,oidkutuphanesi)
    for key, deger in veri.items():
        print((f"{key}: {deger}"))
        
    time.sleep(20)
