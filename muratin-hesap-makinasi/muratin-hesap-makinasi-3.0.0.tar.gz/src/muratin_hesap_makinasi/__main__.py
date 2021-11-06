#!/usr/bin/env python
from .hesap_makinasi import HesapMakinasi

print("===========NAME===========")
print(__name__)
print("==========================")


def main():
    hm = HesapMakinasi()
    hm.islemlere_basla()


# eğer hazırladığımız paket aynı zamanda kend ibaşına çalışan bir uygulama ise kullanılır. 
# doğrudan çalıştırıldığında uygulamanın ayağa kalması için gerekli kodlar buradan başlatılır
if __name__ == "__main__":
    main()