import os


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


def fmtString(String: str, laenge: int) -> str:
    String = str(String)
    margin = int(laenge - round(len(String) , 0) - 1)
    fmt = str(" " + String + margin * " ")
    return fmt

def eingabeCheck(eingabe: str, typ):
    while True:
        try:
            checked = typ(input(eingabe))
            if typ == str and checked == "":
                print("Eingabe leer. Bitte erneut eingeben.")
            else:
                break
        except:
            print("Ungültige Eingabe. Bitte erneut eingeben.")
    return checked

def druckeFahrzeuge(Fuhrpark, fahrzeugListe: dict, fenstergroesse: tuple):
    index = 0
    headline = "Fahrzeuge"
    headlineMargin = int(round(fenstergroesse.columns / 2, 0)) - int(round(len(headline) / 2, 0))
    print(f"\n{fenstergroesse.columns * "="}\n{headlineMargin * " "}Fahrzeuge\n{fenstergroesse.columns * "="}")
    # Bezeichnungen Tabelle
    print(f"{fmtString("INDEX", 8)}|{fmtString("TYP", 16)}|{fmtString("KENNZEICHEN", 16)}|{fmtString("HERSTELLER", 16)}|{fmtString("MODELL", 16)}\n{fenstergroesse.columns * "-"}")
    for kategorie in fahrzeugListe:
        for fahrzeug in fahrzeugListe[kategorie]:
            index += 1
            print(f"{fmtString(index, 8)}|{fmtString(kategorie, 16)}|{fmtString(fahrzeugListe[kategorie][fahrzeug]["kennzeichen"], 16)}|{fmtString(fahrzeugListe[kategorie][fahrzeug]["hersteller"], 16)}|{fmtString(fahrzeugListe[kategorie][fahrzeug]["modell"], 16)}")

