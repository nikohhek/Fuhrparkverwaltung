from modules import fuhrpark

def main():
    # Initiierung von Fuhrpark-Objekt zur Verwaltung
    TestFuhrpark = fuhrpark.Fuhrpark([])

    # manuelle Tests
    TestFuhrpark.addFahrzeug("PKW", "SU_N_9513", "Seat", "Leon", 2002, 5, 0)
    TestFuhrpark.addFahrzeug("LKW", "SU_SJ_513", "Fiat", "Fullback", 2017, 0, 500)
    TestFuhrpark.addFahrzeug("PKW", "SU_N_9513", "Merc", "GLB", 2022, 5, 0)
    print(TestFuhrpark.getFahrzeuge())

if __name__ == "__main__":
    main()