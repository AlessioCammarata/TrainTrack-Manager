import tkinter as tk
from tkinter import ttk
import random
import comandi_refactored
import cam


#Finestre varie
class Windows:

    def __init__(self,locomotive_window,title,dimensions):
        self.locomotive_window = locomotive_window
        self.locomotive_window.title(title)
        self.locomotive_window.geometry(dimensions)
        #per disabilitare il ridimensionamento
        self.locomotive_window.resizable(False, False)
        

    def creation_window(self,GUI):
        
            def save_locomotive():
                global locomotive_names
                global id
                name            = name_entry.get()
                loco_id         = loco_id_entry.get()
                color           = var_color.get()
                #se il colore non è selezionato, ne verra selezionato uno casualmente tra quelli nel vettore che verra rimosso dal vettore in quanto selezionato
                if color == "Default":
                    color = random.choice([colore for colore in GUI.color_available if colore != "Default" ])
                GUI.color_available.remove(color)
                controllo_loco  = len(GUI.locomotives_data)<GUI.max_loco #Controllo per vedere che il numero delle locomotive non sia al limite

                #controllo sugli input
                if name == "" or not loco_id.isdigit() or color.isdigit() or int(loco_id)==0:
                    GUI.show_error_box("Input inseriti incorrettamente","close_window/locomotive_creation_var","")
                    
                    #open_locomotive_creation_window()
                elif len(name)>GUI.max_length_name or int(loco_id)>GUI.max_size_loco_id:
                    GUI.show_error_box("Hai superato il limite di lunghezza/grandezza","close_window/locomotive_creation_var","")
                    #open_locomotive_creation_window()
                else:
                    
                    #controllo se esistono dei buchi tra gli ID
                    if len(GUI.locomotives_data) == 0:
                        id = 1
                    else: 
                        id = GUI.locomotives_data[-1]['ID'] +1
                    

                    #definizione delle locomotive
                    locomotive = {
                        'ID': id,
                        'Nome': name,
                        'LocoID': loco_id,
                        'Colore': color,
                        'Velocita':0,
                        'VelocitaM':0,
                        'Direzione':1
                    }
                    #controllo per vedere se il nome è gia stato usato all'interno del vettore
                    nome_unico = True
                    j=0
                    if GUI.locomotives_data:
                        while nome_unico:
                            nome_unico = name != GUI.locomotives_data[j]['Nome']
                            unicita = nome_unico

                            j = j+1
                            if j == len(GUI.locomotives_data):  
                                nome_unico = False
                    else: 
                        unicita=True
                    
                    #Controllo sulla dimensione del circuito
                    if unicita and controllo_loco:
                        GUI.locomotives_data.append(locomotive)
                        GUI.update_table()
                        #Aggiornamento dei bottoni a seconda degli input
                        locomotive_names = [locomotive['Nome'] for locomotive in GUI.locomotives_data]

                    else: 
                        GUI.show_error_box("Non puoi inserire piu di una locomotiva con lo stesso nome (max 3 locomotive per questo circuito)","close_window/locomotive_creation_var","")
                        # open_locomotive_creation_window()

                #chiude la finestra 
                GUI.on_close(self.locomotive_window,-1)
                #controlla che nel vettore ci sia ancora spazio e che la var di chiusura sia True
                if  GUI.variabili_chiusura["locomotive_creation_var"] and controllo_loco:
                    self.locomotive_window.after(0,GUI.open_locomotive_creation_window())
                #locomotive_creation_window.destroy()
            


            # Creazione del form per la nuova locomotiva
            name_label = tk.Label(self.locomotive_window, text="Nome:")
            name_label.pack()
            name_entry = tk.Entry(self.locomotive_window)
            name_entry.pack()

            loco_id_label = tk.Label(self.locomotive_window, text="LocoID:")
            loco_id_label.pack()
            loco_id_entry = tk.Entry(self.locomotive_window)
            loco_id_entry.pack()

            color_label = tk.Label(self.locomotive_window, text="Colore*:")
            color_label.pack()

    #Il numero dei colori all'interno del vettore deve essere almeno pari al numero di locomoitive massime del sistema, senno errore
            var_color = tk.StringVar(value=GUI.color_available[-1])
            color_button = ttk.Menubutton(self.locomotive_window,text="Default",width=19)
            color = tk.Menu(color_button, tearoff=0)
            color_button.pack()

            color_button["menu"] = color
            color.delete(0, "end")
            for item in GUI.color_available:
                color.add_radiobutton(
                    label=item,
                    value=item,
                    variable=var_color,
                    command=lambda:color_button.configure(text=var_color.get())
                    )
            
            style1 = ttk.Style()
            style1.configure('UniqueCustom.TMenubutton',padding=(),background="white")  #background ="#add8e6" 
            color_button.config(style='UniqueCustom.TMenubutton')

            save_button = tk.Button(self.locomotive_window, text="Salva", command=save_locomotive)
            save_button.pack(pady=(10,0))

            #permette di avviare la funzione con il tasto invio
            self.locomotive_window.bind('<Return>', lambda event: save_locomotive())
            
        
    def remove_window(self,GUI):
            
        def remove_locomotive():
            name    = name_entry.get()
            id      = ID_entry.get()
            # print(CalcolaIDtreno("Nome",name))
            # 
            #controllo sugli input
            if name == "" or not id.isdigit() or int(id) < 1:
                GUI.show_error_box("Input inseriti incorrettamente","close_window/locomotive_remove_var","")
                #open_locomotive_remove_window()
            else:
                id = int(id)
                #controllo per vedere qual è l'ultimo ID
                if id <= GUI.locomotives_data[-1]['ID']:
                    #prende l'indice dell'elememento in cui trova l'ID
                    index = GUI.CalcolaIDtreno('ID',id)

                    #controllo su se trova l'indice e il nome equaivale a quello inserito 
                    if index is not None and name == GUI.locomotives_data[index]['Nome']:
                        #prima di rimuovere la locomotiva, aggiungo il colore che le apparteneva al vettore dei colori disponibili
                        GUI.color_available.insert(0,GUI.locomotives_data[index]['Colore'])
                        GUI.locomotives_data.remove(GUI.locomotives_data[index])
                        GUI.update_table()
                    else: 
                        GUI.show_error_box("Id e nome non coincidono con nessuna locomotiva registrata","close_window/locomotive_remove_var","")
                        #open_locomotive_remove_window()
                else:
                    GUI.show_error_box("ID non valido","close_window/locomotive_remove_var","")
                    #open_locomotive_remove_window()
            #chiude la finestra 
            GUI.on_close(self.locomotive_window,-1)
            if  GUI.variabili_chiusura["locomotive_remove_var"]:
                self.locomotive_window.after(20,GUI.open_locomotive_remove_window())
            #locomotive_remove_window.destroy()

            
        # Creazione del form per la nuova locomotiva
        name_label = tk.Label(self.locomotive_window, text="Nome:")
        name_label.pack()
        name_entry = tk.Entry(self.locomotive_window)
        name_entry.pack()

        ID_label = tk.Label(self.locomotive_window, text="ID:")
        ID_label.pack()
        ID_entry = tk.Entry(self.locomotive_window)
        ID_entry.pack()

        remove_button = tk.Button(self.locomotive_window, text="Rimuovi", command=remove_locomotive)
        remove_button.pack()

        #permette di avviare la funzione con il tasto invio
        self.locomotive_window.bind('<Return>', lambda event: remove_locomotive())
        

    def modify_window(self,GUI):

        def modify_locomotive(): # Qui puoi gestire i dati inseriti nel form (es. salvataggio, stampa, etc.)
            name        = name_entry.get()
            id          = ID_entry.get()
            loco_id     = loco_id_entry.get()
            color       = var_color.get()

            #controlli sugli input
            if not loco_id.isdigit() or not id.isdigit() or int(loco_id)==0 or int(id)==0:
                GUI.show_error_box("Input inseriti incorrettamente","close_window/locomotive_modify_var","")
                #open_locomotive_modify_window()
            elif len(name)>GUI.max_length_name or int(loco_id)>GUI.max_size_loco_id:
                GUI.show_error_box("Hai superato il limite di lunghezza/grandezza","close_window/locomotive_modify_var","")
            else:
                id          = int(id)
                nome_unico  = True
                j=0
                #prende l'indice dell'elememento in cui trova l'ID
                index_to_replace = GUI.CalcolaIDtreno('ID',id)
                if index_to_replace is not None:
                    #se gli do una stringa vuota mi mette in automatico il noemche corrisponde all'ID
                    if name != '':
                        #controllo per vedere se il nome è gia stato usato all'interno del vettore
                        while nome_unico:
                            nome_unico = name != GUI.locomotives_data[j]['Nome']
                            unicita = nome_unico
                            j = j+1
                            if j == len(GUI.locomotives_data):  
                                nome_unico = False

                        if GUI.locomotives_data[index_to_replace]['Nome'] == name:
                            unicita = True
                    else:
                        name = GUI.locomotives_data[index_to_replace]['Nome']
                        unicita = True

                    #controlla che ci sia stata corrispondenza per l'indice e che il nome non sia gia stato utilizzato
                    if unicita:

                        #Sostituisci il dizionario all'indice trovato con il nuovo dizionario
                        if GUI.locomotives_data[index_to_replace]['LocoID'] != loco_id:
                            if GUI.are_you_sure("Prima di continuare assicurati di avere solo la locomotiva alla quale si vuole cambiare l'indirizzo sui binari"):
                                if color != "Default":
                                    #prima di sostituire la locomotiva, aggiungo il colore che le apparteneva al vettore dei colori disponibili
                                    GUI.color_available.insert(0,GUI.locomotives_data[index_to_replace]['Colore'])
                                    GUI.color_available.remove(color)
                                else:
                                    #assegno il colore che gia ha
                                    color = GUI.locomotives_data[index_to_replace]['Colore']
                                new_dict = {'ID':id,'Nome': name, 'LocoID':loco_id, 'Colore':color, 'Velocita':0, 'VelocitaM':0, 'Direzione':1}
                                if comandi_refactored.is_serial_port_available(""):
                                    comandi_refactored.change_id(GUI.locomotives_data[index_to_replace]['LocoID'],loco_id)
                                else: print("Serial port COM4 not available")
                                GUI.locomotives_data[index_to_replace] = new_dict
                            else:
                                GUI.variabili_chiusura["locomotive_modify_var"] = True
                        else:
                            if color != "Default":
                                #prima di sostituire la locomotiva, aggiungo il colore che le apparteneva al vettore dei colori disponibili
                                GUI.color_available.insert(0,GUI.locomotives_data[index_to_replace]['Colore'])
                                GUI.color_available.remove(color)
                            else:
                                #assegno il colore che gia ha
                                color = GUI.locomotives_data[index_to_replace]['Colore']
                            new_dict = {'ID':id,'Nome': name, 'LocoID':loco_id, 'Colore':color, 'Velocita':0, 'VelocitaM':0, 'Direzione':1}
                            GUI.locomotives_data[index_to_replace] = new_dict
                        GUI.update_table()
                    
                    else:
                        GUI.show_error_box("Nome gia inserito","close_window/locomotive_modify_var","")
                        #open_locomotive_modify_window()
                else:
                    GUI.show_error_box("Indice non valido","close_window/locomotive_modify_var","")
            #chiude la finestra  
            GUI.on_close(self.locomotive_window,-1)
            if GUI.variabili_chiusura["locomotive_modify_var"]:
                self.locomotive_window.after(20,GUI.open_locomotive_modify_window())
            #locomotive_modify_window.destroy()
        
        # Creazione del form per la nuova locomotiva
        ID_label = tk.Label(self.locomotive_window, text="ID della locomotiva da modificare:")
        ID_label.pack()
        ID_entry = tk.Entry(self.locomotive_window)
        ID_entry.pack()

        name_label = tk.Label(self.locomotive_window, text="Nuovo Nome:")
        name_label.pack()
        name_entry = tk.Entry(self.locomotive_window)
        name_entry.pack()

        loco_id_label = tk.Label(self.locomotive_window, text="Nuovo LocoID:")
        loco_id_label.pack()
        loco_id_entry = tk.Entry(self.locomotive_window)
        loco_id_entry.pack()

        color_label = tk.Label(self.locomotive_window, text="Colore*:")
        color_label.pack()

