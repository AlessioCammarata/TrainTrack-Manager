'''

                ___             _            
        o O O  |   \   __ _    | |_    __ _  
       o       | |) | / _` |   |  _|  / _` | 
      TS__[O]  |___/  \__,_|   _\__|  \__,_| 
     {======|_|"""""|_|"""""|_|"""""|_|"""""|
    ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'

'''
#Var amministratore
root = False

#Sistema Operativo attuale e architettura
SO = ""
architecture = ""

#In questa var viene memorizzata la path assoluta del programma che viene calcolata durante l'avvio
path = ""

#Tiene a mente tutte le stringhe del programma per effettuare le traduzioni
Textlines = []
languages = ['IT','EN','FR','SP']    #Lista dei linguaggi disponibili

color_available = ["Red", "Green", "Lightblue", "Yellow", "Fuchsia", "Orange", "Pink", "Brown", "Gray", "Cyan","Lightgray","Default"]

locomotives_data =      []                # Lista per salvare i dati delle locomo
max_loco_standard= len(color_available)-1 # Numero max di locomotive che il sistema puo gestire --- Solo 11 colori disponibili
max_loco         =  max_loco_standard     # Numero max di locomotive che il sistema lavora --Puo gestirne di meno di 11 se si vuole si puo impostare
max_length_name  =      20                # Numero max di caratteri che il nome puo avere
max_size_loco_id =   10293                # Numero max dell'indirizzo che si puo dare ad una locomotiva
K_velocita       = 126/100                # Costante basata sulla velocita massima possibile di una locomotiva (0-126)
max_velocita     =     100                # Velocita massima che si puo dare ad una locomotiva
max_loco_auto    =       3                # Numero max di locomotive per la modalità automatica

var_velocita_tastiera = 0                 #Var che aiuta l'implementazione della tastioera nella finestra dei comandi
var_supporto = None                       #Var che aiuta l'apertura della gestione locomotiva da tastiera

# Impostazioni connessione seriale:

serial_port     = "–"   # serial_port è quella che fa riferimento alla centralina dcc,
name            = ""

serial_port1    = "-"   # serial_port1 è quella che fa riferimento ai sensori RFID
name1           = ""

serial_ports    = [serial_port,serial_port1]

port_range = 10         #Numero di porte che vengono controllate

#dizionario che controlla se il collegamento seriale per l'algoritmo è stato inizializzato o no e se la porta è abilitata o disabilitata dall'utente
# Serial_port_info[serial_ports[0]][0] = Inizialized, Serial_port_info[serial_ports[0]][1] = Enabled, Serial_port_info[serial_ports[0]][2] = Cosa c'è collegato, "Arduino Uno"
serial_port_info = {
    serial_ports[0]: [False,False,name], 
    serial_ports[1]: [False,False,name1]
}

control_var_errore = False # Variabile che serve a controllare se c'è stato un errore

# Dizionario per tenere in memoria l'apertura delle pagine
variabili_apertura = {   
    "locomotive_RFID_var":     False,           
    "locomotive_settings_var": False,
    "locomotive_creation_var": False,
    "locomotive_remove_var":   False,
    "locomotive_modify_var":   False,
    "locomotive_circuit_var":  False,
    "locomotive_info_var":     False,
    "locomotive_control_var":  []
}

# Traduzione dei colori - In questo dizionario vengono inserite le traduzioni per ogni elemento
# colors = {
#     "Red":         "",
#     "Green":       "",
#     "Lightblue":   "",
#     "Yellow":      "",
#     "Fuchsia":     "",
#     "Orange":      "",
#     "Pink":        "",
#     "Brown":       "",
#     "Gray":        "",
#     "Cyan":        "",
#     "Lightgray":   "",
#     "Default":     ""
# }
colors = {}
for color in color_available:
    colors[color] = ""
    
