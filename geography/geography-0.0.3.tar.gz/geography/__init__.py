import json
import math


class JsonImports:
    alpha3List = json.loads(open(r"data/json/lists/countries/alpha3List.json", encoding='utf8').read())
    alpha3ToAreaKMm = json.loads(open(r"data/json/dicts/countries/alpha3ToAreaKM.json", encoding='utf8').read())
    alpha3ToCapital = json.loads(open(r"data/json/dicts/countries/alpha3ToCapital.json", encoding='utf8').read())
    alpha3ToContinent = json.loads(open(r"data/json/dicts/countries/alpha3ToContinent.json", encoding='utf8').read())
    alpha3ToFlagURL = json.loads(open(r"data/json/dicts/countries/alpha3ToFlagURL.json", encoding='utf8').read())
    alpha3ToGDP = json.loads(open(r"data/json/dicts/countries/alpha3ToGDP.json", encoding='utf8').read())
    alpha3ToLargestCity = json.loads(open(r"data/json/dicts/countries/alpha3ToLargestCity.json", encoding='utf8').read())
    alpha3ToPopulation = json.loads(open(r"data/json/dicts/countries/alpha3ToPopulation.json", encoding='utf8').read())
    countryNameList = json.loads(open(r"data/json/lists/countries/countryNameList.json", encoding='utf8').read())
    nameToAlpha3 = json.loads(open(r"data/json/dicts/countries/nameToAlpha3.json", encoding='utf8').read())
    usaStateAlphaToAreaKM= json.loads(open(r"data/json/dicts/usaStates/usaStatesAreaKM.json", encoding='utf8').read())
    usaStateAlphaToCapital = json.loads(open(r"data/json/dicts/usaStates/usaStatesCapital.json", encoding='utf8').read())
    usaStateAlphaToLargestCity = json.loads(open(r"data/json/dicts/usaStates/usaStatesLargestCity.json", encoding='utf8').read())
    usaStateAlphaToFlagURL = json.loads(open(r"data/json/dicts/usaStates/usaStateFlagURL.json", encoding='utf8').read())
    usaStateNameToAlpha = json.loads(open(r"data/json/dicts/usaStates/usaStateNameToAlpha.json", encoding='utf8').read())
    usaStateNameList = json.loads(open(r"data/json/lists/usaStates/usaStatesNameList.json", encoding='utf8').read())
    usaStateType = json.loads(open(r"data/json/dicts/usaStates/usaStatesType.json", encoding='utf8').read())


