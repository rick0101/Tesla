import matplotlib.pyplot as plt
import sys

lista_check = []
lista_aggiornata = []
diz = []

def carica_dati ():
    with open ( "dati/data.csv") as f:
        global lista_check
        global lista_aggiornata
        global diz
        for i in f:
            lista_check.append (i.replace("T01:00:00+02:00", "").replace("T00:00:00+02:00", "").replace("\n",""))
        lista_check.pop(-1)
        lista_check.pop(0)

    with open ("dati/registroTesla.txt", "r") as f:
        u = f.read()
        u = u.split("\n")

    with open ("dati/registroTesla.txt", "a") as f:
        for i in lista_check:
            if i in u:
                print (i, "---> già presente" )
            else:    
                print (i, "---> caricato correttamente")
                f.write (i + "\n")

    input()

    with open ("dati/registroTesla.txt") as f:
        for i in f:
            lista_aggiornata.append(i.replace("\n",""))

    for i in lista_aggiornata:
        diz.append({
            "data" : i.split(",")[0],
            "Utilizati_da_Casa" : float(i.split(",")[1]),
            "DaFotovoltaicoKW" : float(i.split(",")[2]),
            "DaPowerwallKW" : float(i.split(",")[3]),
            "Prelevati_da_Rete" : float(i.split(",")[4]),
            "Venduti_alla_Rete" : float(i.split(",")[5]),
                })


def filtroData():
    global diz
    anno = [i["data"].split("-")[0] for i in diz]
    mese = [i["data"].split("-")[1] for i in diz]
    giorno = [i["data"].split("-")[2] for i in diz]

    data1 = input("inserisci data partenza (in formato AAAA-MM-GG):\n") 
    anno1 = data1.split("-")[0]
    mese1 = data1.split("-")[1]
    giorno1 = data1.split ("-")[2]
    if anno1 not in anno or mese1 not in mese or giorno1 not in giorno:
        print ("data inserita:", data1, "non presente")
        input()
        return

    data2 = input("inserisci data finale (in formato AAAA-MM-GG):\n")
    anno2 = data2.split("-")[0]
    mese2 = data2.split("-")[1]
    giorno2 = data2.split ("-")[2]
    if anno2 not in anno or mese2 not in mese or giorno2 not in giorno:
        print ("data inserita:", data2, "non presente")
        input()
        return

    output = [] 
    for i in diz:
        if i["data"].split("-")[0] >= anno1 and i["data"].split("-")[1] >= mese1 and i["data"].split("-")[2] >= giorno1:
            output.append(i)
            if i["data"].split("-")[0] == anno2 and i["data"].split("-")[1] == mese2 and i["data"].split("-")[2] == giorno2:
                print ("Filtro correttamente applicato")
                break
    input()
    return output

def consumato_casa (lista_diz):
    totale = 0
    for i in lista_diz:
        totale += i["Utilizati_da_Casa"]
        totale = round(totale, 3)
    print ( f"La casa ha consumato un totale di: {totale} KW")

def Energia_Venduta (lista_diz):
    totale = 0
    for i in lista_diz:
        totale += i["Venduti_alla_Rete"]
        totale = round(totale, 3)
    print ("Alla rete sono stati venduti: " ,totale, "KW")

def preso_dalla_rete (lista_diz):
    totale = 0
    for i in lista_diz:
        totale += i["Prelevati_da_Rete"]
        totale = round(totale, 3)
    print ( "Dalla rete sono stati comprati: ",totale, "KW")

def prodotto_fotovoltaico (lista_diz):
    totale = 0
    for i in lista_diz:
        totale += round(i["DaFotovoltaicoKW"], 3)
        totale = round(totale, 3)
    print ( "Il fotovoltaico ha prodotto un totale di: ",totale, "KW")

def energia_in_eccesso (lista_diz):
    totale = 0
    for i in lista_diz:
        totale += round(i["Energia_in_Eccesso"], 3)
        totale = round(totale, 3)
    print (f"La differenza tra energia prodotta e energia utilizzata è di: {totale} KW")


def stampa_grafico (key_dict, output):
    plt.subplot(1,2,1)
    x= [int(i["data"].replace("-", "").replace("-", "")) for i in output]
    y= [i[key_dict] for i in output]
    print (x)
    print (y)
    plt.title(key_dict)
    # disegniamo il grafico
    plt.grid()
    plt.plot(x,y)
    plt.subplot(1,2,2)
    y2 = y
    plt.title(key_dict)
    plt.bar(x,y2,color='#CCCCCC')
    media = round(sum((i[key_dict] for i in output)) / len(output), 3)
    plt.axhline(y= media , c='#187FD9', linestyle='--')
    print (f"la media è: {media} KW in {len(output)} giorni")
    plt.show()



def run ():
    op = 0
    while op != 99:
        print ("1. caricare dati")
        print ("2. stampa tutti i dati")
        print ("3. utilizza tutti i dati disponibili")
        print ("4. filtra per data")
        print ("5. calcola KW presi dalla Rete")
        print ("6. calcola KW venduti")
        print ("7. calcola quantità prodotta da fotovoltaico")
        print ("8. calcola energia utilizzata dalla casa")
        print ("99. esci\n")
        op = input("Inserisci operazione:\n")
        if op == "":
            op = 999
        op = int (op)
        print ()


        if op == 1:
            carica_dati()

        if op == 2:
            for i in diz:
                print (i)
            input()


        if op == 3:
            output = diz
            input ("Operazione avvenuta con successo!")

        if op == 4:
            output = filtroData()

        if op == 5:
            preso_dalla_rete(output)
            bool = input("Mostrare il grafico?  ")
            if bool == "si":
                stampa_grafico("Prelevati_da_Rete", output)
            else:
                pass

        if op == 6:
            Energia_Venduta (output)
            bool = input("Mostrare il grafico?  ")
            if bool == "si":
                stampa_grafico("Venduti_alla_Rete", output)
            else:
                pass
            
        if op == 7:
            prodotto_fotovoltaico(output)
            bool = input("Mostrare il grafico?  ")
            if bool == "si":
                stampa_grafico("DaFotovoltaicoKW", output)
            else:
                pass
        
        if op == 8:
            consumato_casa(output)
            bool = input("Mostrare il grafico?  ")
            if bool == "si":
                stampa_grafico("Utilizati_da_Casa", output)
            else:
                pass


run()