# Text User Interface
def tui(Fuhrpark):
    fahrzeugListe = Fuhrpark.getFahrzeuge()
    fenstergroesse = os.get_terminal_size()
    druckeFahrzeuge(Fuhrpark, fahrzeugListe, fenstergroesse)
    while True:
        eingabe = input("\np - PKW hinzufügen\nl - LKW hinzufügen\nd - Details zu Fahrzeug anzeigen\ni - Details zu Fahrzeug nach Index anzeigen\nq - Programm verlassen\n\nBitte Kommando angeben: ")
        if eingabe == "p":
            eingabeKennzeichen = eingabeCheck("Bitte Kennzeichen angeben: ", str)
            eingabeHersteller = eingabeCheck("Bitte Hersteller angeben: ", str)
            eingabeModell = eingabeCheck("Bitte Modell angeben: ", str)
            eingabeBaujahr = eingabeCheck("Bitte das Baujahr angeben: ", int)
            eingabeAnzahlTueren = eingabeCheck("Bitte Anzahl der Türen angeben: ", int)
            Fuhrpark.addFahrzeug("PKW", eingabeKennzeichen, eingabeHersteller, eingabeModell, eingabeBaujahr, eingabeAnzahlTueren, 0)
            break
        elif eingabe == "l":
            eingabeKennzeichen = eingabeCheck("Bitte Kennzeichen angeben: ", str)
            eingabeHersteller = eingabeCheck("Bitte Hersteller angeben: ", str)
            eingabeModell = eingabeCheck("Bitte Modell angeben: ", str)
            eingabeBaujahr = eingabeCheck("Bitte das Baujahr angeben: ", int)
            eingabeLadekapazitaetKG = eingabeCheck("Bitte Ladekapazität in Kilogramm angeben: ", int)
            Fuhrpark.addFahrzeug("LKW", eingabeKennzeichen, eingabeHersteller, eingabeModell, eingabeBaujahr, 0, eingabeLadekapazitaetKG)
            break
        elif eingabe == "q":
            return
        elif eingabe == "d":
            suche = eingabeCheck("Kennzeichen auswählen: ", str)
            try:
                print(f"\nTyp: PKW\nKennzeichen: {fahrzeugListe["PKW"][suche]["kennzeichen"]}\nHersteller: {fahrzeugListe["PKW"][suche]["hersteller"]}\nModell: {fahrzeugListe["PKW"][suche]["modell"]}\nBaujahr: {fahrzeugListe["PKW"][suche]["baujahr"]}\nAnzahl der Tühren: {fahrzeugListe["PKW"][suche]["anzahlTueren"]}")
            except:
                try:
                    print(f"\nTyp: LKW\nKennzeichen: {fahrzeugListe["LKW"][suche]["kennzeichen"]}\nHersteller: {fahrzeugListe["LKW"][suche]["hersteller"]}\nModell: {fahrzeugListe["LKW"][suche]["modell"]}\nBaujahr: {fahrzeugListe["LKW"][suche]["baujahr"]}\nLadekapazität: {fahrzeugListe["LKW"][suche]["ladekapazitaetKG"]} kg")
                except:
                    print("Kennzeichen nicht gefunden. Bitte Eingabe prüfen.")
            input("\nDrücke Return um fortzufahren...")
            break
        elif eingabe == "i":
            index = 0
            suche = ""
            suchNr = eingabeCheck("Index angeben: ", int)
            for kategorie in fahrzeugListe:
                for fahrzeug in fahrzeugListe[kategorie]:
                    index += 1
                    if index == suchNr:
                        suche = fahrzeugListe[kategorie][fahrzeug]["kennzeichen"]
            if suche == "":
                print("Index nicht gefunden.")
                input("\nDrücke Return um fortzufahren...")
                break
            else:
                try:
                    print(f"\nTyp: PKW\nKennzeichen: {fahrzeugListe["PKW"][suche]["kennzeichen"]}\nHersteller: {fahrzeugListe["PKW"][suche]["hersteller"]}\nModell: {fahrzeugListe["PKW"][suche]["modell"]}\nBaujahr: {fahrzeugListe["PKW"][suche]["baujahr"]}\nAnzahl der Tühren: {fahrzeugListe["PKW"][suche]["anzahlTueren"]}")
                except:
                    try:
                        print(f"\nTyp: LKW\nKennzeichen: {fahrzeugListe["LKW"][suche]["kennzeichen"]}\nHersteller: {fahrzeugListe["LKW"][suche]["hersteller"]}\nModell: {fahrzeugListe["LKW"][suche]["modell"]}\nBaujahr: {fahrzeugListe["LKW"][suche]["baujahr"]}\nLadekapazität: {fahrzeugListe["LKW"][suche]["ladekapazitaetKG"]} kg")
                    except:
                        print("Kennzeichen nicht gefunden. Bitte Eingabe prüfen.")
                input("\nDrücke Return um fortzufahren...")
                break
        else:
            print("Ungültige Eingabe. Bitte erneut eingeben.\n")
    tui(Fuhrpark)

def main():
    # Initiierung von Fuhrpark-Objekt zur Verwaltung
    Fuhrpark1 = Fuhrpark([])
    # Füge Samples hinzu
    Fuhrpark1.addFahrzeug("PKW", "SU_N_9513", "Seat", "Leon", 2002, 5, 0)
    Fuhrpark1.addFahrzeug("PKW", "SU_O_9513", "Dacia", "Logan", 2014, 5, 0)
    Fuhrpark1.addFahrzeug("PKW", "SU_JS_1", "Peugot", "206 CC", 2002, 3, 0)
    Fuhrpark1.addFahrzeug("LKW", "SU_SJ_513", "Fiat", "Fullback", 2017, 0, 500)
    Fuhrpark1.addFahrzeug("LKW", "GM_BN_2", "Mercedes", "Actros", 2017, 0, 5500)
    Fuhrpark1.addFahrzeug("LKW", "SU_SJ_513", "Fiat", "Fullback", 2017, 0, 500)
    Fuhrpark1.addFahrzeug("PKW", "SU_N_9513", "Mercedes", "GLB", 2022, 5, 0)
    tui(Fuhrpark1)

if __name__ == "__main__":
    main()