class Countries:

    @classmethod
    def doesCountryExist(cls, alpha3: str):
        if Countries.getRedirectedNameToAlpha3(alpha3) in JsonImports.alpha3List:
            return True
        else:
            return False

    @classmethod
    def getAreaInKM(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            return JsonImports.alpha3ToAreaKMm[alpha3.upper()]

    @classmethod
    def getAreaInMiles(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            return math.ceil(int(JsonImports.alpha3ToAreaKMm[alpha3.upper()]) / 2.59)

    @classmethod
    def getCapital(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            return JsonImports.alpha3ToCapital[Countries.getRedirectedNameToAlpha3(alpha3)]

    @classmethod
    def getContinent(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            return JsonImports.alpha3ToContinent[alpha3.upper()]

    @classmethod
    def getCountryAreaRanking(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            newSorted = dict(sorted(JsonImports.alpha3ToAreaKMm.items(), key=lambda kv: kv[1], reverse=True))
            rank = 0
            for count, item in enumerate(newSorted):
                if str(item) == alpha3.upper():
                    rank = count + 1
            return rank

    @classmethod
    def getFlagURL(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            return JsonImports.alpha3ToFlagURL[Countries.getRedirectedNameToAlpha3(alpha3)]

    @classmethod
    def getGDP(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            return JsonImports.alpha3ToGDP[alpha3.upper()]

    @classmethod
    def getGDPRanking(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            gdpDict = {}
            for count, item in enumerate(JsonImports.alpha3List):
                if Countries.getGDP(item) is None:
                    pass
                else:
                    gdpDict[item] = Countries.getGDP(item)
            newSorted = dict(sorted(gdpDict.items(), key=lambda kv: kv[1], reverse=True))
            rank = 0
            for count, item in enumerate(newSorted):
                if str(item) == alpha3.upper():
                    rank = count + 1
            return rank

    @classmethod
    def getGdpPerCapita(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            try:
                return int(JsonImports.alpha3ToGDP[alpha3.upper()] / JsonImports.alpha3ToPopulation[alpha3.upper()])
            except TypeError:
                return None

    @classmethod
    def getGdpPerCapitaRanking(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            gdpPerCapitaDict = {}
            for count, item in enumerate(JsonImports.alpha3List):
                if Countries.getGdpPerCapita(item) is None:
                    pass
                else:
                    gdpPerCapitaDict[item] = Countries.getGdpPerCapita(item)
            newSorted = dict(sorted(gdpPerCapitaDict.items(), key=lambda kv: kv[1], reverse=True))
            rank = 0
            for count, item in enumerate(newSorted):
                if str(item) == alpha3.upper():
                    rank = count + 1
            return rank

    @classmethod
    def getGdpPerCapitaRankingDict(cls):
        gdpPerCapitaDict = {}
        for count, item in enumerate(JsonImports.alpha3List):
            if Countries.getGdpPerCapita(item) is None:
                pass
            else:
                gdpPerCapitaDict[item] = Countries.getGdpPerCapita(item)
        newSorted = dict(sorted(gdpPerCapitaDict.items(), key=lambda kv: kv[1], reverse=True))
        rank = 0
        rankingDict = {}
        for count, item in enumerate(newSorted):
            rankingDict[count + 1] = item
        return rankingDict

    @classmethod
    def getLargestCity(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            return JsonImports.alpha3ToLargestCity[alpha3.upper()]

    @classmethod
    def getPopulation(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            return JsonImports.alpha3ToPopulation[alpha3.upper()]

    @classmethod
    def getPopulationRanking(cls, alpha3: str):
        if Countries.doesCountryExist(alpha3) is False:
            return None
        else:
            newSorted = dict(sorted(JsonImports.alpha3ToPopulation.items(), key=lambda kv: kv[1], reverse=True))
            rank = 0
            for count, item in enumerate(newSorted):
                if str(item) == alpha3.upper():
                    rank = count + 1
            return rank

    @classmethod
    def getRedirectedNameToAlpha3(cls, name: str):
        if name is None:
            return None
        elif name.upper() in JsonImports.alpha3List:
            return name.upper()
        elif name.title().replace("_", " ") in JsonImports.countryNameList:
            return JsonImports.nameToAlpha3[name.upper().replace(" ", "_")]
        else:
            return None


class UsaStates:

    @classmethod
    def doesStateExist(cls, usStateAlpha: str):
        if UsaStates.getRedirectedNameToAlpha(usStateAlpha) in JsonImports.usaStateAlphaToCapital:
            return True
        else:
            return False

    @classmethod
    def getAreaKM(cls, usStateAlpha: str):
        if UsaStates.doesStateExist(usStateAlpha) is False:
            return None
        else:
            return JsonImports.usaStateAlphaToAreaKM[UsaStates.getRedirectedNameToAlpha(usStateAlpha)]

    @classmethod
    def getAreaMiles(cls, usStateAlpha: str):
        if UsaStates.doesStateExist(usStateAlpha) is False:
            return None
        else:
            return math.ceil(int(JsonImports.alpha3ToAreaKMm[UsaStates.getRedirectedNameToAlpha(usStateAlpha)]) / 2.59)

    @classmethod
    def getCapital(cls, usStateAlpha: str):
        if UsaStates.doesStateExist(usStateAlpha) is False:
            return None
        else:
            return JsonImports.usaStateAlphaToCapital[UsaStates.getRedirectedNameToAlpha(usStateAlpha)]

    @classmethod
    def getFlagURL(cls, usStateAlpha: str):
        if UsaStates.doesStateExist(usStateAlpha) is False:
            return None
        else:
            return JsonImports.usaStateAlphaToFlagURL[UsaStates.getRedirectedNameToAlpha(usStateAlpha)]

    @classmethod
    def getLargestCity(cls, usStateAlpha: str):
        if UsaStates.doesStateExist(usStateAlpha) is False:
            return None
        else:
            return JsonImports.usaStateAlphaToLargestCity[UsaStates.getRedirectedNameToAlpha(usStateAlpha)]

    @classmethod
    def getRedirectedNameToAlpha(cls, name: str):
        if name is None:
            return None
        elif name.upper() in JsonImports.alpha3List:
            return name.upper()
        elif name.title().replace("_", " ") in JsonImports.countryNameList:
            return JsonImports.usaStateNameToAlpha[name.upper().replace(" ", "_")]
        else:
            return None

    @classmethod
    def getStateType(cls, usStateAlpha: str):
        if UsaStates.doesStateExist(usStateAlpha) is False:
            return None
        else:
            return JsonImports.usaStateType[UsaStates.getRedirectedNameToAlpha(usStateAlpha)]
