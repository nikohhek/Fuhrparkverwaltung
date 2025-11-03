import os
import pickle
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox # Für moderne Widgets und Dialoge

# Konstanter Dateiname für das Speichern
DATEINAME = "fuhrparkdaten.pkl"

# Erlaubte Hersteller Liste bleibt unverändert (hier verkürzt zur Übersicht)
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


# --- KLASSEN FÜR DATENSTRUKTUR (Unverändert) ---

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

    def getAnzahlTueren(self) -> int:
        return self.__anzahlTueren

class LKW(Fahrzeug):
    def __init__(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, ladekapazitaetKG: int):
        super().__init__(kennzeichen, hersteller, modell, baujahr)
        self.__ladekapazitaetKG = ladekapazitaetKG

    def getLadekapazitaetKG(self) -> int:
        return self.__ladekapazitaetKG

# --- KLASSE FUHRPARK (Unverändert, inkl. Autosave) ---

class Fuhrpark:
    def __init__(self, fahrzeuge: list):
        self.__fahrzeuge = fahrzeuge

    def getFahrzeuge(self) -> dict:
        fahrzeugListe = {"PKW": {}, "LKW": {}}
        for fahrzeug in self.__fahrzeuge:
            kennzeichen = fahrzeug.getKennzeichen()
            base_data = {
                "kennzeichen": kennzeichen,
                "hersteller": fahrzeug.getHersteller(),
                "modell": fahrzeug.getModell(),
                "baujahr": fahrzeug.getBaujahr(),
            }
            if type(fahrzeug).__name__ == "PKW":
                fahrzeugListe["PKW"][kennzeichen] = {**base_data, "anzahlTueren": fahrzeug.getAnzahlTueren()}
            if type(fahrzeug).__name__ == "LKW":
                fahrzeugListe["LKW"][kennzeichen] = {**base_data, "ladekapazitaetKG": fahrzeug.getLadekapazitaetKG()}
        return fahrzeugListe

    def addFahrzeug(self, fahrzeugtyp: str, kennzeichen: str, hersteller: str, modell: str, baujahr: int, anzahlTueren: int, ladekapazitaetKG: int):
        for fahrzeug in self.__fahrzeuge:
            if fahrzeug.getKennzeichen() == kennzeichen:
                return f"Fahrzeug mit Kennzeichen {kennzeichen} ist bereits gepflegt."
        
        if hersteller.upper() not in ERLAUBTE_HERSTELLER:
             return f"Hersteller '{hersteller}' ist nicht in der Liste der erlaubten Hersteller."

        if fahrzeugtyp == "PKW":
            self.__fahrzeuge.append(PKW(kennzeichen, hersteller, modell, baujahr, anzahlTueren))
            result = "PKW erstellt"
        elif fahrzeugtyp == "LKW":
            self.__fahrzeuge.append(LKW(kennzeichen, hersteller, modell, baujahr, ladekapazitaetKG))
            result = "LKW erstellt"
        else:
            return "Ungültiger Fahrzeugtyp."
        
        self.speichereFuhrpark()
        return result

    def removeFahrzeug(self, kennzeichen: str):
        original_laenge = len(self.__fahrzeuge)
        self.__fahrzeuge = [fahrzeug for fahrzeug in self.__fahrzeuge if fahrzeug.getKennzeichen().upper() != kennzeichen.upper()]
        
        if len(self.__fahrzeuge) < original_laenge:
            self.speichereFuhrpark()
            return f"Fahrzeug mit Kennzeichen {kennzeichen} erfolgreich entfernt."
        else:
            return f"Fahrzeug mit Kennzeichen {kennzeichen} nicht gefunden."

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

# --- VALIDIERUNGSFUNKTION (Für die GUI angepasst) ---

