#!/usr/bin/env python

class HesapMakinasi:

    def __init__(self):
        pass

    def secenek_sun(self) -> int:
        secenek = input("""---------------------------------------------------------
        \n   yapmak istediginiz islemi seciniz:
        \n - Toplama, 1
        \n - Çıkartma, 2
        \n - Çarpma, 3
        \n - Bölme, 4
        \n   Seçiniz:""")

        return int(secenek)


    def topla(self,sayi1:int, sayi2:int):
        return sayi1 + sayi2

    def cikart(self,sayi1:int, sayi2:int):
        return sayi1 - sayi2

    def carp(self,sayi1:int, sayi2:int):
        return sayi1 * sayi2

    def bol(self,sayi1:int, sayi2:int):
        return sayi1 / sayi2

    def islemlere_basla(self):
        while True:
            secenek = self.secenek_sun()
            sayi1 = int(input("sayı1 i giriniz: "))
            sayi2 = int(input("sayı1 i giriniz: "))

            if secenek == 1:
                print(self.topla(sayi1,sayi2))
            elif secenek == 2:
                print(self.cikart(sayi1,sayi2))
            elif secenek == 3:
                print(self.carp(sayi1,sayi2))
            elif secenek == 4:
                print(self.bol(sayi1,sayi2))
            else:
                print("yanlış seçenek")

            devammi = input("devam etmek için e, çıkmak için h: ")
            if devammi =="h":
                break




