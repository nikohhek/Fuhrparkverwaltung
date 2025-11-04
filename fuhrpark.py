import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import pickle
from datetime import datetime

# --- VERBESSERTE, DYNAMISCHE TKINTER PFAD-SETZUNG (Geräteübergreifend) ---
if sys.platform.startswith('win') or sys.platform.startswith('linux'):
    try:
        base_dir = os.environ.get('VIRTUAL_ENV') or sys.prefix
        tcl_found = False
        tcl_win_path = os.path.join(base_dir, 'tcl')

        if os.path.exists(tcl_win_path):
            os.environ['TCL_LIBRARY'] = tcl_win_path
            os.environ['TK_LIBRARY'] = os.path.join(tcl_win_path, 'tk8.6')
            dll_path = os.path.join(base_dir, 'DLLs')
            if os.path.exists(dll_path):
                os.environ['PATH'] += os.pathsep + dll_path
            tcl_found = True

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

# --- NEUE KONSTANTEN FÜR PARKPLÄTZE UND KRAFTSTOFFARTEN ---
E_PARKPLÄTZE_ANZ = 10
P_PARKPLÄTZE_ANZ = 20
GESAMT_PARKPLÄTZE = E_PARKPLÄTZE_ANZ + P_PARKPLÄTZE_ANZ

# Liste der möglichen Parkplatznummern (E1-E10 und P1-P20)
ALLE_PARKPLÄTZE = [f"E{i}" for i in range(1, E_PARKPLÄTZE_ANZ + 1)] + \
                  [f"P{i}" for i in range(1, P_PARKPLÄTZE_ANZ + 1)]

ERLAUBTE_KRAFTSTOFFE = ["Verbrenner", "Hybrid", "Elektro"]

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


# --- KLASSEN FÜR DATENSTRUKTUR (mit Kraftstoffart und Parkplatz) ---

class Fahrzeug:
    # NEU: parkplatznummer hinzugefügt
    def __init__(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, kraftstoffart: str,
                 parkplatznummer: str = "Unassigned"):
        self.__kennzeichen = kennzeichen
        self.__hersteller = hersteller
        self.__modell = modell
        self.__baujahr = baujahr
        self.__kraftstoffart = kraftstoffart
        self.__parkplatznummer = parkplatznummer  # NEU: Parkplatznummer

    def getKennzeichen(self) -> str:
        return self.__kennzeichen

    def getHersteller(self) -> str:
        return self.__hersteller

    def getModell(self) -> str:
        return self.__modell

    def getBaujahr(self) -> int:
        return self.__baujahr

    def getKraftstoffart(self) -> str:
        return self.__kraftstoffart

    def getParkplatznummer(self) -> str:
        return self.__parkplatznummer

    def setParkplatznummer(self, nummer: str):
        self.__parkplatznummer = nummer


class PKW(Fahrzeug):
    # NEU: parkplatznummer hinzugefügt und an super() übergeben
    def __init__(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, kraftstoffart: str,
                 anzahlTueren: int, parkplatznummer: str = "Unassigned"):
        super().__init__(kennzeichen, hersteller, modell, baujahr, kraftstoffart, parkplatznummer)
        self.__anzahlTueren = anzahlTueren

    def getAnzahlTueren(self) -> int:
        return self.__anzahlTueren


class LKW(Fahrzeug):
    # NEU: parkplatznummer hinzugefügt und an super() übergeben
    def __init__(self, kennzeichen: str, hersteller: str, modell: str, baujahr: int, kraftstoffart: str,
                 ladekapazitaetKG: int, parkplatznummer: str = "Unassigned"):
        super().__init__(kennzeichen, hersteller, modell, baujahr, kraftstoffart, parkplatznummer)
        self.__ladekapazitaetKG = ladekapazitaetKG

    def getLadekapazitaetKG(self) -> int:
        return self.__ladekapazitaetKG


# --- KLASSE FUHRPARK (Inkl. Parkplatzlogik & Autosave) ---

