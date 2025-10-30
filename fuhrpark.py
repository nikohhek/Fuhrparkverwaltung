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
    def getFahrzeuge(self) -> dict:
        fahrzeugListe = {
            "PKW": {},
            "LKW": {}
        }
        for fahrzeug in self.__fahrzeuge:
            if type(fahrzeug).__name__ == "PKW":
                fahrzeugListe["PKW"][fahrzeug.getKennzeichen()] = {
                    "kennzeichen": fahrzeug.getKennzeichen(),
                    "hersteller": fahrzeug.getHersteller(),
                    "modell": fahrzeug.getModell(),
                    "baujahr": fahrzeug.getBaujahr(),
                    "anzahlTueren": fahrzeug.getAnzahlTueren()
                }
            if type(fahrzeug).__name__ == "LKW":
                fahrzeugListe["LKW"][fahrzeug.getKennzeichen()] = {
                    "kennzeichen": fahrzeug.getKennzeichen(),
                    "hersteller": fahrzeug.getHersteller(),
                    "modell": fahrzeug.getModell(),
                    "baujahr": fahrzeug.getBaujahr(),
                    "ladekapazitaetKG": fahrzeug.getLadekapazitaetKG()
                }
        return fahrzeugListe

    def addFahrzeug(self, fahrzeugtyp: str, kennzeichen: str, hersteller: str, modell: str, baujahr: int, anzahlTueren: int, ladekapazitaetKG: int):
        for fahrzeug in self.__fahrzeuge:
            if fahrzeug.getKennzeichen() == kennzeichen:
                print(f"Fahrzeug mit Kennzeichen {kennzeichen} ist bereits gepflegt.")
                return
        if fahrzeugtyp == "PKW":
            kennzeichen = PKW(kennzeichen, hersteller, modell, baujahr, anzahlTueren)
            self.__fahrzeuge.append(kennzeichen)
            print("PKW erstellt")
        if fahrzeugtyp == "LKW":
            kennzeichen = LKW(kennzeichen, hersteller, modell, baujahr, ladekapazitaetKG)
            self.__fahrzeuge.append(kennzeichen)
            print("LKW erstellt")

# Text User Interface
def tui(Fuhrpark):
    druckeFahrzeuge(Fuhrpark)

def druckeFahrzeuge(Fuhrpark):
    fahrzeugListe = Fuhrpark.getFahrzeuge()
    for kategorie in fahrzeugListe:
        print(len(fahrzeugListe[kategorie]))
        print(f"\n{20*"="}\n{kategorie}\n{20*"="}")
        for fahrzeug in fahrzeugListe[kategorie]:
            print(f"{fahrzeugListe[kategorie][fahrzeug]}")

def main():
    # Initiierung von Fuhrpark-Objekt zur Verwaltung
    Fuhrpark1 = Fuhrpark([])
    # manuelle Tests
    Fuhrpark1.addFahrzeug("PKW", "SU_N_9513", "Seat", "Leon", 2002, 5, 0)
    Fuhrpark1.addFahrzeug("LKW", "SU_SJ_513", "Fiat", "Fullback", 2017, 0, 500)
    Fuhrpark1.addFahrzeug("PKW", "SU_N_9513", "Merc", "GLB", 2022, 5, 0)
    tui(Fuhrpark1)

if __name__ == "__main__":
    main()