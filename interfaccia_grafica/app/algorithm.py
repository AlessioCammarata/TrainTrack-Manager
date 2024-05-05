import tkinter as tk
import threading
import serial
import time
import queue
import data
import utilities
import comandi
import random
#import traffic_light

'''
    Mi serve lo stato degli scambi, le info delle locomotive(velocita,direzione), e l'otuptut dei sensori
    Quando una locomotiva incontra uno scambio il sensore mi dira che lo ha incontrato, io so a quale fa riferimento, prendo i dati dallo scambio e vedo se è aperto o chiuso,
    a seconda di questo e della direzione della locomotiva, decido se aprirlo o lasciarlo come è - inoltre potro dire che il treno finche non ricevo un altro messaggio dai sensori,        
    si trova in quel pezzo di circuito.
'''

'''
                ___      _      __ _                     _      _      _              
        o O O  /   \    | |    / _` |   ___      _ _    (_)    | |_   | |_     _ __   
       o       | - |    | |    \__, |  / _ \    | '_|   | |    |  _|  | ' \   | '  \  
      TS__[O]  |_|_|   _|_|_   |___/   \___/   _|_|_   _|_|_   _\__|  |_||_|  |_|_|_| 
     {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
    ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'
'''
        
class Algorithm:

    def __init__(self):

        # Definzione della coda 
        self.message_queue = queue.Queue()
        #flag che gesetisce il fatto che io abbia dichiarato i thread
        self.called = False
        #tengo a memoria i threads
        self.threads = ["","",""]
        #flag che serve per la chiamata del thread di process_messages
        self.flag = True


    '''
                    ___                                                   
            o O O  / __|    ___    _ _      ___     ___      _ _    ___   
           o       \__ \   / -_)  | ' \    (_-<    / _ \    | '_|  (_-<   
          TS__[O]  |___/   \___|  |_||_|   /__/_   \___/   _|_|_   /__/_  
         {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
        ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
    '''

    def start_sensor(self,circuit_window):
        
        port_path = f"COM{data.serial_ports[1]}"

        try:
            ser = serial.Serial(port_path, baudrate=115200, timeout=0)

            while not data.terminate:
                try:
                    response = ser.readline().decode('utf-8').strip()
                    if response:
                        print(f"Ricevuto dalla porta seriale: {response}")
                        self.message_queue.put(response)  # Aggiungi il messaggio alla coda

                        #tengo in memoria la risposta per la registrazione delle locomotive
                        data.sensor_response[0] = response

                        message = response.split("/")
                        if data.variabili_apertura["locomotive_RFID_var"]:
                            data.label.configure(text=message[1])
                        circuit_window.tag_label.configure(text=message[1])
                            # background=data.Sensors["Sensore {}".format(message[0])][4])
                        # circuit_window.tag_label.after(1000, lambda: circuit_window.tag_label.configure(text=message[1]))
                        circuit_window.tag_color.configure(background=data.Sensors["Sensore {}".format(message[0])][4])
                        # circuit_window.tag_color.after(1000, lambda: circuit_window.tag_label.configure(text=message[1],background="SystemButtonFace"))
                    
                    #Controllo che tutte le locomotive siano calibrate e inoltre eseguo questa operazione una sola volta (se chiudo la pagina posso rifarla)
                    if data.calibred and self.flag and len(data.locomotives_data) in [2,3]:
                        # self.GUI.on_off()
                        parent = circuit_window.GUI.locomotive_RFID_window if data.variabili_apertura["locomotive_RFID_var"] else circuit_window.locomotive_window

                        utilities.show_info(data.Textlines[60],parent)
                        
                        #creo il thread e lo metto in memoria
                        process_messages_thread = threading.Thread(target=lambda:self.process_messages(circuit_window))
                        self.threads[1] = process_messages_thread
                        #pulisco la queue - avvio il thread - setto la flag
                        self.message_queue.queue.clear()
                        process_messages_thread.start()
                        self.flag = False
                        self.start_throttle(circuit_window)
                        print("PARTITO")
                        #self.flag = False
                except UnicodeDecodeError:
                    print(data.Textlines[40])
                time.sleep(0.1)
        except serial.SerialException as e:
            print(data.Textlines[21]+ str(data.serial_ports[1])+" "+data.Textlines[41]+f"\n{e}")

    '''
                    ___      _      __ _         
            o O O  /   \    | |    / _` |   ___  
           o       | - |    | |    \__, |  / _ \ 
          TS__[O]  |_|_|   _|_|_   |___/   \___/ 
         {======|_|"""""|_|"""""|_|"""""|_|"""""|
        ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'
    '''

    def calibred_RFID(self,ID_treno : int,RFIDtag : str):
        data.locomotives_data[ID_treno]["RFIDtag"] = RFIDtag

    def start_algo(self,circuit_window):

        print("Algoritmo online")

        self.called = True
        data.terminate = False
        # Crea un thread per la funzione start_sensor
        sensor_thread = threading.Thread(target=lambda:self.start_sensor(circuit_window))
        self.threads[0] = sensor_thread 
        
        self.flag = True
        #avvio i thread
        sensor_thread.start()
        
             
    def stop_algo(self):
        #Controlla che la funzione sia stata chiamata e che non sia amministratore
        if self.called and not data.root:
            data.terminate = True
            # Attendi che i thread terminino
            if self.threads[0].is_alive() or self.threads[1].is_alive():
                self.threads[0].join(timeout=5)
                if not self.flag:
                    self.threads[1].join(timeout=5)
                print("Threads terminati correttamente.")
            self.called = False

            #Set dei percorsi a []
            data.percorsi_assegnati = []
        else:
            print("l'ho fermato io ;)")

    def gestione_velocita(self,circuit_window,id,velocita):

        memoria         = data.locomotives_data[id]['ID']
        ID              = data.locomotives_data[id]['LocoID']
        direzione       = data.locomotives_data[id]['Direzione']

        #Impostare la velocita in memoria e la direzione
        data.locomotives_data[id]['Velocita']  = velocita
        data.locomotives_data[id]['Direzione'] = direzione
        velocita_effettiva = velocita * data.K_velocita

        if utilities.is_serial_port_available(data.serial_ports[0]):
            #mando il comando di throttle
            comandi.throttle(memoria,ID,round(velocita_effettiva),direzione)

        else: 
            utilities.show_error_box(data.Textlines[21]+f"{data.serial_ports[0]} "+data.Textlines[22],circuit_window.locomotive_window,"main")


    #Ritorna un vettore che contiene i percorsi liberi in quel momento
    def show_percorsi_liberi(self,id):
        direzione       = data.locomotives_data[id]['Direzione']

        #A seconda delle direzione ci sono dei percorsi diversi
        if direzione == 0:
            return list(set(data.LRoutes.keys()) - set(data.percorsi_assegnati))
        else:
            return list(set(data.RRoutes.keys()) - set(data.percorsi_assegnati))

    #Ritorna l'intersezione tra i percorsi assegnati, in modo da trovare i punti in cui si incrociano i percorsi
    def trova_criticita(self):
        return set(data.LRoutes[data.percorsi_assegnati[0]]) & set(data.RRoutes[data.percorsi_assegnati[-1]])

    #Dato un treno sceglie il percorso, inserisce il vettore contenente le criticita nel caso sia il secondo
    def scegli_percorso(self, id): 
        print("i percorsi assegnati sono: " +str(data.percorsi_assegnati))
        percorsi_liberi = self.show_percorsi_liberi(id)
        percorso_scelto = random.choice(percorsi_liberi)
        print("il percorso scelto è: " +str(percorso_scelto))
        data.percorsi_assegnati.append(percorso_scelto)

        data.locomotives_data[id]['Percorso'] = percorso_scelto
        if id != 0:
            data.criticita = self.trova_criticita()
        
    #Funzione che fa partire i treni, e sceglie il percorso iniziale, in automatico scarta la terza locomotiva
    #Devo stabilire la partenza per decidere la direzione, 
    #in questo momento la locomotivaq 1 e la 2 partono a velocita stabilita
    def start_throttle(self,circuit_window):
        if utilities.is_serial_port_available(data.serial_ports[0]):
            comandi.open_current(1)
            for i in range(2):
                #Impostiamo un percorso e la direzione da prendere
                data.locomotives_data[i]['Direzione'] = i
                self.scegli_percorso(i)

                #Impostiamo la velocita che vogliamo da 0 a 100
                velocita  = 20
                self.gestione_velocita(circuit_window,i,velocita)

                print("le criticità sono: " +str(data.criticita))
            
            #Per ora non funzione
            # for item in data.criticita:
            #     semaphore = traffic_light.Semaphore(circuit_window,item)
            #     self.semaphore.append(semaphore.thread)
        else: 
            utilities.show_error_box(data.Textlines[21]+f"{data.serial_ports[0]} "+data.Textlines[22],circuit_window.locomotive_window,"main")

