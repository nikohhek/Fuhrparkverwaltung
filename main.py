class Fahrzeug:
    def __init__(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int):
        self.__kennzeichen = kennzeichen
        self.__hersteller = hersteller
        self.__modell = modell
        self.__baujahr = baujahr

    def getKennzeichen(self) -> str:
        return self.__kennzeichen

    def getHersteller(self) -> str:
        return self.__hersteller

    def getModell(self) -> str:
        return self.__modell

    def getBaujahr(self) -> int:
        return self.__baujahr


class PKW(Fahrzeug):
    def __init__(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, anzahlTueren: int):
        self.__kenzeichen = kennzeichen
        self.__hersteller = hersteller
        self.__modell = modell
        self.__baujahr = baujahr
        self.__anzahlTueren = anzahlTueren

    def getAnzahlTueren(self) -> str:
        return self.__anzahlTueren


class LKW(Fahrzeug):
    def __init__(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, ladekapazitaetKG: int):
        self.__kenzeichen = kennzeichen
        self.__hersteller = hersteller
        self.__modell = modell
        self.__baujahr = baujahr
        self.__ladekapazitaetKG = ladekapazitaetKG

    def getLadekapazitaetKG(self) -> int:
        return self.__ladekapazitaetKG


class Fuhrpark:
    def __init__(self, fahrzeuge: list):
        self.__fahrzeuge = fahrzeuge

    def getFahrzeuge(self) -> list:
        return self.__fahrzeuge

    def getFahrzeugDaten(self, kennzeichen: str) -> dict:
        pass

    def addPKW(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, anzahlTueren: int):
        for fahrzeug in self.__fahrzeuge:
            if fahrzeug == kennzeichen:
                print(f"Fahrzeug mit Kennzeichen {kennzeichen} ist bereits gepflegt.")
                pass
        kennzeichen = PKW(kennzeichen, hersteller, modell, baujahr, anzahlTueren)
        self.__fahrzeuge.append(kennzeichen)


def main():
    TestFuhrpark = Fuhrpark([])
    TestFuhrpark.addPKW("SU-N-9513", "Seat", "Leon", 2002, 5)
    TestFuhrpark.addPKW("SU-SJ-513", "Fiat", "Fullback", 2017, 5)
    TestFuhrpark.addPKW("BM-CC-0815", "Mercedes", "GLB", 2022, 5)
    print(TestFuhrpark.getFahrzeuge())

main()