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

    # Gibt Kennzeichen aller Fahrzeuge in Liste aus
    def getFahrzeuge(self) -> list:
        fahrzeugListe = []
        for fahrzeug in self.__fahrzeuge:
            fahrzeugListe.append(fahrzeug.getKennzeichen())
        return fahrzeugListe

    # Gibt Fahrzeugdaten eines Fahrzeugs als Dictionary aus
    def getFahrzeugDaten(self, kennzeichen: str) -> dict:
        for fahrzeug in self.__fahrzeuge:
            # Vergleicht Kennzeichen des momentanen Fahrzeugs mit gesuchtem Kennzeichen
            if fahrzeug.getKennzeichen() == kennzeichen:
                # Ausgabe für PKWs
                if type(fahrzeug).__name__ == "PKW":
                    dataDict = {
                        "typ": "PKW",
                        "kennzeichen": fahrzeug.getKennzeichen(),
                        "hersteller": fahrzeug.getHersteller(),
                        "modell": fahrzeug.getModell(),
                        "baujahr": fahrzeug.getBaujahr(),
                        "anzahlTueren": fahrzeug.getAnzahlTueren()
                    }
                    return dataDict
                # Ausgabe für LKWs
                if type(fahrzeug).__name__ == "LKW":
                    dataDict = {
                        "typ": "LKW",
                        "kennzeichen": fahrzeug.getKennzeichen(),
                        "hersteller": fahrzeug.getHersteller(),
                        "modell": fahrzeug.getModell(),
                        "baujahr": fahrzeug.getBaujahr(),
                        "ladekapazitaetKG": fahrzeug.getLadekapazitaetKG()
                    }
                    return dataDict
        # Wird nur ausgeführt, wenn Kennzeichen nicht gefunden wurde
        return "Kein Fahrzeug mit diesem Kennzeichen registriert."

    def addPKW(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, anzahlTueren: int):
        for fahrzeug in self.__fahrzeuge:
            if fahrzeug.getKennzeichen() == kennzeichen:
                print(f"Fahrzeug mit Kennzeichen {kennzeichen} ist bereits gepflegt.")
                return
        kennzeichen = PKW(kennzeichen, hersteller, modell, baujahr, anzahlTueren)
        print("Fahrzeug erstellt")
        self.__fahrzeuge.append(kennzeichen)

    def addLKW(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, ladekapazitaetKG: int):
        for fahrzeug in self.__fahrzeuge:
            if fahrzeug.getKennzeichen() == kennzeichen:
                print(f"Fahrzeug mit Kennzeichen {kennzeichen} ist bereits gepflegt.")
                return
        kennzeichen = LKW(kennzeichen, hersteller, modell, baujahr, ladekapazitaetKG)
        print("Fahrzeug erstellt")
        self.__fahrzeuge.append(kennzeichen)


def main():
    # Initiierung von Fuhrpark-Objekt zur Verwaltung
    TestFuhrpark = Fuhrpark([])

    # manuelle Tests
    TestFuhrpark.addPKW("SU_N_9513", "Seat", "Leon", 2002, 5)
    TestFuhrpark.addLKW("SU_SJ_513", "Fiat", "Fullback", 2017, 5)
    TestFuhrpark.addPKW("SU_N_9513", "Merc", "GLB", 2022, 5)
    print(TestFuhrpark.getFahrzeugDaten("SU_N_9513"))
    print(TestFuhrpark.getFahrzeugDaten("SU_NT_9513"))
    print(TestFuhrpark.getFahrzeugDaten("SU_SJ_513"))
    print(TestFuhrpark.getFahrzeuge())

main()