import os
import pickle
from datetime import datetime
# re-Import entfernt, da die strenge Regex-Prüfung entfällt

# Konstanter Dateiname für das Speichern
DATEINAME = "fuhrparkdaten.pkl"

# Erlaubte Hersteller Liste bleibt unverändert (hier aus Platzgründen ausgeklammert)
ERLAUBTE_HERSTELLER = [
    "ACURA", "ALFA ROMEO", "ASTON MARTIN", "AUDI", "BENTLEY", "BMW", "BUGATTI", 
    "BUICK", "BYD", "CADILLAC", "CHEVROLET", "CHRYSLER", "CITROEN", "DACIA", "DAF", 
    "DAIHATSU", "DODGE", "DS", "FAW", "FERRARI", "FIAT", "FORD", "FREIGHTLINER", 
    "GEELY", "GENESIS", "GMC", "GREAT WALL", "HONDA", "HUMMER", "HYUNDAI", 
    "INFINITI", "ISUZU", "IVECO", "JAC", "JAGUAR", "JEEP", "KAMAZ", "KENWORTH", 
    "KIA", "LAMBORGHINI", "LAND ROVER", "LI AUTO", "LEXUS", "LINCOLN", "LOTUS", 
    "MAN", "MASERATI", "MAZDA", "MCLAREN", "MERCEDES", "MG", "MINI", "MITSUBISHI", 
    "MITSUBISHI FUSO", "NIO", "NISSAN", "OPEL", "PEUGOT", "PETERBILT", "POLESTAR", 
    "PORSCHE", "QOROS", "RAM", "RENAULT", "RENAULT TRUCKS", "ROLLS-ROYCE", "SAAB", 
    "SCANIA", "SEAT", "SKODA", "SMART", "SUBARU", "SUZUKI", "TATA", "TESLA", 
    "TOYOTA", "VAUXHALL", "VOLVO", "VW", "XPENG", "ZEEKR"
]


class Fahrzeug:
    # ... (Klassen bleiben unverändert)
    def __init__(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int):
        self.__kennzeichen = kennzeichen
        self.__hersteller = hersteller
        self.__modell = modell
        self.__baujahr = baujahr

    def getKennzeichen(self) -> str:
        return self.__kennzeichen

    # ... (Getter bleiben unverändert)


class PKW(Fahrzeug):
    def __init__(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, anzahlTueren: int):
        super().__init__(kennzeichen, hersteller, modell, baujahr)
        self.__anzahlTueren = anzahlTueren
    # ...


class LKW(Fahrzeug):
    def __init__(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, ladekapazitaetKG: int):
        super().__init__(kennzeichen, hersteller, modell, baujahr)
        self.__ladekapazitaetKG = ladekapazitaetKG
    # ...


class Fuhrpark:
    def __init__(self, fahrzeuge: list):
        self.__fahrzeuge = fahrzeuge

    # ... (Methoden getFahrzeuge, addFahrzeug, removeFahrzeug, speichereFuhrpark, ladeFuhrpark bleiben unverändert)

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
        # Prüfung auf Duplikat
        for fahrzeug in self.__fahrzeuge:
            if fahrzeug.getKennzeichen() == kennzeichen:
                print(f"Fahrzeug mit Kennzeichen {kennzeichen} ist bereits gepflegt.")
                return
        
        # Prüfung auf Hersteller
        if hersteller.upper() not in ERLAUBTE_HERSTELLER:
             print(f"Hersteller '{hersteller}' ist nicht in der Liste der erlaubten Hersteller.")
             return

        if fahrzeugtyp == "PKW":
            self.__fahrzeuge.append(PKW(kennzeichen, hersteller, modell, baujahr, anzahlTueren))
            print("PKW erstellt")
        if fahrzeugtyp == "LKW":
            self.__fahrzeuge.append(LKW(kennzeichen, hersteller, modell, baujahr, ladekapazitaetKG))
            print("LKW erstellt")
        
        self.speichereFuhrpark()

    def removeFahrzeug(self, kennzeichen: str):
        original_laenge = len(self.__fahrzeuge)
        self.__fahrzeuge = [fahrzeug for fahrzeug in self.__fahrzeuge if fahrzeug.getKennzeichen().upper() != kennzeichen.upper()]
        
        if len(self.__fahrzeuge) < original_laenge:
            print(f"Fahrzeug mit Kennzeichen {kennzeichen} erfolgreich entfernt.")
            self.speichereFuhrpark()
        else:
            print(f"Fahrzeug mit Kennzeichen {kennzeichen} nicht gefunden.")

    def speichereFuhrpark(self, dateiname: str = DATEINAME):
        try:
            with open(dateiname, 'wb') as datei:
                pickle.dump(self.__fahrzeuge, datei)
        except Exception as e:
            print(f"Fehler beim Speichern der Daten: {e}")

    @staticmethod
    def ladeFuhrpark(dateiname: str = DATEINAME) -> list:
        if os.path.exists(dateiname):
            try:
                with open(dateiname, 'rb') as datei:
                    fahrzeuge_liste = pickle.load(datei)
                print(f"Daten erfolgreich aus '{dateiname}' geladen.")
                return fahrzeuge_liste
            except Exception as e:
                print(f"Fehler beim Laden der Daten: {e}")
                return []
        else:
            print(f"Speicherdatei '{dateiname}' nicht gefunden. Starte mit leerem Fuhrpark.")
            return []


