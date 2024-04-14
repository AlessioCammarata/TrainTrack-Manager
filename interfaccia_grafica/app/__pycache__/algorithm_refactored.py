import comandi_refactored
import threading
import serial
import time
import queue

'''
    Mi serve lo stato degli scambi, le info delle locomotive(velocita,direzione), e l'otuptut dei sensori
    Quando una locomotiva incontra uno scambio il sensore mi dira che lo ha incontrato, io so a quale fa riferimento, prendo i dati dallo scambio e vedo se è aperto o chiuso,
    a seconda di questo e della direzione della locomotiva, decido se aprirlo o lasciarlo come è - inoltre potro dire che il treno finche non ricevo un altro messaggio dai sensori,        
    si trova in quel pezzo di circuito.
'''

class Algorithm:

    def __init__(self,GUI):
        self.GUI = GUI
        self.serial_port = 5
        # Definzione della coda 
        self.message_queue = queue.Queue()
        #flag che gesetisce il fatto che io abbia dichiarato i thread
        self.called = False

    '''
                    ___                                                   
            o O O  / __|    ___    _ _      ___     ___      _ _    ___   
           o       \__ \   / -_)  | ' \    (_-<    / _ \    | '_|  (_-<   
          TS__[O]  |___/   \___|  |_||_|   /__/_   \___/   _|_|_   /__/_  
         {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
        ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
    '''

    def start_sensor(self,GUI):
        port_path = f"COM{self.serial_port}"

        try:
            ser = serial.Serial(port_path, baudrate=115200, timeout=0)

            while not GUI.Sensors["Terminate"][0]:
                try:
                    response = ser.readline().decode('utf-8').strip()
                    if response:
                        print(f"Ricevuto dalla porta seriale: {response}")
                        self.message_queue.put(response)  # Aggiungi il messaggio alla coda

                except UnicodeDecodeError:
                    print("Errore di decodifica. Assicurati che il dispositivo stia inviando dati correttamente.")
                time.sleep(0.1)
        except serial.SerialException as e:
            print(f"Errore nell'apertura della porta seriale: {e}")

    '''
                    ___      _      __ _                     _      _      _              
            o O O  /   \    | |    / _` |   ___      _ _    (_)    | |_   | |_     _ __   
           o       | - |    | |    \__, |  / _ \    | '_|   | |    |  _|  | ' \   | '  \  
          TS__[O]  |_|_|   _|_|_   |___/   \___/   _|_|_   _|_|_   _\__|  |_||_|  |_|_|_| 
         {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
        ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'
    '''

    def stop_threads(self,GUI,sensor_thread,process_messages_thread):
        if self.called:
            GUI.Sensors["Terminate"][0] = True
            # Attendi che i thread terminino
            if sensor_thread.is_alive():
                sensor_thread.join(timeout=5)
            if process_messages_thread.is_alive():
                process_messages_thread.join(timeout=5)
            print("Threads terminati correttamente.")
            self.called = False
        else:
            print("l'ho fermato io ;)")

    def algo(self,istruzione):
        
        # Crea un thread per la funzione start_sensor
        sensor_thread = threading.Thread(target=lambda:self.start_sensor(self.GUI))

        # Crea un thread per la funzione process_messages
        process_messages_thread = threading.Thread(target=lambda:self.process_messages(self.GUI))

        if istruzione == "start":
            self.called = True
            self.GUI.Sensors["Terminate"][0] = False
            print("Algoritmo online")


            #probabilmente si puo togliere il contorllo qui poiche lo eseguo gia prima
            if comandi_refactored.is_serial_port_available(self.serial_port):
                #avvio i thread
                sensor_thread.start()
                process_messages_thread.start()
            else:
                self.GUI.show_error_box("Serial port COM3 not available","serial_port","")
        else:
            #print("ferma algoritmo")
            self.stop_threads(self.GUI,sensor_thread,process_messages_thread)

    def process_messages(self,GUI):
        # print(f"Variabile di terminazione: {GUI.Sensors['Terminate'][0]}")
        while not GUI.Sensors["Terminate"][0]:
            try:
                # Attendi con un timeout di 0.1 secondi
                message = self.message_queue.get(timeout=0.1)

                message = message.split("/")#-------> per separare la parte del messaggio che riguarda l'ID del sensore da quella che riguarda l'ID del treno, che corrisponde al LocoID

                # Logica per gestire il messaggio ricevuto
                match message[0]:
                    # case "Led spento":
                    #     # print(message)
                    #     GUI.Sensors["Sensore 1"][0] = message[1]
                    case "1":
                        GUI.Sensors["Sensore 1"][0] = message[1]
                    case "2":
                        GUI.Sensors["Sensore 2"][0] = message[1]
                    case "3":
                        GUI.Sensors["Sensore 3"][0] = message[1]
                    case "4":
                        GUI.Sensors["Sensore 4"][0] = message[1]
                    case "5":
                        GUI.Sensors["Sensore 5"][0] = message[1]
                    case "6":
                        GUI.Sensors["Sensore 6"][0] = message[1]
                    case "7":
                        GUI.Sensors["Sensore 7"][0] = message[1]
                    case "8":
                        GUI.Sensors["Sensore 8"][0] = message[1]
                    case _:
                        print("Messaggio non gestito")
                i=0
                #gestione dei cambi tramite l'outupt dei sensori
                for item in GUI.locomotives_data:
                    if message[1] == GUI.locomotives_data[i]["LocoID"]:
                        #print(GUI.locomotives_data[i]["Nome"])
                        if GUI.locomotives_data[i]["Direzione"] == 0: # va verso sinistra <--
                            j=1
                            for item in GUI.Sensors:
                                if j!= 9 and GUI.Sensors["Sensore {}".format(j)][0] == message[1]: 
                                    #A questo punto arriva il sensore che ha letto il messaggio della locomotiva che va all'indietro e ha l'id registrato dal sensore di j
                                    print(GUI.locomotives_data[i]["Nome"])
                                    print("del sensore: {}".format(j))
                                    print("YES but behind")
                                    text = "Cambio {}".format(j)
                                    canvas = GUI.canvas_array[0]
                                    match text:
                                        case "Cambio 1":
                                            #questa if controlla che l'ultimo treno passato non sia lo stesso che è passato ora
                                            if GUI.Sensors["Sensore 1"][1] != GUI.locomotives_data[i]["LocoID"]:
                                                canvas.after(0, GUI.change_Turnouts, text, "")
                                                GUI.Sensors["Sensore 1"][1] = GUI.locomotives_data[i]["LocoID"]
                                        case "Cambio 2":
                                            #questa if controlla che l'ultimo treno passato non sia lo stesso che è passato ora
                                            if GUI.Sensors["Sensore 2"][1] != GUI.locomotives_data[i]["LocoID"] and GUI.Sensors["Sensore 1"][2] == "":
                                                canvas.after(0, GUI.change_Turnouts, text, "")
                                                GUI.Sensors["Sensore 2"][1] = GUI.locomotives_data[i]["LocoID"]
                                        case "Cambio 3":
                                            GUI.Sensors["Sensore 3"][0] = message[1]
                                        case "Cambio 4":
                                            GUI.Sensors["Sensore 4"][0] = message[1]
                                        case "Cambio 5":
                                            GUI.Sensors["Sensore 5"][0] = message[1]
                                        case "Cambio 6":
                                            GUI.Sensors["Sensore 6"][0] = message[1]
                                        case "Cambio 7":
                                            GUI.Sensors["Sensore 7"][0] = message[1]
                                        case "Cambio 8":
                                            GUI.Sensors["Sensore 8"][0] = message[1]
                                        case _:
                                            print("Cambio insesistente")
                                j+=1
                        else:  # va verso destra -->
                            j=1
                            for item in GUI.Sensors:
                                if j!= 9 and GUI.Sensors["Sensore {}".format(j)][0] == message[1]: 
                                    #A questo punto arriva il sensore che ha letto il messaggio della locomotiva che va in avanti e ha l'id registrato dal sensore di j
                                    #quindi so: chi è passato, da dove, e in che direzione
                                    print(GUI.locomotives_data[i]["Nome"])
                                    print("del sensore: {}".format(j)) # ----> il sensore poi corrispondera al cambio, possiamo cosi ottenere lo stato del deviatoio in questione
                                    print("Stato del cambio {}".format(j),GUI.Turnouts["Cambio {}".format(j)][0])
                                    print("YES but toward")
                                    text = "Cambio {}".format(j)
                                    canvas = GUI.canvas_array[0]
                                    match text:
                                        case "Cambio 1":
                                            GUI.Sensors["Sensore 1"][2] = GUI.locomotives_data[i]["LocoID"]
                                        case "Cambio 2":

                                            if GUI.Sensors["Sensore 1"][2] == GUI.Sensors["Sensore 2"][2]:
                                                GUI.Sensors["Sensore 1"][2] = ""
                                        case "Cambio 3":
                                            GUI.Sensors["Sensore 3"][0] = message[1]
                                        case "Cambio 4":
                                            GUI.Sensors["Sensore 4"][0] = message[1]
                                        case "Cambio 5":
                                            GUI.Sensors["Sensore 5"][0] = message[1]
                                        case "Cambio 6":
                                            GUI.Sensors["Sensore 6"][0] = message[1]
                                        case "Cambio 7":
                                            GUI.Sensors["Sensore 7"][0] = message[1]
                                        case "Cambio 8":
                                            GUI.Sensors["Sensore 8"][0] = message[1]
                                        case _:
                                            print("Cambio insesistente")
                                    # if text == "Cambio 2":
                                    #     canvas.after(0, GUI.change_Turnouts, text, "")


                                j+=1
                    i+=1
            except queue.Empty:
                # Timeout scaduto, controlla nuovamente la variabile di terminazione
                pass
