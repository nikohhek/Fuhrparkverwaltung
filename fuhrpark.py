import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox 
import pickle
from datetime import datetime

# --- VERBESSERTE, DYNAMISCHE TKINTER PFAD-SETZUNG (Geräteübergreifend) ---
# Dieser Block hilft, Tkinter unter Windows/Linux zu starten, wenn die Umgebungsvariablen fehlen.
if sys.platform.startswith('win') or sys.platform.startswith('linux'):
    try:
        # 1. Basis-Installationspfad der Python-Umgebung nutzen
        base_dir = os.environ.get('VIRTUAL_ENV') or sys.prefix

        tcl_found = False
        
        # Windows-Pfade (z.B. Python313/tcl)
        tcl_win_path = os.path.join(base_dir, 'tcl')
        
        # Windows-Suche
        if os.path.exists(tcl_win_path):
            os.environ['TCL_LIBRARY'] = tcl_win_path
            os.environ['TK_LIBRARY'] = os.path.join(tcl_win_path, 'tk8.6') 
            
            # Füge den DLLs-Pfad zur PATH-Variable hinzu (wichtig für Windows)
            dll_path = os.path.join(base_dir, 'DLLs')
            if os.path.exists(dll_path):
                os.environ['PATH'] += os.pathsep + dll_path
                
            tcl_found = True
        
        # Linux/macOS-Suche (sucht in 'lib' nach tcl-Ordnern)
        elif sys.platform.startswith('linux'):
            tcl_lib_path = os.path.join(base_dir, 'lib')
            if os.path.exists(tcl_lib_path):
                 for item in os.listdir(tcl_lib_path):
                     if item.startswith('tcl'):
                         os.environ['TCL_LIBRARY'] = os.path.join(tcl_lib_path, item)
                         tcl_found = True
                         break
        
        if tcl_found:
             print(f"INFO: TCL/TK Pfad dynamisch gesetzt: {os.environ.get('TCL_LIBRARY')}")
        else:
             print("WARNUNG: TCL/TK Pfad konnte nicht dynamisch gefunden werden. Standardmethode wird versucht.")

    except Exception as e:
        print(f"WARNUNG: Fehler bei der dynamischen Pfadsuche: {e}")
# -------------------------------------------------------------------------


# Konstanter Dateiname für das Speichern
DATEINAME = "fuhrparkdaten.pkl"

# Erlaubte Hersteller Liste
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


# --- KLASSEN FÜR DATENSTRUKTUR ---

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

# --- KLASSE FUHRPARK (Inkl. Autosave) ---

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

# --- VALIDIERUNGSFUNKTION (Für die GUI) ---

