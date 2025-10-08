class Fahrzeug:
    def Fahrzeug(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int):
        self.__kenzeichen = kennzeichen
        self.__hersteller = hersteller
        self.__modell = modell
        self.__baujahr = baujahr

class PKW(Fahrzeug):
    def PKW(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, anzahlTueren: int):
        self.__kenzeichen = kennzeichen
        self.__hersteller = hersteller
        self.__modell = modell
        self.__baujahr = baujahr
        self.__anzahlTueren = anzahlTueren

class LKW(Fahrzeug):
    def LKW(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, ladekapazitaetKG: int):
        self.__kenzeichen = kennzeichen
        self.__hersteller = hersteller
        self.__modell = modell
        self.__baujahr = baujahr
        self.__ladekapazitaetKG = ladekapazitaetKG