from modules import fuhrpark

# Text User Interface
def tui(Fuhrpark):
    druckeFahrzeuge(Fuhrpark)

def druckeFahrzeuge(Fuhrpark):
    fahrzeugListe = Fuhrpark.getFahrzeuge()
    for kategorie in fahrzeugListe:
        print(f"{20*"="}\n{kategorie}\n{20*"="}\n\n")
        for fahrzeug in kategorie:
            print(f"{fahrzeugListe}")

def main():
    # Initiierung von Fuhrpark-Objekt zur Verwaltung
    Fuhrpark = fuhrpark.Fuhrpark([])
    # manuelle Tests
    Fuhrpark.addFahrzeug("PKW", "SU_N_9513", "Seat", "Leon", 2002, 5, 0)
    Fuhrpark.addFahrzeug("LKW", "SU_SJ_513", "Fiat", "Fullback", 2017, 0, 500)
    Fuhrpark.addFahrzeug("PKW", "SU_N_9513", "Merc", "GLB", 2022, 5, 0)
    print(Fuhrpark.getFahrzeuge())
    tui(Fuhrpark)

if __name__ == "__main__":
    main()