def fmtString(String: str, laenge: int) -> str:
    # ... (unverändert)
    String = str(String)
    if len(String) > laenge - 1:
        counter = 0
        newString = ""
        for character in String:
            counter += 1
            if counter < 12:
                newString += character
            elif counter >= 12 and counter < 15:
                newString += "."
            else:
                String = newString
                break
    margin = int(laenge - round(len(String) , 0) - 1)
    fmt = str(" " + String + margin * " ")
    return fmt

def eingabeCheck(eingabe: str, typ):
    aktuelles_jahr = datetime.now().year 

    while True:
        try:
            checked = typ(input(eingabe))
            
            if typ == str and checked == "":
                print("Eingabe leer. Bitte erneut eingeben.")
                continue 
            
            # KENNZEICHEN PRÜFUNG (Gelockert)
            if typ == str and "kennzeichen" in eingabe.lower():
                # Wir stellen nur sicher, dass es Großbuchstaben sind und keine reine Leer-Eingabe
                checked = checked.upper().strip() 
                if checked == "":
                    print("Kennzeichen darf nicht leer sein.")
                    continue
                # ACHTUNG: Die strenge re.match Prüfung entfällt hier!
            
            # Baujahr-Prüfung
            if typ == int and "baujahr" in eingabe.lower() and checked > aktuelles_jahr:
                print(f"Ungültiges Baujahr. Das Jahr darf nicht über {aktuelles_jahr} liegen.")
                continue

            # Herstellerprüfung
            if typ == str and "hersteller" in eingabe.lower():
                if checked.upper() not in ERLAUBTE_HERSTELLER:
                    print(f"Hersteller '{checked}' ist nicht in der erlaubten Liste.")
                    print(f"Erlaubte Hersteller (Auszug): {', '.join(sorted(ERLAUBTE_HERSTELLER)[:10])}...")
                    continue
                checked = checked.upper() 

            break 
        except:
            print("Ungültige Eingabe. Bitte erneut eingeben.")
    return checked

def druckeFahrzeuge(Fuhrpark, fahrzeugListe: dict, fenstergroesse: tuple):
    # ... (unverändert)
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
    # ... (unverändert)
    fahrzeugListe = Fuhrpark.getFahrzeuge()
    fenstergroesse = os.get_terminal_size()
    druckeFahrzeuge(Fuhrpark, fahrzeugListe, fenstergroesse)
    while True:
        eingabe = input("\np - PKW hinzufügen\nl - LKW hinzufügen\nd - Details zu Fahrzeug anzeigen\ni - Details zu Fahrzeug nach Index anzeigen\nr - Fahrzeug entfernen\nq - Programm verlassen\n\nBitte Kommando angeben: ")
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
        elif eingabe == "r":
            eingabeKennzeichen = eingabeCheck("Bitte Kennzeichen des zu entfernenden Fahrzeugs angeben: ", str)
            Fuhrpark.removeFahrzeug(eingabeKennzeichen)
            input("\nDrücke Return um fortzufahren...")
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
    geladene_fahrzeuge = Fuhrpark.ladeFuhrpark()
    Fuhrpark1 = Fuhrpark(geladene_fahrzeuge)
    
    if not geladene_fahrzeuge:
        print("Füge Beispieldaten hinzu...")
        # Beispiel-Daten angepasst: Erlauben nun Sonderzeichen
        Fuhrpark1.addFahrzeug("PKW", "0-1", "MERCEDES", "S-Klasse", datetime.now().year, 5, 0) # Bsp. Kennzeichen des Bundespräsidenten
        Fuhrpark1.addFahrzeug("PKW", "SU-O-9513", "DACIA", "Logan", 2014, 5, 0) 
        Fuhrpark1.addFahrzeug("PKW", "F-JS-1", "PEUGOT", "206 CC", 2002, 3, 0) 
        Fuhrpark1.addFahrzeug("LKW", "GM-BN-2", "MERCEDES", "Actros", 2017, 0, 5500) 
        Fuhrpark1.addFahrzeug("LKW", "FR-234-RT", "SCANIA", "R-Serie", 2019, 0, 8000) # Bsp. Ausländisches Kennzeichen
    
    tui(Fuhrpark1)

if __name__ == "__main__":
    main()