def eingabeCheck_GUI(eingabe_wert: str, feld_typ: str) -> tuple[bool, str]:
    """Prüft die Eingabe für die GUI-Formulare."""
    aktuelles_jahr = datetime.now().year 
    eingabe_wert = str(eingabe_wert) # Sicherstellen, dass es ein String ist

    if feld_typ == "baujahr":
        try:
            jahr = int(eingabe_wert)
            if jahr > aktuelles_jahr or jahr < 1900:
                return False, f"Baujahr muss zwischen 1900 und {aktuelles_jahr} liegen."
            return True, jahr
        except ValueError:
            return False, "Baujahr muss eine ganze Zahl sein."

    elif feld_typ == "kennzeichen":
        checked = eingabe_wert.upper().strip() 
        if checked == "":
            return False, "Kennzeichen darf nicht leer sein."
        return True, checked # Gibt den bereinigten (upper) Wert zurück

    elif feld_typ == "hersteller":
        checked = eingabe_wert.upper().strip()
        if checked == "":
             return False, "Hersteller darf nicht leer sein."
        if checked not in ERLAUBTE_HERSTELLER:
            return False, f"Hersteller '{eingabe_wert}' ist nicht erlaubt."
        return True, checked # Gibt den bereinigten (upper) Wert zurück
        
    elif feld_typ == "modell":
        checked = eingabe_wert.strip()
        if checked == "":
             return False, "Modell darf nicht leer sein."
        return True, checked

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

        # Stil 
        style = ttk.Style()
        style.theme_use('clam') 
        style.configure("TFrame", background="#f0f0f0")

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
        
        ttk.Label(self.control_frame, text="Fahrzeug Entfernen nach Kennzeichen", font=("Arial", 10, "bold")).pack(pady=5)
        self.remove_kennzeichen_var = tk.StringVar()
        ttk.Entry(self.control_frame, textvariable=self.remove_kennzeichen_var).pack(fill='x', pady=2)
        ttk.Button(self.control_frame, text="Fahrzeug ENTFERNEN", command=self.remove_fahrzeug).pack(fill='x', pady=5)


    def update_list(self):
        # Löscht alle alten Einträge
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fügt neue Einträge hinzu
        data = self.fuhrpark.getFahrzeuge()
        index = 1
        
        for typ, fahrzeuge in data.items():
            # Sortiere nach Kennzeichen, damit die Reihenfolge nach dem Laden konsistent ist
            for kzn in sorted(fahrzeuge.keys()):
                fz_data = fahrzeuge[kzn]
                details_text = f"Türen: {fz_data['anzahlTueren']}" if typ == "PKW" else f"Kapazität: {fz_data['ladekapazitaetKG']} kg"
                
                self.tree.insert("", "end", iid=kzn, 
                                 values=(index, typ, kzn, fz_data['hersteller'], fz_data['modell'], fz_data['baujahr'], details_text))
                index += 1
                
    def add_fahrzeug(self):
        # 1. Daten aus den Eingabefeldern sammeln
        typ = self.vars["typ"].get()
        kennzeichen = self.vars["kennzeichen"].get()
        hersteller = self.vars["hersteller"].get()
        modell = self.vars["modell"].get()
        baujahr = self.vars["baujahr"].get()
        anzahlTueren = self.vars["anzahlTueren"].get()
        ladekapazitaetKG = self.vars["ladekapazitaetKG"].get()
        
        # 2. Validierung
        validation_fields = [
            ("kennzeichen", kennzeichen),
            ("hersteller", hersteller),
            ("modell", modell),
            ("baujahr", baujahr),
        ]
        
        if typ == "PKW":
            validation_fields.append(("anzahlTueren", anzahlTueren))
        else: # LKW
            validation_fields.append(("ladekapazitaetKG", ladekapazitaetKG))

        validated_data = {}
        for field_name, value in validation_fields:
            is_valid, checked_value = eingabeCheck_GUI(value, field_name)
            if not is_valid:
                messagebox.showerror("Eingabefehler", f"Fehler bei {field_name}: {checked_value}")
                return
            validated_data[field_name] = checked_value
            
        # 3. Fahrzeug hinzufügen und Ergebnis prüfen (Autosave passiert in addFahrzeug)
        result = self.fuhrpark.addFahrzeug(
            typ,
            validated_data["kennzeichen"],
            validated_data["hersteller"],
            validated_data["modell"],
            validated_data["baujahr"],
            validated_data.get("anzahlTueren", 0),
            validated_data.get("ladekapazitaetKG", 0)
        )

        if "erstellt" in result:
            messagebox.showinfo("Erfolg", result)
            self.update_list()
            # Eingabefelder leeren
            for key in self.vars:
                if key != "typ":
                    self.vars[key].set("")
        else:
            messagebox.showerror("Fehler", result)
            
    def remove_fahrzeug(self):
        kennzeichen_to_remove = self.remove_kennzeichen_var.get().upper().strip()
        
        if not kennzeichen_to_remove:
            messagebox.showwarning("Achtung", "Bitte Kennzeichen zum Entfernen eingeben.")
            return

        # Frage zur Sicherheit nach
        if not messagebox.askyesno("Bestätigung", f"Soll das Fahrzeug mit Kennzeichen '{kennzeichen_to_remove}' wirklich entfernt werden?"):
            return 
            
        result = self.fuhrpark.removeFahrzeug(kennzeichen_to_remove) # Autosave passiert hier

        if "erfolgreich entfernt" in result:
            messagebox.showinfo("Erfolg", result)
            self.update_list()
            self.remove_kennzeichen_var.set("")
        else:
            messagebox.showerror("Fehler", result)

    def show_details(self, event):
        """Zeigt Details zum doppelt geklickten Fahrzeug."""
        selected_item = self.tree.focus()
        if not selected_item:
            return

        kennzeichen = self.tree.item(selected_item, 'iid')
        
        # Durchsuche den Fuhrpark nach dem Kennzeichen und dem Typ
        data = self.fuhrpark.getFahrzeuge()
        fahrzeug_info = None
        typ = None
        for t, fahrzeuge in data.items():
            if kennzeichen in fahrzeuge:
                fahrzeug_info = fahrzeuge[kennzeichen]
                typ = t
                break

        if fahrzeug_info:
            detail_str = f"Typ: {typ}\n"
            detail_str += f"Kennzeichen: {fahrzeug_info.get('kennzeichen', 'N/A')}\n"
            detail_str += f"Hersteller: {fahrzeug_info.get('hersteller', 'N/A')}\n"
            detail_str += f"Modell: {fahrzeug_info.get('modell', 'N/A')}\n"
            detail_str += f"Baujahr: {fahrzeug_info.get('baujahr', 'N/A')}\n"
            
            if typ == "PKW":
                detail_str += f"Anzahl Türen: {fahrzeug_info.get('anzahlTueren', 'N/A')}"
            else:
                detail_str += f"Ladekapazität: {fahrzeug_info.get('ladekapazitaetKG', 'N/A')} kg"
            
            messagebox.showinfo(f"Details: {kennzeichen}", detail_str)

    def sort_column(self, tree, col, reverse):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        
        # Versuche, Zahlen zu sortieren
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            # Wenn keine Zahl, als Text sortieren
            l.sort(reverse=reverse)

        # Neu anordnen
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        # Neuen Sortierpfeil setzen
        tree.heading(col, command=lambda: self.sort_column(tree, col, not reverse))


def main():
    # 1. Daten laden
    geladene_fahrzeuge = Fuhrpark.ladeFuhrpark()
    Fuhrpark1 = Fuhrpark(geladene_fahrzeuge)
    
    # 2. Beispieldaten hinzufügen, falls leer (Autosave passiert hier automatisch)
    if not geladene_fahrzeuge:
        print("Füge Beispieldaten hinzu...")
        Fuhrpark1.addFahrzeug("PKW", "0-1", "MERCEDES", "S-Klasse", datetime.now().year, 5, 0)
        Fuhrpark1.addFahrzeug("PKW", "SU-O-9513", "DACIA", "Logan", 2014, 5, 0)
        Fuhrpark1.addFahrzeug("LKW", "GM-BN-2", "MERCEDES", "Actros", 2017, 0, 5500)
    
    # 3. GUI starten
    root = tk.Tk()
    app = FuhrparkGUI(root, Fuhrpark1)
    root.mainloop()

if __name__ == "__main__":
    main()