#Creazione in memoria dei deviatoi
# Turnout["Cambio1"] = [Stato Turnout, ID turnout, canvasdef, canvas]
Turnouts = {                   
    "Cambio 1":   [False,"","",""],
    "Cambio 2":   [False,"","",""],
    "Cambio 3":   [False,"","",""],
    "Cambio 4":   [False,"","",""],
    "Cambio 5":   [False,"","",""],
    "Cambio 6":   [False,"","",""],
    "Cambio 7":   [False,"","",""],
    "Cambio 8":   [False,"","",""]
}

#Non lo sto usando per ora
#Scambi adiacenti, contengono il numero identificativo di ogni scambio a se adiacente
#Quelli a sinistra sono i percorsi direzione sinistra e gli altri direzione destra
Adjacent_Turnouts = {
    #            Sinistra    Destra
    "Cambio 1":   [[],       [2]],
    "Cambio 2":   [[1,3],    [5]],
    "Cambio 3":   [[4],      [2,7]],
    "Cambio 4":   [[5],      [3,8]],
    "Cambio 5":   [[2,6],    [4]],
    "Cambio 6":   [[7,8],    [5]],
    "Cambio 7":   [[3],      [6,8]],
    "Cambio 8":   [[6],      [4,7]]
}

#creazione in memoria dei sensori
# terminate = [Bool di boot per algo]
# Sensors[Sensore 1] = [Ultimo messaggio ricevuto,Memoria dell'ultimo treno passato verso sinistra, indietro,Memoria dell'ultimo treno passato verso destra, avanti][color_img] [standard_color_img] |fase di test|
terminate = False
Sensors = {
    "Sensore 1":   ["","","","","purple"],
    "Sensore 2":   ["","","","","orange"],
    "Sensore 3":   ["","","","","white"],
    "Sensore 4":   ["","","","","yellow"],
    "Sensore 5":   ["","","","","green"],
    "Sensore 6":   ["","","","","blue"],
    "Sensore 7":   ["","","","","black"],
    "Sensore 8":   ["","","","","red"]
}

label = ""                  #La label è quella della pagina rfid, non riesco ad accederci da fuori poiche si trova all'interno di una funzione
canvas_array = [""]         #array dei canvas
calibred = False            #Variabile per controllare se tutti i treni in tabella sono stati calibrati
sensor_response = ["_/_"]   #Qui viene inserita la varibile del sensore per la calibrazione

'''
Se partono da 7 viaggiano verso sinistra e cominciano alla stazione

 1-GCDEFHG    -> Schiva A e B    -> Ricomincia da G, GCDEFHG
 2-GCDEFG     -> Schiva A,B,H    -> Ricomincia da G, GCDEFG
 3-GCDEFHD    -> Schiva A e B    -> Ricomincia da D, DEFHD
 4-GCDEBA     -> Schiva F e H    -> Finisce in deposito, A
 5-GCDEBC     -> Schiva A,F,H    -> Ricomincia Da C, CDEB
1A 2B 3C 4D 5E 6F 7G 8H

 6-ABEDCGFE   -> Schiva H             -> Ricomincia da E, EDCGFE
 7-ABEDHFE   -> Schiva C e G          -> Ricomincia da E, EDHFE
 8-ABEDCB     -> Schiva F,G,H         -> Ricomincia da B, BEDCB
 9-ABEDCGHFE  -> Non schiva niente    -> Ricomincia Da E, EDCGHF
'''
#Test di algo
#Per ora senza ripetizioni
LRoutes = {
1: [7,3,4,5,6,8],
2: [7,3,4,5,6],
3: [7,3,4,5,6,8],
4: [7,3,4,5,2,1],
5: [7,3,4,5,2]
}

RRoutes = {
6: [1,2,5,4,3,7,6],
7: [1,2,5,4,8,6],
8: [1,2,5,4,3,2],
9: [1,2,5,4,3,7,8,6]
}


percorsi_assegnati = []
criticita = []
root_occupied = ""
