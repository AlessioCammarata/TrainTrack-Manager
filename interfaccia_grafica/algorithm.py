import comandi
import sensor
import function
import threading
import time

'''
    Mi serve lo stato degli scambi, le info delle locomotive(velocita,direzione), e l'otuptut dei sensori
    Quando una locomotiva incontra uno scambio il sensore mi dira che lo ha incontrato, io so a quale fa riferimento, prendo i dati dallo scambio e vedo se è aperto o chiuso,
    a seconda di questo e della direzione della locomotiva, decido se aprirlo o lasciarlo come è - inoltre potro dire che il treno finche non ricevo un altro messaggio dai sensori,        
    si trova in quel pezzo di circuito.
'''
#flag che gesetisce il fatto che io abbia dichiarato i thread
called = False
serial_port = 3

def stop_threads():
    global called
    if called:
        function.Sensors["Terminate"][0] = True
        # Attendi che i thread terminino
        if sensor_thread.is_alive():
            sensor_thread.join(timeout=5)
        if process_messages_thread.is_alive():
            process_messages_thread.join(timeout=5)
        print("Threads terminati correttamente.")
        called = False
    else:
        print("l'ho fermato io ;)")

def algo(istruzione):
    global sensor_thread, process_messages_thread, called
    if istruzione == "start":
        called = True
        function.Sensors["Terminate"][0] = False
        print("Algoritmo online")
        # Crea un thread per la funzione start_sensor
        sensor_thread = threading.Thread(target=sensor.start_sensor)

        # Crea un thread per la funzione process_messages
        process_messages_thread = threading.Thread(target=process_messages)

        #probabilmente si puo togliere il contorllo qui poiche lo eseguo gia prima
        if comandi.is_serial_port_available(serial_port):
            #avvio i thread
            sensor_thread.start()
            process_messages_thread.start()
        else:
            function.show_error_box("Serial port COM3 not available","serial_port","")
    else:
        #print("ferma algoritmo")
        stop_threads()

def process_messages():
    # print(f"Variabile di terminazione: {function.Sensors['Terminate'][0]}")
    while not function.Sensors["Terminate"][0]:
        try:
            # Attendi con un timeout di 0.1 secondi
            message = sensor.message_queue.get(timeout=0.1)

            message = message.split("/")#-------> per separare la parte del messaggio che riguarda l'ID del sensore da quella che riguarda l'ID del treno, che corrisponde al LocoID

            # Logica per gestire il messaggio ricevuto
            match message[0]:
                # case "Led spento":
                #     # print(message)
                #     function.Sensors["Sensore 1"][0] = message[1]
                case "1":
                    function.Sensors["Sensore 1"][0] = message[1]
                case "2":
                    function.Sensors["Sensore 2"][0] = message[1]
                case "3":
                    function.Sensors["Sensore 3"][0] = message[1]
                case "4":
                    function.Sensors["Sensore 4"][0] = message[1]
                case "5":
                    function.Sensors["Sensore 5"][0] = message[1]
                case "6":
                    function.Sensors["Sensore 6"][0] = message[1]
                case "7":
                    function.Sensors["Sensore 7"][0] = message[1]
                case "8":
                    function.Sensors["Sensore 8"][0] = message[1]
                case _:
                    print("Messaggio non gestito")
            i=0
            #gestione dei cambi tramite l'outupt dei sensori
            for item in function.locomotives_data:
                if message[1] == function.locomotives_data[i]["LocoID"]:
                    #print(function.locomotives_data[i]["Nome"])
                    if function.locomotives_data[i]["Direzione"] == 0: # va verso sinistra <--
                        j=1
                        for item in function.Sensors:
                            if j!= 9 and function.Sensors["Sensore {}".format(j)][0] == message[1]: 
                                #A questo punto arriva il sensore che ha letto il messaggio della locomotiva che va all'indietro e ha l'id registrato dal sensore di j
                                print(function.locomotives_data[i]["Nome"])
                                print("del sensore: {}".format(j))
                                print("YES but behind")
                                text = "Cambio {}".format(j)
                                canvas = function.canvas_array[0]
                                match text:
                                    case "Cambio 1":
                                        #questa if controlla che l'ultimo treno passato non sia lo stesso che è passato ora
                                        if function.Sensors["Sensore 1"][1] != function.locomotives_data[i]["LocoID"]:
                                            canvas.after(0, function.change_Turnouts, text, "")
                                            function.Sensors["Sensore 1"][1] = function.locomotives_data[i]["LocoID"]
                                    case "Cambio 2":
                                        #questa if controlla che l'ultimo treno passato non sia lo stesso che è passato ora
                                        if function.Sensors["Sensore 2"][1] != function.locomotives_data[i]["LocoID"] and function.Sensors["Sensore 1"][2] == "":
                                            canvas.after(0, function.change_Turnouts, text, "")
                                            function.Sensors["Sensore 2"][1] = function.locomotives_data[i]["LocoID"]
                                    case "Cambio 3":
                                        function.Sensors["Sensore 3"][0] = message[1]
                                    case "Cambio 4":
                                        function.Sensors["Sensore 4"][0] = message[1]
                                    case "Cambio 5":
                                        function.Sensors["Sensore 5"][0] = message[1]
                                    case "Cambio 6":
                                        function.Sensors["Sensore 6"][0] = message[1]
                                    case "Cambio 7":
                                        function.Sensors["Sensore 7"][0] = message[1]
                                    case "Cambio 8":
                                        function.Sensors["Sensore 8"][0] = message[1]
                                    case _:
                                        print("Cambio insesistente")
                            j+=1
                    else:  # va verso destra -->
                        j=1
                        for item in function.Sensors:
                            if j!= 9 and function.Sensors["Sensore {}".format(j)][0] == message[1]: 
                                #A questo punto arriva il sensore che ha letto il messaggio della locomotiva che va in avanti e ha l'id registrato dal sensore di j
                                #quindi so: chi è passato, da dove, e in che direzione
                                print(function.locomotives_data[i]["Nome"])
                                print("del sensore: {}".format(j)) # ----> il sensore poi corrispondera al cambio, possiamo cosi ottenere lo stato del deviatoio in questione
                                print("Stato del cambio {}".format(j),function.Turnouts["Cambio {}".format(j)][0])
                                print("YES but toward")
                                text = "Cambio {}".format(j)
                                canvas = function.canvas_array[0]
                                match text:
                                    case "Cambio 1":
                                        function.Sensors["Sensore 1"][2] = function.locomotives_data[i]["LocoID"]
                                    case "Cambio 2":

                                        if function.Sensors["Sensore 1"][2] == function.Sensors["Sensore 2"][2]:
                                            function.Sensors["Sensore 1"][2] = ""
                                    case "Cambio 3":
                                        function.Sensors["Sensore 3"][0] = message[1]
                                    case "Cambio 4":
                                        function.Sensors["Sensore 4"][0] = message[1]
                                    case "Cambio 5":
                                        function.Sensors["Sensore 5"][0] = message[1]
                                    case "Cambio 6":
                                        function.Sensors["Sensore 6"][0] = message[1]
                                    case "Cambio 7":
                                        function.Sensors["Sensore 7"][0] = message[1]
                                    case "Cambio 8":
                                        function.Sensors["Sensore 8"][0] = message[1]
                                    case _:
                                        print("Cambio insesistente")
                                # if text == "Cambio 2":
                                #     canvas.after(0, function.change_Turnouts, text, "")


                            j+=1
                i+=1
        except sensor.queue.Empty:
            # Timeout scaduto, controlla nuovamente la variabile di terminazione
            pass
    # message_queue.put(None)

#algo("start")

