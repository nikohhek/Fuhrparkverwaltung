class Fahrzeug:
    def Fahrzeug(self, kennzeichen, hersteller, modell, baujahr):
        self.__kenzeichen = kennzeichen
        self.__hersteller = hersteller
        self.__modell = modell
        self.__baujahr = baujahr

class PKW(Fahrzeug):
    def PKW(self, kennzeichen, hersteller, modell, baujahr, anzahlTueren):
        self.__kenzeichen = kennzeichen
        self.__hersteller = hersteller
        self.__modell = modell
        self.__baujahr = baujahr
        self.__anzahlTueren = anzahlTueren

class LKW(Fahrzeug):
    def LKW(self, kennzeichen, hersteller, modell, baujahr, ladekapazitaetKG):
        self.__kenzeichen = kennzeichen
        self.__hersteller = hersteller
        self.__modell = modell
        self.__baujahr = baujahr
        self.__ladekapazitaetKG = ladekapazitaetKG