class Fuhrpark:
    def __init__(self, fahrzeuge: list):
        self.__fahrzeuge = fahrzeuge
        # Aktualisiert Parkplatznummern beim Laden, falls ein Fahrzeug durch Löschen seinen Platz verlor
        self.__aktualisiere_parkplaetze(self.__fahrzeuge)

    def __aktualisiere_parkplaetze(self, fahrzeuge: list):
        """Stellt sicher, dass die Parkplatznummern nach dem Laden konsistent sind und zugewiesen werden."""

        # 1. Definiere verfügbare Plätze
        verfuegbare_e = sorted([p for p in ALLE_PARKPLÄTZE if p.startswith('E')], key=lambda p: int(p[1:]))
        verfuegbare_p = sorted([p for p in ALLE_PARKPLÄTZE if p.startswith('P')], key=lambda p: int(p[1:]))
        belegte_parkplaetze = set()

        # Sortiere Fahrzeuge (z.B. nach Kennzeichen), um die Vergabe reproduzierbar zu machen
        sortierte_fahrzeuge = sorted(fahrzeuge, key=lambda f: f.getKennzeichen())

        # 2. Versuch, alte, korrekte Plätze zu re-reservieren
        for fahrzeug in sortierte_fahrzeuge:
            aktuelle_nummer = fahrzeug.getParkplatznummer()
            ist_e_fahrzeug = fahrzeug.getKraftstoffart() in ["Hybrid", "Elektro"]

            if ist_e_fahrzeug and aktuelle_nummer.startswith(
                    'E') and aktuelle_nummer in verfuegbare_e and aktuelle_nummer not in belegte_parkplaetze:
                belegte_parkplaetze.add(aktuelle_nummer)
                verfuegbare_e.remove(aktuelle_nummer)
            elif not ist_e_fahrzeug and aktuelle_nummer.startswith(
                    'P') and aktuelle_nummer in verfuegbare_p and aktuelle_nummer not in belegte_parkplaetze:
                belegte_parkplaetze.add(aktuelle_nummer)
                verfuegbare_p.remove(aktuelle_nummer)

        # 3. Zuweisen neuer Plätze (für migrierte oder neu geladene)
        for fahrzeug in sortierte_fahrzeuge:
            aktuelle_nummer = fahrzeug.getParkplatznummer()
            ist_e_fahrzeug = fahrzeug.getKraftstoffart() in ["Hybrid", "Elektro"]

            # Neu zuweisen, wenn der Platz "Unassigned" ist, falsch zugewiesen ist oder durch Re-Reservierung nicht erfasst wurde
            if aktuelle_nummer not in belegte_parkplaetze:
                if ist_e_fahrzeug and verfuegbare_e:
                    neue_nummer = verfuegbare_e.pop(0)
                    fahrzeug.setParkplatznummer(neue_nummer)
                    belegte_parkplaetze.add(neue_nummer)
                elif not ist_e_fahrzeug and verfuegbare_p:
                    neue_nummer = verfuegbare_p.pop(0)
                    fahrzeug.setParkplatznummer(neue_nummer)
                    belegte_parkplaetze.add(neue_nummer)
                else:
                    fahrzeug.setParkplatznummer("KEIN PLATZ")

    def getFahrzeuge(self) -> dict:
        fahrzeugListe = {"PKW": {}, "LKW": {}}
        self.__aktualisiere_parkplaetze(self.__fahrzeuge)  # Sicherstellen, dass die Parkplätze aktuell sind

        for fahrzeug in self.__fahrzeuge:
            kennzeichen = fahrzeug.getKennzeichen()
            base_data = {
                "kennzeichen": kennzeichen,
                "hersteller": fahrzeug.getHersteller(),
                "modell": fahrzeug.getModell(),
                "baujahr": fahrzeug.getBaujahr(),
                "kraftstoffart": fahrzeug.getKraftstoffart(),
                "parkplatznummer": fahrzeug.getParkplatznummer(),  # NEU: Parkplatznummer
            }
            if type(fahrzeug).__name__ == "PKW":
                fahrzeugListe["PKW"][kennzeichen] = {**base_data, "anzahlTueren": fahrzeug.getAnzahlTueren()}
            if type(fahrzeug).__name__ == "LKW":
                fahrzeugListe["LKW"][kennzeichen] = {**base_data, "ladekapazitaetKG": fahrzeug.getLadekapazitaetKG()}
        return fahrzeugListe

    def __finde_freien_parkplatz(self, fahrzeug_ist_e: bool) -> str or None:
        """Sucht den nächsten freien Parkplatz basierend auf dem Kraftstofftyp."""

        # Aktualisiere die Parkplatzlogik, um freie Plätze zu identifizieren
        self.__aktualisiere_parkplaetze(self.__fahrzeuge)
        belegte_parkplaetze = {f.getParkplatznummer() for f in self.__fahrzeuge}

        # Definiere Suchbereich (sortiert, um immer den kleinsten verfügbaren zu nehmen)
        if fahrzeug_ist_e:
            ziel_plaetze = sorted([p for p in ALLE_PARKPLÄTZE if p.startswith('E')], key=lambda p: int(p[1:]))
        else:
            ziel_plaetze = sorted([p for p in ALLE_PARKPLÄTZE if p.startswith('P')], key=lambda p: int(p[1:]))

        # Ersten freien Platz finden
        for platz in ziel_plaetze:
            if platz not in belegte_parkplaetze:
                return platz

        return None

    def addFahrzeug(self, fahrzeugtyp: str, kennzeichen: str, hersteller: str, modell: str, baujahr: int,
                    kraftstoffart: str, anzahlTueren: int, ladekapazitaetKG: int):
        for fahrzeug in self.__fahrzeuge:
            if fahrzeug.getKennzeichen() == kennzeichen:
                return f"Fahrzeug mit Kennzeichen {kennzeichen} ist bereits gepflegt."

        if hersteller.upper() not in ERLAUBTE_HERSTELLER:
            return f"Hersteller '{hersteller}' ist nicht in der Liste der erlaubten Hersteller."

        # NEU: Parkplatz Zuweisungs-Logik
        ist_e_fahrzeug = kraftstoffart in ["Hybrid", "Elektro"]
        parkplatznummer = self.__finde_freien_parkplatz(ist_e_fahrzeug)

        if parkplatznummer is None:
            if ist_e_fahrzeug:
                return "FEHLER: Alle 10 E-Parkplätze sind belegt. Kann kein E- oder Hybrid-Fahrzeug hinzufügen."
            else:
                return "FEHLER: Alle 20 Standard-Parkplätze sind belegt. Kann kein Verbrenner-Fahrzeug hinzufügen."

        # Hinzufügen des Fahrzeugs mit zugewiesener Parkplatznummer
        if fahrzeugtyp == "PKW":
            self.__fahrzeuge.append(
                PKW(kennzeichen, hersteller, modell, baujahr, kraftstoffart, anzahlTueren, parkplatznummer))
            result = f"PKW erstellt und Parkplatz {parkplatznummer} zugewiesen."
        elif fahrzeugtyp == "LKW":
            self.__fahrzeuge.append(
                LKW(kennzeichen, hersteller, modell, baujahr, kraftstoffart, ladekapazitaetKG, parkplatznummer))
            result = f"LKW erstellt und Parkplatz {parkplatznummer} zugewiesen."
        else:
            return "Ungültiger Fahrzeugtyp."

        self.speichereFuhrpark()
        return result

    def removeFahrzeug(self, kennzeichen: str):
        original_laenge = len(self.__fahrzeuge)

        fahrzeug_zum_entfernen = next(
            (f for f in self.__fahrzeuge if f.getKennzeichen().upper() == kennzeichen.upper()), None)

        self.__fahrzeuge = [fahrzeug for fahrzeug in self.__fahrzeuge if
                            fahrzeug.getKennzeichen().upper() != kennzeichen.upper()]

        if len(self.__fahrzeuge) < original_laenge:
            self.speichereFuhrpark()
            parkplatz = fahrzeug_zum_entfernen.getParkplatznummer() if fahrzeug_zum_entfernen else "unbekannt"
            return f"Fahrzeug mit Kennzeichen {kennzeichen} erfolgreich entfernt. Parkplatz {parkplatz} ist wieder frei."
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
                # Fängt Fehler ab, wenn die alte pkl-Datei nicht mehr zur neuen Klasse passt
                print(f"WARNUNG: Fehler beim Laden der Daten aus {dateiname}. Alte Datei wird ignoriert. {e}")
                return []
        else:
            print(f"Speicherdatei '{dateiname}' nicht gefunden. Starte mit leerem Fuhrpark.")
            return []