#Il numero dei colori all'interno del vettore deve essere almeno pari al numero di locomoitive massime del sistema, senno errore
        var_color = tk.StringVar(value=GUI.color_available[-1])
        color_button = ttk.Menubutton(self.locomotive_window,text="Default",width=19)
        color = tk.Menu(color_button, tearoff=0)
        color_button.pack()

        color_button["menu"] = color
        color.delete(0, "end")
        for item in GUI.color_available:
            color.add_radiobutton(
                label=item,
                value=item,
                variable=var_color,
                command=lambda:color_button.configure(text=var_color.get())
                )
        
        # style1 = ttk.Style()
        # style1.configure('UniqueCustom.TMenubutton', borderwidth=1, relief="solid", padding=()) 
        color_button.config(style='UniqueCustom.TMenubutton')

        modify_button = tk.Button(self.locomotive_window, text="Modifica", command=modify_locomotive)
        modify_button.pack(pady=(10,0))

        #permette di avviare la funzione con il tasto invio
        self.locomotive_window.bind('<Return>', lambda event: modify_locomotive())

    def control_window(self,GUI,locomotiva,id_controllo):
        speed_label = tk.Label(self.locomotive_window, text="Regola la velocità:")
        speed_label.pack(pady=10)

        #creazione dello slider
        speed_slider = tk.Scale(self.locomotive_window, from_=0, to=100, orient=tk.HORIZONTAL)
        speed_slider.pack(pady=5)

        #funzione per settare lo slider alla velocita salvata
        speed_slider.set(GUI.locomotives_data[id_controllo]['Velocita'])
        GUI.check_control_button_state()
    
        root_control = tk.Frame(self.locomotive_window)
        root_control.pack(pady=5)
        #root_control.configure(bg="#c0c0c0")

        #funzione per il throttle delle locomotive
        def throttle_command(direzione):
            #prendere gli input da mandare al comando
            velocita        = speed_slider.get()
            id_loco         = GUI.CalcolaIDtreno('Nome',locomotiva)
            memoria         = GUI.locomotives_data[id_loco]['ID']
            ID              = GUI.locomotives_data[id_loco]['LocoID']
            #Impostare la velocita in memoria e la direzione
            GUI.locomotives_data[id_loco]['Velocita']  = velocita
            GUI.locomotives_data[id_loco]['Direzione'] = direzione
            #moltiplicazione per la costante e approssimazione
            velocita_effettiva = velocita*GUI.K_velocita
            if comandi_refactored.is_serial_port_available(""):
                #mando il comando di throttle
                comandi_refactored.throttle(memoria,ID,round(velocita_effettiva),direzione)
            else: GUI.show_error_box("Serial port COM4 not available","focus_page/_",self.locomotive_window)

        #funzione per arrestare la locomotiva - setta lo slider a 0
        def stop_command():
            #prendere gli input da mandare al comando
            id_loco     = GUI.CalcolaIDtreno('Nome',locomotiva)
            memoria     = GUI.locomotives_data[id_loco]['ID']
            ID          = GUI.locomotives_data[id_loco]['LocoID']
            #Impostare la velocita in memoria e la direzione
            GUI.locomotives_data[id_loco]['VelocitaM']  = GUI.locomotives_data[id_loco]['Velocita']
            GUI.locomotives_data[id_loco]['Velocita']   = 0
            if comandi_refactored.is_serial_port_available(""):
                comandi_refactored.STOP(memoria,ID)
                speed_slider.set(0)
            else: GUI.show_error_box("Serial port COM4 not available","focus_page/_",self.locomotive_window)
            
        
        #creazione del form
        direction_label = tk.Label(root_control, text="Direzione:")
        direction_label.pack(side=tk.TOP, pady=5)

        forward_button = tk.Button(root_control, text="Avanti",command=lambda:throttle_command(1))
        forward_button.pack(side=tk.LEFT, padx=5,pady=5)

        backward_button = tk.Button(root_control, text="Indietro",command=lambda:throttle_command(0))
        backward_button.pack(side=tk.LEFT, padx=5,pady=5)

        stop_button = tk.Button(self.locomotive_window, bg="#f08080", text="Arresta",command=stop_command)
        stop_button.pack(pady=5)

        self.locomotive_window.bind('<Return>', lambda event: stop_command())

