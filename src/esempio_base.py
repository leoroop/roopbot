# I tipi di python

# - Numeri
# - Stringhe
# - Liste
# - Dizionari
# - Tuple
# - Booleani

while True:
    spettatore = input("Inserisci il nome dello spettatore da salutare: ")
    entusiasmo = int(input("Dai un voto al tuo entusiasmo: "))
    punti_esclamativi = ""
    for i in range(entusiasmo):
        # spettatore += "!"  spettatore -> Rossetto!!!
        punti_esclamativi += "!"

    print("Hello %s%s\n" % (spettatore, punti_esclamativi))

    if spettatore == "Rossetto":
        break

print("Ho finito")