# --- VALIDIERUNGSFUNKTION (Unverändert) ---

def eingabeCheck_GUI(eingabe_wert: str, feld_typ: str) -> tuple[bool, str]:
    """Prüft die Eingabe für die GUI-Formulare."""
    aktuelles_jahr = datetime.now().year
    eingabe_wert = str(eingabe_wert)

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
        return True, checked

    elif feld_typ == "hersteller":
        checked = eingabe_wert.upper().strip()
        if checked == "":
            return False, "Hersteller darf nicht leer sein."
        if checked not in ERLAUBTE_HERSTELLER:
            return False, f"Hersteller '{eingabe_wert}' ist nicht erlaubt."
        return True, checked

    elif feld_typ == "modell":
        checked = eingabe_wert.strip()
        if checked == "":
            return False, "Modell darf nicht leer sein."
        return True, checked

    elif feld_typ == "kraftstoffart":
        checked = eingabe_wert.strip()
        if checked not in ERLAUBTE_KRAFTSTOFFE:
            return False, f"Kraftstoffart '{eingabe_wert}' ist ungültig. Erlaubt: {', '.join(ERLAUBTE_KRAFTSTOFFE)}."
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


# --- TKINTER GUI KLASSE (mit Parkplatznummer) ---

class FuhrparkGUI:
    def __init__(self, master, fuhrpark):
        self.master = master
        master.title("Fuhrpark-Management (Parkplätze: E1-E10 | P1-P20)")
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
        # Spalte "Index" durch "Parkplatz" ersetzt
        columns = ("Parkplatz", "Typ", "Kennzeichen", "Hersteller", "Modell", "Baujahr", "Kraftstoff", "Details")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(self.tree, c, False))
            # Spaltenbreite angepasst
            self.tree.column(col, anchor="w", width=75 if col in ("Typ", "Baujahr", "Kraftstoff", "Parkplatz") else 100)

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
            "kraftstoffart": tk.StringVar(value="Verbrenner"),
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
            ("Kraftstoffart:", ttk.Combobox, "kraftstoffart", ERLAUBTE_KRAFTSTOFFE),
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

        ttk.Label(self.control_frame, text="Fahrzeug Entfernen nach Kennzeichen", font=("Arial", 10, "bold")).pack(
            pady=5)
        self.remove_kennzeichen_var = tk.StringVar()
        ttk.Entry(self.control_frame, textvariable=self.remove_kennzeichen_var).pack(fill='x', pady=2)
        ttk.Button(self.control_frame, text="Fahrzeug ENTFERNEN", command=self.remove_fahrzeug).pack(fill='x', pady=5)

    def update_list(self):
        # Löscht alle alten Einträge
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fügt neue Einträge hinzu
        data = self.fuhrpark.getFahrzeuge()

        all_vehicles = []
        for typ, fahrzeuge in data.items():
            for kzn in fahrzeuge.keys():
                all_vehicles.append(fahrzeuge[kzn])

        # Sortierung: Sortiert zuerst nach Parkplatz-Typ (E vor P) und dann numerisch (E1 vor E2)
        def sort_key(fz_data):
            platz = fz_data['parkplatznummer']
            if platz.startswith('E'):
                # Numerischer Teil
                return (0, int(platz[1:]) if platz[1:].isdigit() else 999)
            elif platz.startswith('P'):
                return (1, int(platz[1:]) if platz[1:].isdigit() else 999)
            return (2, 0)  # "KEIN PLATZ" oder "Unassigned" ans Ende

        sorted_vehicles = sorted(all_vehicles, key=sort_key)

        for fz_data in sorted_vehicles:
            typ = "PKW" if "anzahlTueren" in fz_data else "LKW"
            kzn = fz_data['kennzeichen']
            details_text = f"Türen: {fz_data.get('anzahlTueren', 'N/A')}" if typ == "PKW" else f"Kapazität: {fz_data.get('ladekapazitaetKG', 'N/A')} kg"

            # Zeigt die Parkplatznummer anstelle des Index an
            self.tree.insert("", "end", iid=kzn,
                             values=(fz_data['parkplatznummer'], typ, kzn, fz_data['hersteller'], fz_data['modell'],
                                     fz_data['baujahr'], fz_data['kraftstoffart'], details_text))

    def add_fahrzeug(self):
        # 1. Daten aus den Eingabefeldern sammeln
        typ = self.vars["typ"].get()
        kennzeichen = self.vars["kennzeichen"].get()
        hersteller = self.vars["hersteller"].get()
        modell = self.vars["modell"].get()
        baujahr = self.vars["baujahr"].get()
        kraftstoffart = self.vars["kraftstoffart"].get()
        anzahlTueren = self.vars["anzahlTueren"].get()
        ladekapazitaetKG = self.vars["ladekapazitaetKG"].get()

        # 2. Validierung
        validation_fields = [
            ("kennzeichen", kennzeichen),
            ("hersteller", hersteller),
            ("modell", modell),
            ("baujahr", baujahr),
            ("kraftstoffart", kraftstoffart),
        ]

        if typ == "PKW":
            validation_fields.append(("anzahlTueren", anzahlTueren))
        else:  # LKW
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
            validated_data["kraftstoffart"],
            validated_data.get("anzahlTueren", 0),
            validated_data.get("ladekapazitaetKG", 0)
        )

        if "erstellt" in result:
            messagebox.showinfo("Erfolg", result)
            self.update_list()
            # Eingabefelder leeren
            for key in self.vars:
                if key not in ("typ", "kraftstoffart"):
                    self.vars[key].set("")
        else:
            messagebox.showerror("Fehler", result)

    def remove_fahrzeug(self):
        kennzeichen_to_remove = self.remove_kennzeichen_var.get().upper().strip()

        if not kennzeichen_to_remove:
            messagebox.showwarning("Achtung", "Bitte Kennzeichen zum Entfernen eingeben.")
            return

        # Frage zur Sicherheit nach
        if not messagebox.askyesno("Bestätigung",
                                   f"Soll das Fahrzeug mit Kennzeichen '{kennzeichen_to_remove}' wirklich entfernt werden?"):
            return

        result = self.fuhrpark.removeFahrzeug(kennzeichen_to_remove)

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

        # Durchsuche den Fuhrpark nach dem Kennzeichen
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
            detail_str += f"Parkplatz: {fahrzeug_info.get('parkplatznummer', 'N/A')}\n"  # NEU: Parkplatz
            detail_str += f"Kennzeichen: {fahrzeug_info.get('kennzeichen', 'N/A')}\n"
            detail_str += f"Hersteller: {fahrzeug_info.get('hersteller', 'N/A')}\n"
            detail_str += f"Modell: {fahrzeug_info.get('modell', 'N/A')}\n"
            detail_str += f"Baujahr: {fahrzeug_info.get('baujahr', 'N/A')}\n"
            detail_str += f"Kraftstoffart: {fahrzeug_info.get('kraftstoffart', 'N/A')}\n"

            if typ == "PKW":
                detail_str += f"Anzahl Türen: {fahrzeug_info.get('anzahlTueren', 'N/A')}"
            else:
                detail_str += f"Ladekapazität: {fahrzeug_info.get('ladekapazitaetKG', 'N/A')} kg"

            messagebox.showinfo(f"Details: {kennzeichen}", detail_str)

    def sort_column(self, tree, col, reverse):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]

        def sort_logic(t):
            val = t[0]
            if col == "Parkplatz":
                # E1, E10, E2 -> (0, 1), (0, 10), (0, 2)
                if val.startswith('E'):
                    return (0, int(val[1:]) if val[1:].isdigit() else 999)
                # P1, P10, P2 -> (1, 1), (1, 10), (1, 2)
                if val.startswith('P'):
                    return (1, int(val[1:]) if val[1:].isdigit() else 999)
                return (2, 0)  # "KEIN PLATZ" etc.
            try:
                # Normale numerische Spalten
                return float(val)
            except ValueError:
                # Textspalten
                return val.lower()

        l.sort(key=sort_logic, reverse=reverse)

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
        # Fügt E-/Hybrid-Autos und Verbrenner hinzu, um Parkplatzlogik zu testen
        Fuhrpark1.addFahrzeug("PKW", "E-TESLA-1", "TESLA", "Model S", 2024, "Elektro", 5, 0)  # E1
        Fuhrpark1.addFahrzeug("PKW", "H-BMW-2", "BMW", "i3", 2023, "Hybrid", 5, 0)  # E2
        Fuhrpark1.addFahrzeug("PKW", "V-DACIA-3", "DACIA", "Logan", 2014, "Verbrenner", 5, 0)  # P1
        Fuhrpark1.addFahrzeug("LKW", "V-LKW-4", "MERCEDES", "Actros", 2017, "Verbrenner", 0, 5500)  # P2
        Fuhrpark1.addFahrzeug("PKW", "H-TOYOTA-5", "TOYOTA", "Prius", 2022, "Hybrid", 5, 0)  # E3

    # 3. GUI starten
    root = tk.Tk()
    app = FuhrparkGUI(root, Fuhrpark1)
    root.mainloop()


if __name__ == "__main__":
    main()