# #devo vedere
# def singleton(cls):
#     instances = {}

#     def get_instance(*args, **kwargs):
#         if cls not in instances:
#             instances[cls] = cls(*args, **kwargs)
#         return instances[cls]

#     return get_instance

# @singleton
class circuit_window(Windows):

    def __init__(self,locomotive_window,title,nscambi,algo):
        super().__init__(locomotive_window,title,"")
        self.nscambi = nscambi
        self.serial_port = 5
        #richiamo del'oggetto algo
        self.algo = algo
        #creazione dell'oggetto camera
        self.camera = cam.Camera(self.locomotive_window)

    #Funzione per cambiare i deviatoi
    def change_Turnouts(self,GUI,text,button):
        #gestione grafica degli scambi
        if button == "":
            pass
        else:
            current_color = button.cget("background")
            new_color = "#8fbc8f" if current_color == "#f08080" else "#f08080"
            new_text = "/" if current_color == "#f08080" else "|"
            button.config(background=new_color,text=new_text)

        if comandi_refactored.is_serial_port_available(""):
            comandi_refactored.cambia_deviatoio(GUI.Turnouts[text][1])

            #print("fuori ",Turnouts[text][1])
            if not GUI.Turnouts[text][0]:
                self.change_color(GUI,text,GUI.Turnouts[text][0])
                GUI.Turnouts[text][0] = True
                
            else:
                self.controlla_scambi_doppi(GUI,text)
                GUI.Turnouts[text][0] = False 

    #Funzione che controlla se lo scambio_doppio è selezionato da almeno 1 dei due, se è cosi non cambia il centrale ma l'altro, senno lo cambia
    def controlla_scambi_doppi(self,GUI,text):
        if GUI.Turnouts[text][3] == GUI.Turnouts['Cambio 4'][3]:
            #qui siamo entrati sia nel caso in cui text è 4 sia se è 8
            if GUI.Turnouts['Cambio 4'][0] and GUI.Turnouts['Cambio 8'][0]:
                #dato che una è una curva e l'altra è un segmento, bisogna specificare il caso
                if text == 'Cambio 4':
                    GUI.canvas_array[0].itemconfig(GUI.Turnouts[text][2], fill="red")
                else:
                    GUI.canvas_array[0].itemconfig(GUI.Turnouts[text][2], outline="red")
            else:
                #nel caso in cui non siano entrambi attivi, esegue semplicemente la funzione
                self.change_color(GUI,text,GUI.Turnouts[text][0])
            
        elif GUI.Turnouts[text][3] == GUI.Turnouts['Cambio 6'][3]:
            #qui siamo entrati sia nel caso in cui text è 6 sia se è 7
            if GUI.Turnouts['Cambio 6'][0] and GUI.Turnouts['Cambio 7'][0]:
                #dato che sono entrambe curve basta un solo comando, non si cambia quello comune
                GUI.canvas_array[0].itemconfig(GUI.Turnouts[text][2], outline="red")
            else:
                #nel caso in cui non siano entrambi attivi, esegue semplicemente la funzione
                self.change_color(GUI,text,GUI.Turnouts[text][0])
        else:
            #nel caso in cui non siano tra gli scambi doppi, esegue semplicemente la funzione
            self.change_color(GUI,text,GUI.Turnouts[text][0])


    #Funzione che ccambia il colore dello0 scambio in base a come è nel circuito
    def change_color(self,GUI,text,activated):
        print(GUI.Turnouts[text])
        if text not in {'Cambio 3', 'Cambio 4', 'Cambio 5'}:
            #Se il cambio è fromato da 2 curve
            if activated:
                GUI.canvas_array[0].itemconfig(GUI.Turnouts[text][2], outline="red")
                GUI.canvas_array[0].itemconfig(GUI.Turnouts[text][3], outline="black")   
            else:
                GUI.canvas_array[0].itemconfig(GUI.Turnouts[text][3], outline="red")
                GUI.canvas_array[0].itemconfig(GUI.Turnouts[text][2], outline="black")
        else:
            #Se il cambio è fromato da 1 curva ed un segmento
            if activated:
                GUI.canvas_array[0].itemconfig(GUI.Turnouts[text][2], fill="red")
                GUI.canvas_array[0].itemconfig(GUI.Turnouts[text][3], outline="black")
            else:
                GUI.canvas_array[0].itemconfig(GUI.Turnouts[text][3], outline="red")
                GUI.canvas_array[0].itemconfig(GUI.Turnouts[text][2], fill="black")

    def open_circuit_window(self,GUI,automatico):
        #creo un oggetto Algorithm
        '''
                    ___      _                               _      _     
            o O O  / __|    (_)      _ _    __     _  _     (_)    | |_   
           o      | (__     | |     | '_|  / _|   | +| |    | |    |  _|  
          TS__[O]  \___|   _|_|_   _|_|_   \__|_   \_,_|   _|_|_   _\__|  
         {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
        ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
        '''
 
            #funzione che gestisce il bottone che attiva la webcam
        def change_color_webcam():
            current_color = webcam.cget("background")
            new_color = "green" if current_color == "blue" else "blue"
            new_text = "VIDEO ON" if current_color == "blue" else "VIDEO OFF"
            
            if current_color == "blue" :
                controlloCam = self.camera.cattura_webcam("esiste")
                if controlloCam:
                    webcam.config(background=new_color,text=new_text)
                    self.camera.cattura_webcam("")
                else:
                    GUI.show_error_box("Collega una videocamera","focus_page/_",root)
            else:
                webcam.config(background=new_color,text=new_text)
                self.camera.cattura_webcam("chiudi")

    #funzione che gestisce il cambio da manuale a automatico
        def change_window(text,root):
            #root.destroy()
            #controllo per effettuare correttamente il cap.release
            if text=="MANUALE" and self.camera.impostazioni[0]!="": 
                self.camera.cattura_webcam("chiudi")
            #Distrugge tutti i widget presenti nella pagina corrente
            for widget in root.winfo_children():
                widget.destroy()
            #avvia la pagina selezionata
            if text == "MANUALE":
                self.algo.algo("stop")
                self.open_circuit_window(GUI,False)
            else: 
                self.open_circuit_window(GUI,True)


    # Funzione per creare un label con un checkbutton
        def create_label_with_button(canvas, x, y, text):
            label = canvas.create_text(x, y, text=text, anchor=tk.W)  # Crea il testo sul canvas
            if automatico:
                pass
                #button = tk.Button(canvas, text="OFF", width=3, height=1,bg="blue" ,command=lambda: change_color_webcam(text,button))
            else:
                button = tk.Button(canvas, text="|", width=3, height=1,bg="#f08080" ,command=lambda: self.change_Turnouts(GUI,text,button))
            canvas.create_window(x + 55, y + 0, window=button, anchor=tk.W)  # Crea il bottone vicino al testo sul canvas
            return label, button

        def START():
            #gestione grafica degllo start dell'Auto version
            current_color = start_button.cget("background")
            new_color = "#00ff00" if current_color == "red" else "red"
            
            if comandi_refactored.is_serial_port_available(""):
                start_button.config(background=new_color)
                self.algo.algo("start") if current_color == "red" else self.algo.algo("stop")
            else:
                GUI.show_error_box("Serial port COM3 not available","serial_port",root)
            

        #---------CREAZIONE DELLA PAGINA---------

        root = self.locomotive_window

        canvas_width = 1200
        canvas_height = 700

        frame = tk.Frame(root)
        frame.pack(anchor=tk.NW)

        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
        canvas.pack(side=tk.LEFT, expand=True)
        GUI.canvas_array[0] = canvas

        if automatico:
            text = "MANUALE"
            feature_button = tk.Button(frame, text=text, height = 2, command=lambda:change_window(text,root))
            feature_button.pack(side=tk.LEFT)

            image_power_path="interfaccia_grafica\\assets\\power_icon.png"
            image_power = GUI.process_image(image_power_path,'resize',35,35)
            start_button = tk.Button(frame, image=image_power,bg="red", command=START)
            start_button.pack(padx=(10,5),side=tk.LEFT)
            
            webcam = tk.Button(frame, text="VIDEO OFF", height=2,bg="blue" ,command=lambda: change_color_webcam())
            webcam.pack(padx=5,side=tk.LEFT)

            locomotive_label = tk.Label(frame, text="CONTROLLO AUTOMATICO CIRCUITO")
            locomotive_label.pack(padx=(340,0),pady=10,side=tk.LEFT)

            #webcam = create_label_with_button(canvas,600,350,"Attiva Webcam")
        else:
            text = "AUTOMATICO"
            feature_button = tk.Button(frame, text=text, height = 2, command=lambda:change_window(text,root))
            feature_button.pack(side=tk.LEFT)

            locomotive_label = tk.Label(frame, text="CONTROLLO MANUALE CIRCUITO")
            locomotive_label.pack(padx=462,pady=10,side=tk.LEFT, anchor=tk.NW)

        #creazione dei bottoni per i deviatoi
            cambio1, button1 = create_label_with_button(canvas, 10, 60, "Cambio 1")
            cambio2, button2 = create_label_with_button(canvas, 200, canvas_height-630, "Cambio 2")
            cambio3, button3 = create_label_with_button(canvas, 375, canvas_height-20, "Cambio 3")
            cambio4, button4 = create_label_with_button(canvas, 675, canvas_height-20, "Cambio 4")
            cambio5, button5 = create_label_with_button(canvas, 1050, canvas_height-450, "Cambio 5")
            cambio6, button6 = create_label_with_button(canvas, 875, 60, "Cambio 6")
            cambio7, button7 = create_label_with_button(canvas, 150, canvas_height-500, "Cambio 7")
            cambio8, button8 = create_label_with_button(canvas, 415, canvas_height-150, "Cambio 8")

        
        # feature_button.pack(side=tk.LEFT)
        #locomotive_label.pack(padx=472,pady=10,side=tk.LEFT)
  


        #----DISEGNO CIRCUITO---- link docs: https://www.pythontutorial.net/tkinter/tkinter-canvas/

        # Percorso dell'immagine originale
        stop_path = 'interfaccia_grafica\\assets\\stop_treno.png'
        casetta_path = 'interfaccia_grafica\\assets\\casetta.png'
        sensore_path = 'interfaccia_grafica\\assets\\sensore_rfid.jpg'
        # binario_path = 'interfaccia_grafica\\assets\\binario.png'

        # Ridimensiona l'immagine utilizzando la funzione resize_image
        stop_treno = GUI.process_image(stop_path,'resize', 50, 50)
        casetta = GUI.process_image(casetta_path,'resize', 100, 100)
        # binario = process_image(binario_path,'resize', 100, 100)
        sensore = GUI.process_image(sensore_path,'resize', 50, 50)
        sensore_rotated1 = GUI.process_image(sensore_path,'rotate', -90, 50, 50)  # Ruota a sinistra
        sensore_rotated2 = GUI.process_image(sensore_path,'rotate', -180, 50, 50)  # Ruota di 180
        sensore_rotated3 = GUI.process_image(sensore_path,'rotate', 90, 50, 50)  # Ruota a destra

        canvas.create_image(
            (30, canvas_height-150),
            image=stop_treno,
        )

        canvas.create_image(
            (70, canvas_height-50),
            image=stop_treno,
        )

        canvas.create_image(
            (700, 450),
            image=casetta,
        )

        canvas.create_image(
            (780, 300),
            image=casetta,
        )

        canvas.create_image(
            (900, 620),
            image=sensore,
        )

        canvas.create_image(
            (135, 300),
            image=sensore_rotated1,
        )

        canvas.create_image(
            (1145, 400),
            image=sensore_rotated3,
        )

        canvas.create_image(
            (350, 70),
            image=sensore_rotated2,
        )

        #linee sinistra con stop
        canvas.create_line((30, 155), (30, canvas_height-160), width=8, fill='black')
        canvas.create_line((70, 150), (70, canvas_height-60), width=8, fill='black')
        canvas.create_line((30, 155), (30, canvas_height-160), width=4, fill='white')
        canvas.create_line((70, 150), (70, canvas_height-60), width=4, fill='white')

        #linea in alto dritta
        canvas.create_line((293, 31), (1000, 31), width=8, fill='black')
        canvas.create_line((293, 31), (1000, 31), width=4, fill='white')

        # Disegna l'immagine come sfondo centrata sulla linea superiore
        # x = 270
        # for i in range(8):
        #     canvas.create_image(x, -20, anchor=tk.NW, image=binario)
        #     x += 95
        #     i +=1
        # canvas.create_image(365, -20, anchor=tk.NW, image=binario)
        
        #curva esterna in alto a destra
        canvas.create_arc((825, 270), (1175, 30), style=tk.ARC, start=0, extent=90, width=8, outline="black")
        canvas.create_arc((825, 270), (1175, 30), style=tk.ARC, start=0, extent=90, width=4, outline="white")
        # canvas.create_oval((825, 270), (1175, 30), outline="black", width=2)

        #linea destra esterna dritta
        canvas.create_line((1175, 150), (1175, canvas_height-170), width=8, fill='black')
        canvas.create_line((1175, 150), (1175, canvas_height-170), width=4, fill='white')

        #curva esterna in basso a destra
        canvas.create_arc((825, canvas_height-50), (1175, canvas_height-290), style=tk.ARC, start=0, extent=-90, width=8, outline="black")
        canvas.create_arc((825, canvas_height-50), (1175, canvas_height-290), style=tk.ARC, start=0, extent=-90, width=4, outline="white")
        # canvas.create_oval((825, canvas_height-50), (1175, canvas_height-290), outline="black", width=2)

        #linea in basso esterna dritta
        canvas.create_line((270, canvas_height-50), (1000, canvas_height-50), width=8, fill='black')
        canvas.create_line((270, canvas_height-50), (1000, canvas_height-50), width=4, fill="white")

        #curva esterna in basso a sinistra
        canvas.create_arc((100, canvas_height-50), (450, canvas_height-290), style=tk.ARC, start=270, extent=-90, width=8, outline="black")
        canvas.create_arc((100, canvas_height-50), (450, canvas_height-290), style=tk.ARC, start=270, extent=-90, width=4, outline="white")
        # canvas.create_oval((50, 270), (400, 30), outline="black", width=2)

        #linea sinistra interna dritta
        canvas.create_line((100, 150), (100, canvas_height-170), width=8, fill='black')
        canvas.create_line((100, 150), (100, canvas_height-170), width=4, fill='white')

        #id scambio 1
        cambio1def  = canvas.create_arc((28, 270), (400, 70), style=tk.ARC, start=134, extent= 38, width=8, outline="red")
        canvas.create_arc((28, 270), (400, 70), style=tk.ARC, start=134, extent= 38, width=4, outline="white")
        # canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=180, extent=-90, width=4, outline="black")
        cambio1     = canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=156, extent=24, width=8, outline="black")
        canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=156, extent=24, width=4, outline="white")
        # canvas.create_oval((28, 270), (400, 70), outline="black", width=2)
        GUI.Turnouts['Cambio 1'][2] = cambio1def
        GUI.Turnouts['Cambio 1'][3] = cambio1
        # GUI.Turnouts['Cambio 1'].append(cambio1def)
        # GUI.Turnouts['Cambio 1'].append(cambio1)

        #id scambio 2
        cambio2     = canvas.create_arc((100, 270), (500, 30), style=tk.ARC, start=96, extent=84, width=8, outline="black")
        canvas.create_arc((100, 270), (500, 30), style=tk.ARC, start=96, extent=84, width=4, outline="white")

        cambio2def  = canvas.create_arc((68, 260), (475, 30), style=tk.ARC, start=84, extent=74, width=8, outline="red")
        canvas.create_arc((68, 260), (475, 30), style=tk.ARC, start=84, extent=74, width=4, outline="white")
        # canvas.create_oval((68, 270), (475, 30), outline="black", width=2)
        GUI.Turnouts['Cambio 2'][2] = cambio2def
        GUI.Turnouts['Cambio 2'][3] = cambio2
        # GUI.Turnouts['Cambio 2'].append(cambio2def)
        # GUI.Turnouts['Cambio 2'].append(cambio2)

        #id scambio 3
        cambio3     = canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=145, extent=100, width=8, outline="black")
        canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=145, extent=100, width=4, outline="white")

        cambio3def  = canvas.create_line((270, canvas_height-50), (470, canvas_height-50), width=8, fill='red')
        canvas.create_line((270, canvas_height-50), (470, canvas_height-50), width=4, fill='white')
        # canvas.create_oval((175, canvas_height-50), (1200, canvas_height-640), outline="black", width=2)
        GUI.Turnouts['Cambio 3'][2] = cambio3def
        GUI.Turnouts['Cambio 3'][3] = cambio3
        # GUI.Turnouts['Cambio 3'].append(cambio3def)
        # GUI.Turnouts['Cambio 3'].append(cambio3)


        #id scambio 4
        cambio4def  = canvas.create_line((470, canvas_height-50), (700, canvas_height-50), width=8, fill='red')
        canvas.create_line((470, canvas_height-50), (700, canvas_height-50), width=4, fill='white')
        GUI.Turnouts['Cambio 4'][2] = cambio4def
        # GUI.Turnouts['Cambio 4'].append(cambio4def)

        #id scambio 4/8
        cambio4     = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=226, extent=40, width=8, outline="black")
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=226, extent=40, width=4, outline="white")
        GUI.Turnouts['Cambio 4'][3] = cambio4
        # GUI.Turnouts['Cambio 4'].append(cambio4)
        # canvas.create_oval((250, canvas_height-50), (1200, canvas_height-600), outline="black", width=2)
        
        #id scambio 5
        cambio5  = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=19, extent=54, width=8, outline="black")
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=19, extent=54, width=4, outline="white")

        cambio5def = canvas.create_line((1175, 150), (1175, 267), width=8, fill='red')
        canvas.create_line((1175, 150), (1175, 267), width=4, fill='white')
        GUI.Turnouts['Cambio 5'][2] = cambio5def
        GUI.Turnouts['Cambio 5'][3] = cambio5
        # GUI.Turnouts['Cambio 5'].append(cambio5def)
        # GUI.Turnouts['Cambio 5'].append(cambio5)

        # canvas.create_oval((250, canvas_height-50), (1200, canvas_height-600), outline="black", width=2)
        
        #id scambio 6
        cambio6def  = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=73, extent=65, width=8, outline="red")
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=73, extent=65, width=4, outline="white")

        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=139, extent=88, width=8, outline="black")
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=139, extent=88, width=4, outline="white")
        GUI.Turnouts['Cambio 6'][2] = cambio6def
        # GUI.Turnouts['Cambio 6'].append(cambio6def)
        # canvas.create_oval((250, canvas_height-50), (1200, canvas_height-600), outline="black", width=2)
        
        
        #id scambio 6/7
        cambio7 = canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=68, extent=85, width=8, outline="black")
        canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=68, extent=85, width=4, outline="white")
        # Turnouts['Cambio 5'].append(cambio5def)
        GUI.Turnouts['Cambio 6'][3] = cambio7
        # GUI.Turnouts['Cambio 6'].append(cambio7)
        # canvas.create_oval((175, canvas_height-50), (1200, canvas_height-640), outline="black", width=2)

        #id scambio 7
        cambio7def  = canvas.create_arc((208, canvas_height-300), (900, canvas_height-546), style=tk.ARC, start=117, extent=50, width=8, outline="red")
        canvas.create_arc((208, canvas_height-300), (900, canvas_height-546), style=tk.ARC, start=117, extent=50, width=4, outline="white")
        # canvas.create_oval((210, canvas_height-300), (900, canvas_height-546), outline="black", width=2)
        GUI.Turnouts['Cambio 7'][2] = cambio7def
        GUI.Turnouts['Cambio 7'][3] = cambio7
        # GUI.Turnouts['Cambio 7'].append(cambio7def)
        # GUI.Turnouts['Cambio 7'].append(cambio7)

        #id scambio 8
        cambio8def  = canvas.create_arc((230, canvas_height-110), (900, canvas_height-563), style=tk.ARC, start=244, extent=237, width=8, outline="red")
        canvas.create_arc((230, canvas_height-110), (900, canvas_height-563), style=tk.ARC, start=244, extent=237, width=4, outline="white")
        GUI.Turnouts['Cambio 8'][2] = cambio8def
        GUI.Turnouts['Cambio 8'][3] = cambio4
        # GUI.Turnouts['Cambio 8'].append(cambio8def)
        # GUI.Turnouts['Cambio 8'].append(cambio4)
        # canvas.create_oval((230, canvas_height-110), (900, canvas_height-563), outline="black", width=2)
        
        # canvas = tk.Canvas(root, width=800, height=400, bg="white")
        # canvas.pack()
        

        #const = automatico
        #gestione dei pin ARDUINO
        if comandi_refactored.is_serial_port_available(""):
            if not GUI.variabili_chiusura["locomotive_circuit_var"]:
                GUI.variabili_chiusura["locomotive_circuit_var"] = True
                for i in range (self.nscambi):
                    i+=1
                    str = 'Cambio {}'.format(i)
                    if i == 3: 
                        comandi_refactored.crea_deviatoio(i,i+37) # va sul pin 40
                    elif i == 4:
                        comandi_refactored.crea_deviatoio(i,i+34) # va sul pin 38
                    else:
                        comandi_refactored.crea_deviatoio(i,i+40) # vanno nel loro pin corrispondente + 40 
                    GUI.Turnouts[str][1] = i

 

        # # Aggiungere la gestione del click del mouse sui label
        # cambi_label.bind("<Button-1>", lambda event: label_clicked(event, "Cambi"))
        # semafori_label.bind("<Button-1>", lambda event: label_clicked(event, "Semafori"))

        # # Funzione per gestire il click del mouse sui label
        # def label_clicked(event, label_text):
        #     print("Label cliccato:", label_text)

        # Eseguire il loop principale
        root.mainloop()