#   Questa funzione controlla che i percorsi adiacenti a quelli toccati dal treno, nella direzione in cui sta andando siano liberi
    def control(self,Turnout,direzione,natural_link):

        for item in data.Adjacent_Turnouts[Turnout][direzione]:
            #Se nel sensore c'è qualcosa, attiva lo scambio, almeno che non sia passivo, 
            #in quel caso deve fermare il treno e poi farlo ripartire quando passa    --------------------------------------------
            if data.Sensors["Sensore {}".format(item)][direzione+1] != "" :
                #-1 vuoldire cambio passivo
                if natural_link == -1:
                    print("STOP")

                #Assegno il percorso che è occupato.

                data.root_occupied = item
                return natural_link==data.root_occupied
            
        return False

    def process_messages(self,circuit_window):
        # print(f"Variabile di terminazione: {GUI.Sensors['Terminate'][0]}")

        while not data.terminate:
            #Controlla che la finestra della calibrazione sia aperta
            if data.variabili_apertura["locomotive_RFID_var"]:
               #aspetta che venga chiusa e pulisce la queue
               circuit_window.GUI.locomotive_RFID_window.wait_window()
               self.message_queue.queue.clear()

            try:
                # Attendi con un timeout di 0.1 secondi
                message = self.message_queue.get(timeout=0.1)

                message = message.split("/")#-------> per separare la parte del messaggio che riguarda l'ID del sensore da quella che riguarda l'ID del treno, che corrisponde al LocoID
                canvas = data.canvas_array[0]

                #gestione dei cambi tramite l'outupt dei sensori


                #Cerco l'id corrispondente alla locomotiva che è passata.
                id = utilities.CalcolaIDtreno('RFIDtag',message[1])
                text = "Cambio {}".format(message[0])
                sensor = "Sensore {}".format(message[0])

                #Metto in memoria del sensore che ha ricevuto, l'ultimo uid letto
                data.Sensors[sensor][0] = message[1]
                canvas.after(0, circuit_window.change_Sensors, sensor, message[1])

                if data.locomotives_data[id]["Direzione"] == 0: # va verso sinistra <--
                    #Percorsi possibili partendo da G, stazione:
                    '''
                        ABCDEFGH -> 12345678
                        1-GCDEFHG    -> Schiva A e B    -> Ricomincia da G, GCDEFHG
                        2-GCDEFG     -> Schiva A,B,H    -> Ricomincia da G, GCDEFG
                        3-GCDEFHD    -> Schiva A e B    -> Ricomincia da D, DEFHD
                        4-GCDEBA     -> Schiva F e H    -> Finisce in deposito, A
                        5-GCDEBC     -> Schiva A,F,H    -> Ricomincia Da C, CDEB
                        Lettere che cambiano stato sono: -> A cambia ma si gestisce da solo
                        A,H,E,F,
                        Lettere passive sono: 
                        C,D,G

                        Albero logico:
                        if E == aperto:
                            if F == aperto:
                                if H == aperto:
                                    1
                                else:
                                    3
                            else:
                                2
                        else:
                            if B == aperto:
                                5
                            else:
                                4

                        Tutti i percorsi dipendono da E
                        Le altre dipendenze sono:
                        1 e 3 dipendono da H e F; hanno F uguale, se cambia diventa 2
                        2 Dipende da F
                        4 va in deposito, dopo di esso sicuramente si cambia direzione. Dipende da E e B
                        5 dipende da 
                        I percorsi percio sono intercambiabili, a seconda delle loro dipendenze, in ogni caso seguono questi schemi. Da 1 pero si puo andare a 4, 
                        basta modificare le dipendenze di 4 che sono E e B. Infatti tutti i percorsi dipendono da E.

                        10 = B and E -> Il percorso dieci sara la distanza tra b ed e, il suo passaggio da destra è inevitabile se si arriva da B
                        11 = E and D
                        12 = C and D
                        13 = C and B
                        14 = C and G
                        15 = G and F
                        16 = F and E
                        17 = H and G
                        18 = H and D

                        Vige la precedenza a destra
                        Partenza da A: In ogni caso bisogna controllare sinistra e destra, prima sinistra
                        10 - Arriva il segnale in A, e si decide che fare
                            if C == False,
                                if sensore C == '' or sensore C == sensore B vai pure, 
                                else aspetta che C sia == a B di DESTRA  
                            if E == False, bisogna controllare se ci sono dei treni, 
                                if sensore E != '' or sensore E == sensore B vai pure, 
                                else aspetta che E sia = a B di SINISTRA

                        11 - Arriva il segnale in B, e si decide che fare
ì
                            if sensore F == '' or sensore G == sensore F 
                                ifsensore F == sensore H vai pure, 
                                else aspetta che F sia uguale a H
                            else aspetta che F sia == a G di DESTRA  

                            if sensore D == '' or sensore D == sensore E vai pure, 
                            else aspetta che D sia = a E di SINISTRA

                         12 - Arriva il segnale in B, e si decide che fare   

                            if sensore G == '' or sensore G != sensore C 
                                   if sensore B == '' or sensore B != sensore C vai pure, 
                                   else scambia D prima che arriva l'altro treno, scambio deve essere True
                            else scambia D prima che arriva l'altro treno da 14, scambio deve essere False  DESTRA

                            2 casi:
                            Arriva da G, 
                            if B == '' or B == C, vai
                            else aspetta che B sia uguale a C

                            Arriva da G, 
                            if B == '' or B == C, vai
                            else aspetta che B sia uguale a C

                    '''
                    #A questo punto arriva il sensore che ha letto il messaggio della locomotiva che va all'indietro e ha l'id registrato dal sensore che trasmette
                    print(data.locomotives_data[id]["Nome"])
                    print("del sensore: {}".format(message[0]))

                    match text:
                        case "Cambio 1":

                            #Azzero il cambio precedente
                            data.Sensors["Sensore 2"][1] = ""

                            # database.Sensors[text][0] = message[1]
                            # canvas.after(0, GUI.change_Sensors, text, message[1])
                            data.Sensors["Sensore 5"][1] = "ABA"


                            # Avvia la funzione dopo un certo tempo, a seconda di quanto serva 
                            time = 5
                            #Impostiamo la velocita che vogliamo da 0 a 100
                            velocita  = 0
                            self.threads[2] = threading.Timer(time, lambda: self.gestione_velocita(circuit_window,id,velocita))
                            self.threads[2].start()

                            #questa if controlla che l'ultimo treno passato non sia lo stesso che è passato ora
                            if data.Sensors["Sensore 1"][1] != data.locomotives_data[id]["RFIDtag"]:
                                #comando per scambiare
                                canvas.after(0, circuit_window.change_Turnouts, text, "")
                            #Imposta la var del treno in memoria
                            data.Sensors["Sensore 1"][1] = data.locomotives_data[id]["RFIDtag"]
                            print(text,data.Sensors["Sensore 1"][1])


                        case "Cambio 2":
                            #questa if controlla che l'ultimo treno passato non sia lo stesso che è passato ora
                            # if database.Sensors["Sensore 2"][1] != database.locomotives_data[id]["RFIDtag"] and database.Sensors["Sensore 1"][2] == "":
                            #     canvas.after(0, circuit_window.change_Turnouts, text, "")
                            #     database.Sensors["Sensore 2"][1] = database.locomotives_data[id]["RFIDtag"]

                            #Azzero il cambio precedente da sinistra
                            data.Sensors["Sensore 5"][1] = ""

                            #è il collegamento che ha di natura il cambio, all'inizio di tutto.
                            natural_link = 3 if data.Turnouts[text][0] else 1
                            #Gli si puo mettere anche 0 fisso
                            #Fa il controllo, and se il link di base è uguale a quello occupato avvia lo scambio
                            if self.control(text,data.locomotives_data[id]["Direzione"],natural_link):
                                canvas.after(0, circuit_window.change_Turnouts, text, "")

                        case "Cambio 3":
                            #Azzero il cambio precedente da sinistra
                            data.Sensors["Sensore 2"][1] = ""
                            data.Sensors["Sensore 7"][1] = ""

                        case "Cambio 4":
                            #Azzero il cambio precedente da sinistra
                            data.Sensors["Sensore 3"][1] = ""
                            data.Sensors["Sensore 8"][1] = ""

                        case "Cambio 5":
                            #Azzero il cambio precedente da sinistra
                            data.Sensors["Sensore 4"][1] = ""

                        case "Cambio 6":
                            #Azzero il cambio precedente da sinistra
                            data.Sensors["Sensore 5"][1] = ""

                        case "Cambio 7":
                            #Azzero il cambio precedente da sinistra
                            data.Sensors["Sensore 6"][1] = ""
                            data.Sensors["Sensore 8"][1] = ""

                        case "Cambio 8":
                            #Azzero il cambio precedente da sinistra
                            data.Sensors["Sensore 6"][1] = ""

                        case _:
                            print("Cambio insesistente")

                else:  # va verso destra -->
                    #Percorsi possibili partendo da A, deposito treni:
                    '''
                        ABCDEFGH -> 12345678
                        1-ABEDCGFE   -> Schiva H             -> Ricomincia da E, EDCGFE
                        2-ABEDHFE   -> Schiva C e G          -> Ricomincia da E, EDHFE
                        3-ABEDCB     -> Schiva F,G,H         -> Ricomincia da B, BEDCB
                        4-ABEDCGHFE  -> Non schiva niente    -> Ricomincia Da E, EDCGHF
                        Lettere che cambiano stato sono:
                        C,D,
                        Lettere passive sono:
                        A,B,E,F,H

                        Albero logico:
                        if D == aperto:
                                2
                        else:
                            if C == aperto:
                                if G == aperto:
                                    4
                                else:
                                    1   
                            else:
                                3

                        Tutti i percorsi dipendono da D
                        Le altre dipendenze sono:
                        2 dipende solo da D
                        1 e 4 dipendono da C e G; hanno C uguale, se cambia diventa 3
                        3 Dipende da C

                        I percorsi percio sono intercambiabili, a seconda delle loro dipendenze, in ogni caso seguono questi schemi. Da 4 pero si puo andare a 3, 
                        basta modificare le dipendenze di 3 che sono D e C. Infatti tutti i percorsi dipendono da D.
                        In questo caso non sara neanche necessario cambiare D  dato che si trova nella stessa condizione di 4.

                        Negli scambi passivi vige la precedenza a destra, percio se si proviene da destra si potra andare, se si proviene da sinistra bisognera attendere lo scambio di destra e frontale
                        Gli scambi attivi dovranno invece controllare che ci sia un treno in ognuno dei suoi percorsi adiacenti.
                    '''


                    match text:
                        case "Cambio 1":
                            data.Sensors["Sensore 1"][2] = data.locomotives_data[id]["RFIDtag"]
                            #Deve avvisare il 2 che sta arrivando un treno e che quindi non puo aprirsi,
                        case "Cambio 2":
                            #Azzero il cambio precedente da destra
                            data.Sensors["Sensore 1"][2] = ""
                            data.Sensors["Sensore 3"][2] = ""


                            if data.Sensors["Sensore 1"][2] == data.Sensors["Sensore 2"][2]:
                                data.Sensors["Sensore 1"][2] = ""
                        case "Cambio 3":
                            #Azzero il cambio precedente da destra
                            data.Sensors["Sensore 4"][2] = ""

                        case "Cambio 4":
                            #Azzero il cambio precedente da destra
                            data.Sensors["Sensore 5"][2] = ""

                        case "Cambio 5":
                            #Azzero il cambio precedente da destra
                            data.Sensors["Sensore 2"][2] = ""
                            data.Sensors["Sensore 6"][2] = ""

                        case "Cambio 6":
                            #Azzero il cambio precedente da destra
                            data.Sensors["Sensore 8"][2] = ""
                            data.Sensors["Sensore 7"][2] = ""

                        case "Cambio 7":
                            #Azzero il cambio precedente da destra
                            data.Sensors["Sensore 3"][2] = ""

                        case "Cambio 8":
                            #Azzero il cambio precedente da destra
                            data.Sensors["Sensore 8"][2] = ""
                            data.Sensors["Sensore 4"][2] = ""

                        case _:
                            print("Cambio insesistente")

            except queue.Empty:
                # Timeout scaduto, controlla nuovamente la variabile di terminazione
                pass
