try:
    import upsidedown  
    
except (ModuleNotFoundError, ImportError):
    pass

try:
    from zalgo_text import zalgo as zalg
    
except (ModuleNotFoundError, ImportError):
    pass

try:
    from nltk import pos_tag, word_tokenize
    
except (ModuleNotFoundError, ImportError):
    pass

import random

from .exception import *

gen = random.SystemRandom()

class teg:
    def __init__(self):
        try:
            self.zal = zalg.zalgo()
            
        except NameError:
            pass
        
    def _objrepl(self, str_, a, b):
        """Function dependency of rouxls()"""
        out = str(str_).replace(a.lower(), b.lower())
        out = str(out).replace(a.title(), b.title())
        out = str(out).replace(a.upper(), b.upper())
        return out
    
    def _objreplic(self, str_, a, b):
        out = str(str_).replace(a.lower(), b)
        out = str(out).replace(a.title(), b)
        out = str(out).replace(a.upper(), b)
        return out
        
    def udown(self, intext):
        """Generates upside-down text"""
        try:
            return upsidedown.transform(str(intext))
        
        except NameError:
            raise ModuleError("Upsidedown must be installed. Try pip install upsidedown or pip install beetroot[text].")
        
    def zalgo(self, intext, **kwargs):
        """Generates Zalgo text"""
        craziness = float(
            kwargs.get(
                "crazy",
                1
            )
        )
        try:
            self.zal.numAccentsUp = (round(craziness), round(craziness * 10))
            self.zal.numAccentsDown = (round(craziness), round(craziness * 10))
            self.zal.numAccentsMiddle = (round(craziness), round(craziness * 10))
            self.zal.maxAccentsPerLetter = round(craziness * 40)
            return self.zal.zalgofy(str(intext))
        
        except NameError:
            raise ModuleError("Zalgo_text must be installed. Try pip install zalgo-text or pip install beetroot[text].")
        
    def rouxls(self, sentence):
        try:
            yee = pos_tag(word_tokenize(sentence))
            
            out = []
            for i in range(0, len(yee)):
                if yee[i][1].startswith("NN") or yee[i][1].startswith("VB"):
                    dumb = random.randint(1, 100)
                    if dumb <= 40:
                        if yee[i][0].endswith("a") or yee[i][0].endswith("e") or yee[i][0].endswith("i") or yee[i][0].endswith("o") or yee[i][0].endswith("u"):
                            out.append("".join([str(yee[i][0]), "th"]))
                            
                        elif yee[i][0].endswith("s"):
                            if yee[i][0].endswith("es"):
                                out.append("".join([str(yee[i][0]), "t"]))
                                
                            else:
                                out.append("".join([str(yee[i][0]), "e"]))
                            
                        elif yee[i][0].endswith("y"):
                            out.append("".join([str(yee[i][0])[:-1], "ie"]))
                            
                        else:
                            out.append("".join([str(yee[i][0]), "eth"]))
                        
                    elif dumb > 40 and dumb <= 80:
                        if yee[i][0].endswith("a") or yee[i][0].endswith("e") or yee[i][0].endswith("i") or yee[i][0].endswith("o") or yee[i][0].endswith("u"):
                            out.append("".join([str(yee[i][0]), "st"]))
                            
                        elif yee[i][0].endswith("s"):
                            if yee[i][0].endswith("es"):
                                out.append("".join([str(yee[i][0]), "t"]))
                                
                            else:
                                out.append("".join([str(yee[i][0]), "e"]))
                            
                        elif yee[i][0].endswith("y"):
                            out.append("".join([str(yee[i][0])[:-1], "ie"]))
                            
                        else:
                            out.append("".join([str(yee[i][0]), "est"]))

                    elif dumb > 80 and dumb <= 90:
                        if yee[i][1].startswith("NN"):
                            if yee[i][0].endswith("e"):
                                out.append(str(yee[i][0]))
                                
                            else:
                                out.append("".join([str(yee[i][0]), "e"]))
                            
                        else:
                            if yee[i][0].endswith("a") or yee[i][0].endswith("e") or yee[i][0].endswith("i") or yee[i][0].endswith("o") or yee[i][0].endswith("u"):
                                out.append("".join([str(yee[i][0]), "t"]))
                                
                            elif yee[i][0].endswith("s"):
                                if yee[i][0].endswith("es"):
                                    out.append("".join([str(yee[i][0]), "st"]))
                                
                                else:
                                    out.append("".join([str(yee[i][0]), "e"]))
                                
                            elif yee[i][0].endswith("y"):
                                out.append("".join([str(yee[i][0])[:-1], "ie"]))
                                
                            else:
                                out.append("".join([str(yee[i][0]), "est"]))

                    else:
                        out.append(str(yee[i][0]))
                        
                else:
                    out.append(str(yee[i][0]))
                    
            for i in range(0, len(out)):
                out[i] = self._objrepl(out[i], "you", "thou")
                out[i] = self._objrepl(out[i], "your", "thine")
                out[i] = self._objrepl(out[i], "have", "haste")
                out[i] = self._objrepl(out[i], "ahest", "ah")
                out[i] = self._objrepl(out[i], "aheth", "ah")
                out[i] = self._objrepl(out[i], "ahe", "ah")
                out[i] = self._objrepl(out[i], "ise", "is")
                out[i] = self._objrepl(out[i], "rouxls", "Rouxls, The Duketh of Puzzles")
                out[i] = self._objrepl(out[i], "rouxlse", "Rouxls, The Duketh of Puzzles")
                out[i] = self._objrepl(out[i], "Rouxls, The Duketh of Puzzlese", "Rouxls, The Duketh of Puzzles")
                out[i] = self._objrepl(out[i], "the", "thy")
                out[i] = self._objrepl(out[i], "thyre", "there")
                out[i] = self._objrepl(out[i], "thour", "your")
                out[i] = self._objrepl(out[i], "amest", "am")
                out[i] = self._objrepl(out[i], "ameth", "am")
                out[i] = self._objrepl(out[i], "asse", "arse")
                out[i] = self._objrepl(out[i], "real", "reale")
                    
            out = " ".join(out).replace(" '", "'").replace(" .", ".").replace(" ,", ",").replace(" !", "!").replace(" ?", "?")
            
            out = self._objrepl(out, "shuteth up", "shutteth. yon. uppeth.")
            out = self._objrepl(out, "shutest up", "shutteth. yon. uppeth.")
            
            return out
        
        except NameError:
            raise ModuleError("nltk must be installed to use beetroot.text.rouxls(). Try pip install nltk or pip install beetroot[text].")
            
    def spamton(self, sentence):
        try:
            yee = pos_tag(sentence.upper().split(" "))
            
            out = []
            for i in range(0, len(yee)):
                if yee[i][1].startswith("NN") or yee[i][1].startswith("VB"):
                    dumb = random.randint(1, 100)
                    if dumb <= 30:
                        out.append("".join(["[", str(yee[i][0]).lower().title(), "]"]))

                    elif dumb > 30 and dumb <= 40:
                        out.append("".join(["[[", str(yee[i][0]).lower().title(), "]]"]))
                        
                    elif dumb > 40 and dumb <= 60:
                        if yee[i][1] == "NN" or yee[i][1] == "NNS":
                            out.append("[[Hyperlink Blocked]]")
                            
                        elif yee[i][1] == "NNPS":
                            nnpsn = [
                                "LIGHT neRs",
                                "DARK neRs",
                                "[Friends]",
                                "[[Hearts]]"
                            ]
                            dumb3 = random.choice(nnpsn)
                            dumb3_1 = random.randint(0, 1)
                            if dumb3_1 == 0:
                                dumb3 = "".join(["[", dumb3, "]"])
                                
                            else:
                                dumb3 = "".join(["[[", dumb3, "]]"])
                                
                            out.append(dumb3)
                            
                        elif yee[i][1] == "NNP":
                            nnpn = [
                                "Kris",
                                "Salesman1997",
                                "Little Sponge",
                                "[[Hyperlink Blocked]]"
                            ]
                            dumb2 = random.choice(nnpn)
                            dumb2_1 = random.randint(0, 1)
                            if dumb2_1 == 0:
                                dumb2 = "".join(["[", dumb2, "]"])
                                
                            else:
                                dumb2 = "".join(["[[", dumb2, "]]"])
                                
                            out.append(dumb2)
                        
                        else:
                            out.append(str(yee[i][0]))
                        
                    else:
                        out.append(str(yee[i][0]))
                        
                else:
                    out.append(str(yee[i][0]))
                    
            for i in range(0, len(out)):
                out[i] = self._objreplic(out[i], "spamton", "[Spamton G. Spamton]")
                out[i] = self._objreplic(out[i], "strings", "Silly Strings")
                out[i] = self._objreplic(out[i], "soul", "HeartShapedObject")
                out[i] = self._objrepl(out[i], "special", "specil")
                
            out = " ".join(out).replace(" '", "'").replace(" .", ".").replace(" ,", ",").replace(" !", "!").replace(" ?", "?")
            
            return out
            
        except NameError:
            raise ModuleError("nltk must be installed to use beetroot.text.spamton(). Try pip install nltk or pip install beetroot[text].")
            
    def greek(self, text):
        greekalpha = list(str("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzΑΒΨΔΕΦΓΗΙΞΚΛΜΝΟΠ:ΡΣΤΘΩ΅ΧΥΖαβψδεφγηιξκλμνοπ;ρστθωςχυζABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzΑΒΨΔΕΦΓΗΙΞΚΛΜΝΟΠ:ΡΣΤΘΩ΅ΧΥΖαβψδεφγηιξκλμνοπ;ρστθωςχυζ"))
        
        text = list(self._objreplic(self._objreplic(str(text), "greek", "Ellihnika"), "english", "Agglika"))
        #print(text)
        for i in range(0, len(text)):
            try:
                spos = greekalpha.index(text[i])
                text[i] = greekalpha[spos + 52]
                
            except (ValueError, IndexError):
                pass
            
        return "".join(text)
    
    def russian(self, text):
        rusalpha = list(str("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯфисвуапршолдьтщзйкыегмцчняABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯфисвуапршолдьтщзйкыегмцчня"))
        
        text = list(self._objreplic(self._objreplic(str(text), "russian", "Heccrqq"), "english", "Ayukqqcrqq"))
        #print(text)
        for i in range(0, len(text)):
            try:
                spos = rusalpha.index(text[i])
                text[i] = rusalpha[spos + 52]
                
            except (ValueError, IndexError):
                pass
            
        return "".join(text)
    
    def reverse(self, text):
        return str(text)[::-1]
                    
text = teg()
del teg