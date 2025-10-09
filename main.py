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
        super().__init__(kennzeichen, hersteller, modell, baujahr)
        self.__anzahlTueren = anzahlTueren

    def getAnzahlTueren(self) -> str:
        return self.__anzahlTueren


class LKW(Fahrzeug):
    def __init__(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, ladekapazitaetKG: int):
        super().__init__(kennzeichen, hersteller, modell, baujahr)
        self.__ladekapazitaetKG = ladekapazitaetKG

    def getLadekapazitaetKG(self) -> int:
        return self.__ladekapazitaetKG


class Fuhrpark:
    def __init__(self, fahrzeuge: list):
        self.__fahrzeuge = fahrzeuge

    def getFahrzeuge(self) -> list:
        #for fahrzeug in self.__fahrzeuge:
            #print(SU_N_9513.getKennzeichen())
        return self.__fahrzeuge

    def getFahrzeugDaten(self, kennzeichen: str) -> dict:
        for fahrzeug in self.__fahrzeuge:
            if fahrzeug.getKennzeichen() == kennzeichen:
                if type(fahrzeug).__name__ == "PKW":
                    dataDict = {
                        "kennzeichen": fahrzeug.getKennzeichen(),
                        "hersteller": fahrzeug.getHersteller(),
                        "modell": fahrzeug.getModell(),
                        "baujahr": fahrzeug.getBaujahr(),
                        "anzahlTueren": fahrzeug.getAnzahlTueren()
                    }
                    return dataDict
                if type(fahrzeug).__name__ == "LKW":
                    dataDict = {
                        "kennzeichen": fahrzeug.getKennzeichen(),
                        "hersteller": fahrzeug.getHersteller(),
                        "modell": fahrzeug.getModell(),
                        "baujahr": fahrzeug.getBaujahr(),
                        "ladekapazitaetKG": fahrzeug.getLadekapazitaetKG()
                    }
                    return dataDict
        return "Kein Fahrzeug mit diesem Kennzeichen registriert."

    def addPKW(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, anzahlTueren: int):
        for fahrzeug in self.__fahrzeuge:
            if fahrzeug.getKennzeichen() == kennzeichen:
                print(f"Fahrzeug mit Kennzeichen {kennzeichen} ist bereits gepflegt.")
                return
        kennzeichen = PKW(kennzeichen, hersteller, modell, baujahr, anzahlTueren)
        print("Fahrzeug erstellt")
        self.__fahrzeuge.append(kennzeichen)


def main():
    TestFuhrpark = Fuhrpark([])
    TestFuhrpark.addPKW("SU_N_9513", "Seat", "Leon", 2002, 5)
    TestFuhrpark.addPKW("SU_SJ_513", "Fiat", "Fullback", 2017, 5)
    TestFuhrpark.addPKW("SU_N_9513", "Merc", "GLB", 2022, 5)
    print(TestFuhrpark.getFahrzeugDaten("SU_N_9513"))
    print(TestFuhrpark.getFahrzeugDaten("SU_NT_9513"))
    print(TestFuhrpark.getFahrzeugDaten("SU_SJ_513"))

main()