def eingabeCheck_GUI(eingabe_wert: str, feld_typ: str) -> tuple[bool, str]:
    """Prüft die Eingabe für die GUI-Formulare."""
    aktuelles_jahr = datetime.now().year 

    if feld_typ == "baujahr":
        try:
            jahr = int(eingabe_wert)
            if jahr > aktuelles_jahr:
                return False, f"Baujahr darf nicht über {aktuelles_jahr} liegen."
            return True, ""
        except ValueError:
            return False, "Baujahr muss eine ganze Zahl sein."

    elif feld_typ == "kennzeichen":
        checked = eingabe_wert.upper().strip() 
        if checked == "":
            return False, "Kennzeichen darf nicht leer sein."
        return True, checked # Gibt den bereinigten (upper) Wert zurück

    elif feld_typ == "hersteller":
        checked = eingabe_wert.upper().strip()
        if checked not in ERLAUBTE_HERSTELLER:
            return False, f"Hersteller '{eingabe_wert}' ist nicht erlaubt."
        return True, checked # Gibt den bereinigten (upper) Wert zurück

    elif feld_typ in ("anzahlTueren", "ladekapazitaetKG"):
        try:
            wert = int(eingabe_wert)
            if wert < 0:
                 return False, "Wert muss positiv sein."
            return True, wert
        except ValueError:
            return False, "Eingabe muss eine ganze Zahl sein."
            
    return True, eingabe_wert

# --- TKINTER GUI KLASSE ---

class FuhrparkGUI:
    def __init__(self, master, fuhrpark):
        self.master = master
        master.title("Fuhrpark-Management")
        self.fuhrpark = fuhrpark

        # Stil (Optional, macht die GUI hübscher)
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", padding=6, relief="flat", background="#ccc")

        # --- Frames ---
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(fill='both', expand=True)

        self.list_frame = ttk.Frame(self.main_frame)
        self.list_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.control_frame = ttk.Frame(self.main_frame, padding="10", relief="groove")
        self.control_frame.pack(side="right", fill="y", padx=5, pady=5)

        # --- Liste / Treeview ---
        self.setup_list_view()
        self.update_list()
        
        # --- Steuerung/Formular ---
        self.setup_control_panel()

    def setup_list_view(self):
        # Treeview (Tabelle) erstellen
        columns = ("Index", "Typ", "Kennzeichen", "Hersteller", "Modell", "Baujahr", "Details")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(self.tree, c, False))
            self.tree.column(col, anchor="w", width=80 if col in ("Typ", "Baujahr") else 100)
            
        self.tree.pack(side="top", fill="both", expand=True)

        # Scrollbar hinzufügen
        vsb = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Event für Doppelklick zur Detailanzeige
        self.tree.bind('<Double-1>', self.show_details)


    def setup_control_panel(self):
        ttk.Label(self.control_frame, text="Fahrzeug hinzufügen/entfernen", font=("Arial", 12, "bold")).pack(pady=10)

        # Variablen für die Eingabefelder
        self.vars = {
            "typ": tk.StringVar(value="PKW"),
            "kennzeichen": tk.StringVar(),
            "hersteller": tk.StringVar(),
            "modell": tk.StringVar(),
            "baujahr": tk.StringVar(),
            "anzahlTueren": tk.StringVar(),
            "ladekapazitaetKG": tk.StringVar()
        }

        # Eingabefelder erstellen
        fields = [
            ("Typ:", ttk.Combobox, "typ", ["PKW", "LKW"]),
            ("Kennzeichen:", ttk.Entry, "kennzeichen"),
            ("Hersteller:", ttk.Entry, "hersteller"),
            ("Modell:", ttk.Entry, "modell"),
            ("Baujahr:", ttk.Entry, "baujahr"),
            ("Anzahl Türen (PKW):", ttk.Entry, "anzahlTueren"),
            ("Ladekapazität (LKW):", ttk.Entry, "ladekapazitaetKG")
        ]

        for label_text, widget_type, var_name, *options in fields:
            row = ttk.Frame(self.control_frame)
            row.pack(fill='x', pady=2)
            ttk.Label(row, text=label_text, width=15, anchor='w').pack(side='left')
            
            if widget_type == ttk.Combobox:
                widget = widget_type(row, textvariable=self.vars[var_name], values=options[0], state="readonly")
            else:
                widget = widget_type(row, textvariable=self.vars[var_name])
            widget.pack(side='right', expand=True, fill='x')
        
        # Schaltflächen
        ttk.Button(self.control_frame, text="Fahrzeug HINZUFÜGEN", command=self.add_fahrzeug).pack(fill='x', pady=10)
        
        ttk.Separator(self.control_frame).pack(fill='x', pady=10)
