import tkinter as tk
from tkinter import ttk
import random
import comandi
import cam
import data
import utilities

'''

             __      __  _                _                           
        o O O\ \    / / (_)    _ _     __| |    ___   __ __ __  ___   
       o      \ \/\/ /  | |   | ' \   / _` |   / _ \  \ V  V / (_-<   
      TS__[O]  \_/\_/  _|_|_  |_||_|  \__,_|   \___/   \_/\_/  /__/_  
     {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
    ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'
'''
"""
     
    SHORTCUTS 
    
    Queste 2 sono utilizzate da tutte le finestra della classe windows, ad esclusione della pagina circuit window che utilizza le sue personalizzate.

        self.locomotive_window.bind('<Return>', lambda event: {Bottone})
        Invio -> Tramite il tasto invio e come se schiaccisassi il tasto salva

        self.locomotive_window.bind("<Escape>", lambda event: utilities.on_close(self.locomotive_window,"{Nome finestra}"))
        Esc -> Puoi schiacciare il tasto esc per chiudere la finestra
        
    Inoltre la finestra relativa ai settingsRFID dispone di un tasto particolare in piu per effettuare il refresh.

        self.locomotive_window.bind("<KeyPress-r>", lambda event: refresh())
        
"""
#Funzione che gestisce la logica della pagine di creazione locomotive
def creation_window(locomotive_window,GUI):

    def save_locomotive():

        name            = name_entry.get()
        loco_id         = loco_id_entry.get()
        color           = var_color.get()

        controllo_loco  = len(data.locomotives_data)<data.max_loco #Controllo per vedere che il numero delle locomotive non sia al limite

        #controllo sugli input
        if name == "" or not loco_id.isdigit() or int(loco_id)==0 :
            utilities.show_error_box(data.Textlines[24],locomotive_window,"")

        elif len(name)>data.max_length_name or int(loco_id)>data.max_size_loco_id:
            utilities.show_error_box(data.Textlines[25],locomotive_window,"")
        elif data.variabili_apertura["locomotive_RFID_var"] and len(data.locomotives_data) == data.max_loco_auto:
            utilities.show_error_box(data.Textlines[67],locomotive_window,"")
        else:
            #controllo se esistono dei buchi tra gli ID
            if len(data.locomotives_data) == 0:
                id = 1
            else: 
                id = data.locomotives_data[-1]['ID'] +1
            
            #controlli per vedere se il nome e il locoid sono gia stati usati all'interno del vettore
            nome_unico = True
            Locoid_unico = True
        
            j=0
            if data.locomotives_data:
                while nome_unico:
                    nome_unico = name != data.locomotives_data[j]['Nome']
                    unicita_nome = nome_unico

                    j = j+1
                    if j == len(data.locomotives_data):  
                        nome_unico = False
                j=0
                #controllo per vedere se il nome è gia stato usato all'interno del vettore
                while Locoid_unico:
                    Locoid_unico = loco_id != data.locomotives_data[j]['LocoID']
                    unicita_id = Locoid_unico
                    j = j+1
                    if j == len(data.locomotives_data):  
                        Locoid_unico = False

            else: 
                unicita_nome    = True
                unicita_id      = True

            unicita = unicita_nome and unicita_id
            #Controllo sulla dimensione del circuito
            if unicita and controllo_loco:

                #se il colore non è selezionato, ne verra selezionato uno casualmente tra quelli nel vettore che verra rimosso dal vettore in quanto selezionato
                if color == "Default" :
                    color = random.choice([colore for colore in data.color_available if colore != "Default" ])
                data.color_available.remove(color)

                #definizione delle locomotive -Fase di test
                locomotive = {
                    'ID': id,
                    'Nome': name,
                    'LocoID': loco_id,
                    'Colore': color,
                    'Velocita':0,
                    'VelocitaM':0,
                    'Direzione':1,
                    'RFIDtag':"",
                    'Percorso':"",
                    'Ultimo_sensore':""
                }

                data.locomotives_data.append(locomotive)
                GUI.update_table()

                #setto la variabile relativa alla calibrazione dell RFID a False
                data.calibred = False
            else: 
                utilities.show_error_box(data.Textlines[26]+ f" {data.max_loco} " + data.Textlines[27],locomotive_window,"")

        #Controllo se la finestra ha avuto degli errori (reset) o no (chiude)
        if data.control_var_errore:
            reset_inputs()
            data.control_var_errore = False
        else:
            utilities.on_close(locomotive_window,"creation")

    #Funzione che resetta le entry
    def reset_inputs():
        name_entry.delete(0, tk.END)
        loco_id_entry.delete(0, tk.END)
        color_button.configure(text = "Default")

    # Creazione del form per la nuova locomotiva
    name_label = tk.Label(locomotive_window, text=data.Textlines[80]+":")
    name_label.pack()
    name_entry = tk.Entry(locomotive_window)
    name_entry.pack()

    #Constraint
    validate_input = locomotive_window.register(lambda P: P.isdigit() or P == '')

    loco_id_label = tk.Label(locomotive_window, text=data.Textlines[81])
    loco_id_label.pack()
    loco_id_entry = tk.Entry(locomotive_window, validate="key", validatecommand=(validate_input, '%P'))
    loco_id_entry.pack()

    color_label = tk.Label(locomotive_window, text=data.Textlines[82])
    color_label.pack()

#Il numero dei colori all'interno del vettore deve essere almeno pari al numero di locomotive massime del sistema, senno errore
    var_color = tk.StringVar(value=data.color_available[-1])
    color_button = ttk.Menubutton(locomotive_window,text=data.color_available[-1],width=19)
    color = tk.Menu(color_button, tearoff=0)
    color_button.pack()

    color_button["menu"] = color
    color.delete(0, "end")
    for item in data.color_available:
        color.add_radiobutton(
            label=data.colors[item],
            value=item,
            variable=var_color,
            command=lambda item = item :color_button.configure(text=data.colors[item])
            )
    
    style1 = ttk.Style()
    style1.configure('UniqueCustom.TMenubutton',padding=(),background="white")  #background ="#add8e6" 
    color_button.config(style='UniqueCustom.TMenubutton')

    save_button = tk.Button(locomotive_window, text=data.Textlines[44], command=save_locomotive)
    save_button.pack(pady=(10,0))
    

    name_entry.focus_set()
    #permette di avviare la funzione con il tasto invio
    locomotive_window.bind('<Return>', lambda event: save_locomotive())
    locomotive_window.bind("<Escape>", lambda event: utilities.on_close(locomotive_window,"creation"))
    
#Funzione che elimina le locomotive
def remove_window(locomotive_window,GUI):

    def remove_locomotive():
        name    = name_entry.get()
        id      = ID_entry.get()

        #controllo sugli input
        if name == "" or not id.isdigit():
            utilities.show_error_box(data.Textlines[24],locomotive_window,"")

        else:
            id = int(id)
            #controllo per vedere qual è l'ultimo ID
            if id <= data.locomotives_data[-1]['ID']:
                #prende l'indice dell'elememento in cui trova l'ID
                index = utilities.CalcolaIDtreno('ID',id)

                #controllo su se trova l'indice e il nome equaivale a quello inserito 
                if index is not None and name == data.locomotives_data[index]['Nome']:
                    
                    #Sett a True la variabile della calibrazione, il calcolo viene poi effettuato nell'update table
                    data.calibred = True
                    #prima di rimuovere la locomotiva, aggiungo il colore che le apparteneva al vettore dei colori disponibili
                    data.color_available.insert(0,data.locomotives_data[index]['Colore'])
                    data.locomotives_data.remove(data.locomotives_data[index])
                    
                    if data.locomotives_data:
                        #fa l'unbind del tasto - senza sort, funziona utilizzando index + 1 nel primo if e semplicemente index - 10 nel secondo 
                        if data.locomotives_data[-1]['ID'] < 10:
                            GUI.container.unbind("<KeyPress-{}>".format(data.locomotives_data[-1]['ID']))
                        else:
                            GUI.container.unbind("<Control-KeyPress-{}>".format(data.locomotives_data[-1]['ID'] - 10))
                    else:
                        GUI.container.unbind("<KeyPress-1>")

                    #Riordina il vettore dopo che si elimina un tizio - Non so se va benissimo, comunque oltre al pezzo sopra funziona tutto lo stesso
                    sequenza = list(range(1, len(data.locomotives_data )+1))
                    j=0
                    for item in data.locomotives_data:
                        item['ID'] = sequenza[j]
                        j += 1

                    GUI.update_table()
                else: 
                    utilities.show_error_box(data.Textlines[28],locomotive_window,"")

            else:
                utilities.show_error_box(data.Textlines[29],locomotive_window,"")


        #Controllo se la finestra ha avuto degli errori (reset) o no (chiude)
        if data.control_var_errore:
            reset_inputs()
            data.control_var_errore = False
        else:
            utilities.on_close(locomotive_window,"remove")

    #Resetta le entry
    def reset_inputs():
        name_entry.delete(0, tk.END)
        ID_entry.delete(0, tk.END)
        
    # Creazione del form per la nuova locomotiva
    name_label = tk.Label(locomotive_window, text=data.Textlines[80]+":")
    name_label.pack()
    name_entry = tk.Entry(locomotive_window)
    name_entry.pack()

    #Constraint
    validate_input = locomotive_window.register(lambda P: P.isdigit() or P == '')

    ID_label = tk.Label(locomotive_window, text=data.Textlines[83])
    ID_label.pack()
    ID_entry = tk.Entry(locomotive_window, validate="key", validatecommand=(validate_input, '%P'))
    ID_entry.pack()

    remove_button = tk.Button(locomotive_window, text=data.Textlines[48], command=remove_locomotive)
    remove_button.pack(pady=(10,0))

    name_entry.focus_set()
    #permette di avviare la funzione con il tasto invio
    locomotive_window.bind('<Return>', lambda event: remove_locomotive())
    locomotive_window.bind("<Escape>", lambda event: utilities.on_close(locomotive_window,"remove"))

def modify_window(locomotive_window,GUI):

    def modify_locomotive(): 
        name        = name_entry.get()
        id          = ID_entry.get()
        loco_id     = loco_id_entry.get()
        color       = var_color.get()

        #Assegnazione di default
        if loco_id == "": loco_id = "404"

        #controlli sugli input
        if int(loco_id)==0 or not id.isdigit() or int(id)==0 :
            utilities.show_error_box(data.Textlines[24],locomotive_window,"")

        elif len(name)>data.max_length_name or int(loco_id)>data.max_size_loco_id:
            utilities.show_error_box(data.Textlines[25],locomotive_window,"")

        else:
            id          = int(id)
            nome_unico  = True
            Locoid_unico = True

            j=0
            #prende l'indice dell'elememento in cui trova l'ID
            index_to_replace = utilities.CalcolaIDtreno('ID',id)
            if index_to_replace is not None:
                #se gli do una stringa vuota mi mette in automatico il noemche corrisponde all'ID
                if name != '':
                    #controllo per vedere se il nome è gia stato usato all'interno del vettore
                    while nome_unico:
                        nome_unico = name != data.locomotives_data[j]['Nome']
                        unicita_nome = nome_unico
                        j = j+1
                        if j == len(data.locomotives_data):  
                            nome_unico = False

                    if data.locomotives_data[index_to_replace]['Nome'] == name:
                        unicita_nome = True
                else:
                    name = data.locomotives_data[index_to_replace]['Nome']
                    unicita_nome = True
                j=0
                if loco_id != "404":
                    #controllo per vedere se il nome è gia stato usato all'interno del vettore
                    while Locoid_unico:
                        Locoid_unico = loco_id != data.locomotives_data[j]['LocoID']
                        unicita_id = Locoid_unico
                        j = j+1
                        if j == len(data.locomotives_data):  
                            Locoid_unico = False

                    if data.locomotives_data[index_to_replace]['LocoID'] == loco_id:
                        unicita_id = True
                else:
                    loco_id = data.locomotives_data[index_to_replace]['LocoID']
                    unicita_id = True

                
                unicita = unicita_nome and unicita_id
                #controlla che ci sia stata corrispondenza per l'indice e che il nome non sia gia stato utilizzato
                if unicita:
                    #Mantengo il tag assegnato prima, nel cso in cui sia stato assegnato
                    RFIDtag = data.locomotives_data[index_to_replace]['RFIDtag']

                    #Sostituisci il dizionario all'indice trovato con il nuovo dizionario
                    if data.locomotives_data[index_to_replace]['LocoID'] != loco_id:
                        if utilities.are_you_sure(data.Textlines[61],locomotive_window):
                            if color != "Default":
                                #prima di sostituire la locomotiva, aggiungo il colore che le apparteneva al vettore dei colori disponibili
                                data.color_available.insert(0,data.locomotives_data[index_to_replace]['Colore'])
                                data.color_available.remove(color)
                            else:
                                #assegno il colore che gia ha
                                color = data.locomotives_data[index_to_replace]['Colore']

                            new_dict = {'ID':id,
                                        'Nome':         name,
                                        'LocoID':       loco_id, 
                                        'Colore':       color, 
                                        'Velocita':     0, 
                                        'VelocitaM':    0, 
                                        'Direzione':    1,
                                        'RFIDtag':      RFIDtag
                                        }
                            if utilities.is_serial_port_available(data.serial_ports[0]):
                                comandi.change_id(data.locomotives_data[index_to_replace]['LocoID'],loco_id)

                            data.locomotives_data[index_to_replace] = new_dict
                    else:
                        if color != "Default":
                            #prima di sostituire la locomotiva, aggiungo il colore che le apparteneva al vettore dei colori disponibili
                            data.color_available.insert(0,data.locomotives_data[index_to_replace]['Colore'])
                            data.color_available.remove(color)
                        else:
                            #assegno il colore che gia ha
                            color = data.locomotives_data[index_to_replace]['Colore']
                        new_dict = {'ID':           id,
                                    'Nome':         name,
                                    'LocoID':       loco_id,
                                    'Colore':       color, 
                                    'Velocita':     0, 
                                    'VelocitaM':    0, 
                                    'Direzione':    1,
                                    'RFIDtag':      RFIDtag
                                    }
                        data.locomotives_data[index_to_replace] = new_dict
                    GUI.update_table()
                
                else:
                    utilities.show_error_box(data.Textlines[30],locomotive_window,"")
            else:
                utilities.show_error_box(data.Textlines[29],locomotive_window,"")

        #Controllo se la finestra ha avuto degli errori (reset) o no (chiude) 
        if data.control_var_errore:
            reset_inputs()
            data.control_var_errore = False
        else:
            utilities.on_close(locomotive_window,"modify")

    #Funzione che resetta gli entry
    def reset_inputs():
        name_entry.delete(0, tk.END)
        ID_entry.delete(0, tk.END)
        loco_id_entry.delete(0, tk.END)
        color_button.configure(text = "Default")
    
    #Constraint
    validate_input = locomotive_window.register(lambda P: P.isdigit() or P == '')

    # Creazione del form per la nuova locomotiva
    ID_label = tk.Label(locomotive_window, text=data.Textlines[84])
    ID_label.pack()
    ID_entry = tk.Entry(locomotive_window, validate="key", validatecommand=(validate_input, '%P'))
    ID_entry.pack()

    name_label = tk.Label(locomotive_window, text=data.Textlines[85]+" "+ data.Textlines[80]+":")
    name_label.pack()
    name_entry = tk.Entry(locomotive_window)
    name_entry.pack()

    loco_id_label = tk.Label(locomotive_window, text=data.Textlines[85]+" "+data.Textlines[81])
    loco_id_label.pack()
    loco_id_entry = tk.Entry(locomotive_window, validate="key", validatecommand=(validate_input, '%P'))
    loco_id_entry.pack()

    color_label = tk.Label(locomotive_window, text=data.Textlines[82])
    color_label.pack()

#Il numero dei colori all'interno del vettore deve essere almeno pari al numero di locomoitive massime del sistema, senno errore
    var_color = tk.StringVar(value=data.color_available[-1])
    color_button = ttk.Menubutton(locomotive_window,text="Default",width=19)
    color = tk.Menu(color_button, tearoff=0)
    color_button.pack()

    color_button["menu"] = color
    color.delete(0, "end")
    for item in data.color_available:
        color.add_radiobutton(
            label=data.colors[item],
            value=item,
            variable=var_color,
            command=lambda item = item :color_button.configure(text=data.colors[item])
            )
    
    # style1 = ttk.Style()
    # style1.configure('UniqueCustom.TMenubutton', borderwidth=1, relief="solid", padding=()) 
    color_button.config(style='UniqueCustom.TMenubutton')

    modify_button = tk.Button(locomotive_window, text=data.Textlines[49], command=modify_locomotive)
    modify_button.pack(pady=(10,0))

    ID_entry.focus_set()
    #permette di avviare la funzione con il tasto invio
    locomotive_window.bind('<Return>', lambda event: modify_locomotive())
    locomotive_window.bind("<Escape>", lambda event: utilities.on_close(locomotive_window,"modify"))

#Finestra che permette di controllare manualmente le locomotive
def control_window(locomotive_window,GUI,locomotiva,id_controllo):

    speed_label = tk.Label(locomotive_window, text=data.Textlines[86])
    speed_label.pack(pady=10)

    #creazione dello slider
    speed_slider = tk.Scale(locomotive_window, from_=0, to=100, orient=tk.HORIZONTAL)
    speed_slider.pack(pady=5)

    #funzione per settare lo slider alla velocita salvata
    speed_slider.set(data.locomotives_data[id_controllo]['Velocita'])
    GUI.check_control_button_state()

    root_control = tk.Frame(locomotive_window)
    root_control.pack(pady=5)

    #funzione per il throttle delle locomotive
    def throttle_command(direzione):
        print("QUI")
        data.var_velocita_tastiera = 0
        #prendere gli input da mandare al comando
        velocita        = speed_slider.get()
        id_loco         = utilities.CalcolaIDtreno('Nome',locomotiva)
        memoria         = data.locomotives_data[id_loco]['ID']
        ID              = data.locomotives_data[id_loco]['LocoID']
        #Impostare la velocita in memoria e la direzione
        data.locomotives_data[id_loco]['Velocita']  = velocita
        data.locomotives_data[id_loco]['Direzione'] = direzione
        #moltiplicazione per la costante e approssimazione
        velocita_effettiva = velocita*data.K_velocita
        if utilities.is_serial_port_available(data.serial_ports[0]):
            #mando il comando di throttle
            comandi.throttle(memoria,ID,round(velocita_effettiva),direzione)
        else: utilities.show_error_box(data.Textlines[21]+f"{data.serial_ports[0]} "+data.Textlines[22],locomotive_window,"main")

    #funzione per arrestare la locomotiva - setta lo slider a 0
    def stop_command():
        #prendere gli input da mandare al comando
        id_loco     = utilities.CalcolaIDtreno('Nome',locomotiva)
        memoria     = data.locomotives_data[id_loco]['ID']
        ID          = data.locomotives_data[id_loco]['LocoID']
        #Impostare la velocita in memoria e la direzione
        data.locomotives_data[id_loco]['VelocitaM']  = data.locomotives_data[id_loco]['Velocita']
        data.locomotives_data[id_loco]['Velocita']   = 0
        if utilities.is_serial_port_available(data.serial_ports[0]):
            comandi.STOP(memoria,ID)
            speed_slider.set(0)
        else: utilities.show_error_box(data.Textlines[21]+f"{data.serial_ports[0]} "+data.Textlines[22],locomotive_window,"main")
    
    #permette di selezionare il numero da tastiera
    def add_speed(numero):
        if data.var_velocita_tastiera == 0:
            #Intervallo di massimo 1 secondo
            locomotive_window.after(1000, set_slider)
        
        var = str(data.var_velocita_tastiera) + str(numero)
        if int(var) > data.max_velocita: var = data.max_velocita
        data.var_velocita_tastiera = int(var)
    
    #Imposta lo slider alla velocita inserita da tastiera e azzera la var di tastiera
    def set_slider():
        speed_slider.set(data.var_velocita_tastiera)
        data.var_velocita_tastiera = 0

    #creazione del form
    direction_label = tk.Label(root_control, text=data.Textlines[87])
    direction_label.pack(side=tk.TOP, pady=5)

    forward_button = tk.Button(root_control, text=data.Textlines[45],command=lambda:throttle_command(1))
    forward_button.pack(side=tk.LEFT, padx=5,pady=5)

    backward_button = tk.Button(root_control, text=data.Textlines[46],command=lambda:throttle_command(0))
    backward_button.pack(side=tk.LEFT, padx=5,pady=5)

    stop_button = tk.Button(locomotive_window, bg="#f08080", text=data.Textlines[47],command=stop_command)
    stop_button.pack(pady=5)

    #Comandi da tastiera
    locomotive_window.bind('<Up>',     lambda event: throttle_command(1))
    locomotive_window.bind('<Down>',   lambda event: throttle_command(0))
    locomotive_window.bind('<Return>', lambda event: stop_command())
    locomotive_window.bind("<Escape>", lambda event: utilities.on_close(locomotive_window,f"{id_controllo}"))
    #Creazione dei tasti da 0 a 9 per i numeri
    for i in range(10):
        locomotive_window.bind('<KeyPress-{}>'.format(i), lambda event, i=i: add_speed(i))
    
    #Fissa la finestra in primo piano
    locomotive_window.attributes("-topmost", True)

#Logica della finestra delle impostazioni della pagina principale
def settings_window(locomotive_window,GUI):

    def active_settings():
        centralina    = var_port0.get()
        rfid          = var_port1.get()
        max_loco      = max_loco_entry.get()
        port0_enabled = port0_checkbox_var.get()
        port1_enabled = port1_checkbox_var.get()

        #Assegnazione di default
        if max_loco == '' : max_loco = str(data.max_loco)
        
        #Amministratore
        data.root = True if int(max_loco) == 2005 and not data.root else False
        
        #controlli sugli input, non so bene che sistemare
        if rfid == centralina or int(max_loco) == 0:
            utilities.show_error_box(data.Textlines[24],locomotive_window,"")
        elif int(max_loco) > data.max_loco_standard:
            utilities.show_error_box(data.Textlines[31] + " {} ".format(data.max_loco_standard) + data.Textlines[123],locomotive_window,"")
        elif not utilities.port_exist(centralina) and port0_enabled:
            utilities.show_error_box(data.Textlines[32],locomotive_window,"")
        elif not utilities.port_exist(rfid) and port1_enabled:
            utilities.show_error_box(data.Textlines[33],locomotive_window,"")
        else:

            #Assegnazione e cast del valore in int
            if not centralina == "–": centralina = int(centralina)
            if not rfid == "-": rfid = int(rfid)
            max_loco = int(max_loco)

            #Controlla che il max loco non sia uguale a quello gia presente, nel caso in cui sia minore al numero di locomotive inserite,le cancella tutte
            if max_loco != data.max_loco:
                if data.locomotives_data and max_loco < len(data.locomotives_data):
                    if utilities.are_you_sure( data.Textlines[68] +"\n"+ data.Textlines[69] +"\n",locomotive_window):
                        #Rimuove tutte le locomotive, fino a che non si arriva al limite stabilito
                        for i in range(len(data.locomotives_data)-max_loco):
                            data.locomotives_data.remove(data.locomotives_data[-1])
                        data.max_loco = max_loco
                        GUI.update_table()
                else:
                    data.max_loco = max_loco

            #Si controlla che almeno una delle due sia diversa
            if centralina != data.serial_ports[0] or rfid != data.serial_ports[1]:

                #Cambiamo i rispettivi centralina e rfid
                utilities.set_port_var(centralina,rfid)

                # print(data.serial_ports)
                # print(data.SO)
                for port in ports_available:
                    if ports_name[port] != 'Sconosciuto':
                        data.serial_port_info[port][2] = ports_name[port]
                        print(ports_name[port])
                
                GUI.serial_port = data.serial_ports[0]
            #Aggiorniamo i valori relativi allo sblocco delle porte seriali dell'utente
            data.serial_port_info[data.serial_ports[0]][1]      = port0_enabled
            data.serial_port_info[data.serial_ports[1]][1]      = port1_enabled

        if data.root:
            #Amministratore
            utilities.show_info("ROOT BOSS alexein",locomotive_window)
            for i in data.serial_port_info:
                data.serial_port_info[i][1] = True
            locomotive_window.focus_set()

        #Controllo se la finestra ha avuto degli errori (reset) o no (chiude) 
        if data.control_var_errore:
            max_loco_entry.delete(0, tk.END)
            data.control_var_errore = False
        else:
            utilities.on_close(locomotive_window,"settings")

    #Serve a non permettere di selezionare il secondo checkbox se il primo non è selezionato
    def appoint_selection(checkbox):
        if checkbox == 0:
            if port0_checkbox_var.get():
                checkbox1.config(state='normal')
            else:
                checkbox1.config(state='disabled')
        else:
            if port1_checkbox_var.get():
                checkbox0.config(state='disabled')
            else:
                checkbox0.config(state='normal')
    
    def refresh():

        print("Refresh")
        for col in columns:
            tree.heading(col, text=col)
            
        for row in tree.get_children():
            tree.delete(row)
    
        # Riempimento della tabella con i dati delle porte seriali
        for port in ports_available:
            name = ports_name[port] if port not in data.serial_ports else data.serial_port_info[port][2]
            print(ports_name[port])
            tree.insert('', tk.END, values=(
                port,
                name
            ))

            
        for col in columns:
            width = 10 if col == "porta" else 150 
            tree.column(col, anchor='center', width=width)
        # tree.update()

    #Controlla le prime 10 porte se sono libere
    ports_available = []
    for i in range(data.port_range):
        if utilities.port_exist(i):
            ports_available.append(i)
            
        i+=1
    

    style = ttk.Style()
    style.configure('UniqueCustom.TMenubutton',padding=(),background="white") 

    centralina_label = tk.Label(locomotive_window, text=data.Textlines[88])
    centralina_label.grid(row=0, column=0, sticky=tk.W, padx=5)

#Il numro dei colori all'interno del vettore deve essere almeno pari al numero di locomoitive massime del sistema, senno errore
    centralina_port = data.serial_ports[0]
    var_port0 = tk.StringVar(value=centralina_port)
    port0_button = ttk.Menubutton(locomotive_window, text=centralina_port, width=8)
    port0 = tk.Menu(port0_button, tearoff=0)
    port0_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
    port0_button["menu"] = port0
    port0.delete(0, "end")
    for item in ports_available:
        port0.add_radiobutton(
            label=item,
            value=item,
            variable=var_port0,
            command=lambda:port0_button.configure(text=var_port0.get())
            )
    
    port0_button.config(style='UniqueCustom.TMenubutton')

    port0_checkbox_var = tk.BooleanVar()
    port0_checkbox_var.set(data.serial_port_info[data.serial_ports[0]][1])
    # Creazione della casella di controllo
    checkbox0 = tk.Checkbutton(locomotive_window,text=data.Textlines[57], variable=port0_checkbox_var, command = lambda: appoint_selection(0))
    checkbox0.grid(row=0, column=2, padx=5, sticky=tk.W)
    # checkbox0.select()

    RFID_label = tk.Label(locomotive_window, text=data.Textlines[89])
    RFID_label.grid(row=1, column=0, sticky=tk.W, padx=5)


#Il numro dei colori all'interno del vettore deve essere almeno pari al numero di locomoitive massime del sistema, senno errore
    RFID_port = data.serial_ports[1]
    var_port1 = tk.StringVar(value=RFID_port)
    port1_button = ttk.Menubutton(locomotive_window, text=RFID_port, width=8)
    port1 = tk.Menu(port0_button, tearoff=0)
    port1_button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
    port1_button["menu"] = port1
    port1.delete(0, "end")
    for item in ports_available:
        port1.add_radiobutton(
            label=item,
            value=item,
            variable=var_port1,
            command=lambda:port1_button.configure(text=var_port1.get())
            )
    
    port1_button.config(style='UniqueCustom.TMenubutton')

    port1_checkbox_var = tk.BooleanVar()
    port1_checkbox_var.set(data.serial_port_info[data.serial_ports[1]][1])
    # print(data.serial_port_info[data.serial_ports[1]][1])
    # Creazione della casella di controllo
    checkbox1 = tk.Checkbutton(locomotive_window,text=data.Textlines[57], variable=port1_checkbox_var, command = lambda: appoint_selection(1))
    checkbox1.grid(row=1, column=2, padx=5, sticky=tk.W)
    
    validate_input = locomotive_window.register(lambda P: P.isdigit() or P == '')

    # Terza coppia label-entry
    max_loco_label = tk.Label(locomotive_window, text=data.Textlines[90])
    max_loco_label.grid(row=2, column=0, sticky=tk.W, padx=5)  # Posiziona a sinistra
    max_loco_entry = tk.Entry(locomotive_window,width=10,validate="key", validatecommand=(validate_input, '%P'))
    max_loco_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)  # Posiziona a destra

    #Mostro il sistema operativo attuale, per far capire i path utilizzati
    SO_label = tk.Label(locomotive_window, text=data.Textlines[91])
    SO_label.grid(row=3, column=0, sticky=tk.W,padx=5)
    actual_SO_label = tk.Label(locomotive_window, text=data.SO + " " + data.architecture)
    actual_SO_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)
    
    port1_button.config(style='UniqueCustom.TMenubutton')

    #Creazione della tabella con le porte e i nomi dei device
    columns = ("porta","Dispositivo")
    tree = ttk.Treeview(locomotive_window, columns=columns, show='headings', height= 2)
    tree.grid(row=4, column=0, pady=(10, 0), padx=(10,0), sticky="nsew")

    #Ottengo il nome delle porte
    ports_name      = utilities.get_name_arduino(ports_available)

    print("I nomi dispnibiel")
    print(ports_available)
    print("I nomi sono")
    print(ports_name)
    refresh()

    settings_button = tk.Button(locomotive_window, text=data.Textlines[50], width=5,
                                command=active_settings)
    settings_button.grid(row=5, column=0, pady=(20, 0), padx=(180,0), sticky="nsew")

    #Attiviamo la selezione del 0 che è la standard
    appoint_selection(0)
    
    #Rende di nuovo visibile la finestra
    locomotive_window.deiconify()
    locomotive_window.grab_set()

    locomotive_window.bind('<Return>', lambda event: active_settings())
    locomotive_window.bind("<Escape>", lambda event: utilities.on_close(locomotive_window,"settings"))
    locomotive_window.bind("<FocusIn>",lambda event: max_loco_entry.focus_set())

#Logica della finestra delle impostazioni della pagina dei tag RFID
def RFID_window(locomotive_window,algo,circuit_window,GUI):
    
    # locomotive_window.info_window = None
    def show_page_info():

        locomotive_window1 = GUI.open_locomotive_window("info", data.Textlines[16], "600x400",locomotive_window)
        if locomotive_window1:

            info_text = (
                    "1. "+data.Textlines[116]+"\n\n"
                    " - "+data.Textlines[117]+"\n\n"
                    " - "+data.Textlines[118]+"\n\n\n"
                    "2. "+data.Textlines[119]+"\n\n"
                    " - "+data.Textlines[120]+"\n\n"
                    " - "+data.Textlines[121]
                )
                 
            label_title = tk.Label(locomotive_window1, text=data.Textlines[122], font=('Helvetica', 14, 'bold'))
            label_title.pack(pady=10)
            
            text = tk.Text(locomotive_window1, wrap='word', width=60, height=20)
            text.insert(tk.END, info_text)
            text.config(state='disabled')
            text.pack(padx=10, pady=5)
            
            locomotive_window1.transient(locomotive_window)

            locomotive_window1.protocol("WM_DELETE_WINDOW", lambda: locomotive_window1.destroy())
            locomotive_window1.bind('<Return>', lambda event: locomotive_window1.destroy())
            locomotive_window1.bind("<Escape>", lambda event: locomotive_window1.destroy())

            close_button = tk.Button(locomotive_window1, text=data.Textlines[43], command=locomotive_window1.destroy)
            close_button.pack(pady=10)

#Funzione che fa il refresh della tabella
    def refresh(creation):

        if not tree.winfo_exists():
            # Il widget non esiste più, non fare nulla
            return
        
        #Variabile che permette di eseguire una singola volta il refresh
        if not creation or not locomotive_window2.winfo_exists():
            utilities.update_circuit_table(columns,tree)
    
    def enable_circuitWindow():
        # circuit_window.attributes("-alpha", 1)
        circuit_window.grab_set()

    def open_locomotive_creation_window():
        global locomotive_window2

        locomotive_window2 = GUI.open_locomotive_window("creation", data.Textlines[12], "250x170",locomotive_window)

        if locomotive_window2:
            creation_window(locomotive_window2,GUI)
            locomotive_window2.bind("<Destroy>", lambda event: refresh(True))
            
        
    def active_settings():

        id      = RFID_entry.get()

        #Assegnazione di default - id = 0 non esiste percio dara errore
        if id == "": id = 0

        # Controllo che locmotives data non sia vuoto
        if data.locomotives_data:
            index_to_replace = utilities.CalcolaIDtreno('ID',int(id))
            # Controllo che l'elemento inserito esista
            if index_to_replace is not None:
                # controllare se tutti i sensori sono calibrati quando si invia
                if not data.sensor_response[0] == "_/_":
                    message = data.sensor_response[0] 
                    message = message.split("/")

                    LocotagRFID = utilities.CalcolaIDtreno('RFIDtag', message[1])
                    # Controllo che il messaggio non sia gia presente all'interno di quella locomotiva
                    if LocotagRFID is None:
                        data.calibred = True
                        algo.calibred_RFID(index_to_replace,message[1])
                        print("QUI")
                        data.sensor_response[0] = "_/_"
                        refresh(False)
                    else:
                        utilities.show_error_box(data.Textlines[34]+f" {LocotagRFID + 1}: {message[1]}",locomotive_window,"")
                else:
                    utilities.show_info(data.Textlines[62]+"\n"+ data.Textlines[63]+"\n"+data.Textlines[64],locomotive_window)
            else:
                utilities.show_error_box(data.Textlines[29],locomotive_window,"")
        else:
            # Potrei mettere l'altra finestra
            utilities.show_error_box(data.Textlines[35],locomotive_window,"")
        
        RFID_entry.focus_set()
        if data.control_var_errore:
            RFID_entry.delete(0, tk.END)
            data.control_var_errore = False
        # else:
        #     utilities.on_close(self.locomotive_window,"RFID")

    
    locomotive_window.image_info = utilities.process_image(GUI.image_info_path, 'resize', 35, 25)
    info_button = tk.Button(locomotive_window, image= locomotive_window.image_info, borderwidth=0, 
                            command=show_page_info)
    info_button.grid(row=0, column=0, pady=(10, 0), padx=(7,0),sticky=tk.W)

    tag_label = tk.Label(locomotive_window, text="", relief = tk.SUNKEN, width=10)
    tag_label.grid(row=0, column=0, pady=(10, 0), padx=(60,0),sticky=tk.W)
    tag_label.config(state="disabled")
    data.label = tag_label
    

    ADD_button = tk.Button(locomotive_window, text=data.Textlines[52], width=7,
                                command=open_locomotive_creation_window)
    ADD_button.grid(row=0, column=0, pady=(10, 0), padx=(0,7),sticky=tk.E)

    #Permette di inserire solo numeri
    validate_input = locomotive_window.register(lambda P: P.isdigit() or P == '')

    RFID_label = tk.Label(locomotive_window, text=data.Textlines[92])
    RFID_label.grid(row=2, column=0, sticky=tk.W,padx=5)  # Posiziona a sinistra
    #controllo sugli input,
    RFID_entry = tk.Entry(locomotive_window, width=5, validate="key", validatecommand=(validate_input, '%P'))
    RFID_entry.grid(row=2, column=0, pady=5, sticky=tk.E)  # Posiziona a destra


    columns = (data.Textlines[96], data.Textlines[95], data.Textlines[80])
    tree = ttk.Treeview(locomotive_window, columns=columns, show='headings')
    refresh(False)

    settings_button = tk.Button(locomotive_window, text=data.Textlines[51], width=7,
                                command=active_settings)
    settings_button.grid(row=3, column=0, pady=(10, 0), sticky="ns")

    locomotive_window.bind('<Return>', lambda event: active_settings())
    #GUI.open_locomotive_creation_window()
    locomotive_window.bind('<+>', lambda event: open_locomotive_creation_window())
    locomotive_window.bind('<i>', lambda event: show_page_info())
    locomotive_window.bind("<Escape>", lambda event: (enable_circuitWindow(),utilities.on_close(locomotive_window,"RFID")))
    locomotive_window.bind("<FocusIn>",   lambda event: RFID_entry.focus_set())

    #Salvo la pagina, mi serve per bloccare la pagina circuit
    GUI.locomotive_RFID_window = locomotive_window

    #Non permette altre azioni finche non chiudi la finestra, quando chiudi riabilita la circuit_window
    locomotive_window.protocol("WM_DELETE_WINDOW", lambda: (enable_circuitWindow(),utilities.on_close(locomotive_window,"RFID")))
    locomotive_window.grab_set()
'''
                ___      _                               _      _            __      __  _                _                    
        o O O  / __|    (_)      _ _    __     _  _     (_)    | |_          \ \    / / (_)    _ _     __| |    ___   __ __ __ 
       o      | (__     | |     | '_|  / _|   | +| |    | |    |  _|    ___   \ \/\/ /  | |   | ' \   / _` |   / _ \  \ V  V / 
      TS__[O]  \___|   _|_|_   _|_|_   \__|_   \_,_|   _|_|_   _\__|   |___|   \_/\_/  _|_|_  |_||_|  \__,_|   \___/   \_/\_/  
     {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|  
    ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'  
'''
"""
    SHORTCUTS

    Il tasto {esc} gestisce la chiusura della pagina che dovra anche controllare la chiusura dei thread dell'algoritmo, 
    Rendere disponibile il bottone dei settings e segnalare la sua chiusura

        self.locomotive_circuit_window.bind("<Escape>", lambda event: (utilities.on_close(self.locomotive_circuit_window,"circuit"),
                                                                                    self.container.algo.stop_algo(),
                                                                                    self.settings_button.config(state='normal')))
    -Manuale

        root.bind("<KeyPress-{}>".format(id)) -> Deviatoi nella pagina non automatica
        1 -> Cambio 1
        2 -> Cambio 2
        3 -> Cambio 3
        4 -> Cambio 4
        5 -> Cambio 5
        6 -> Cambio 6
        7 -> Cambio 7
        8 -> Cambio 8

        root.bind("<c>", lambda event: change_window(text,root))
        c -> Tasto che cambia la pagina da non automatica a automatica

    -Automatico

        root.bind("<c>", lambda event: change_window(text,root))
        c -> Tasto che cambia la pagina da automatica a non automatica

        root.bind("<s>", lambda event: (self.open_RFID_window(),root.attributes("-alpha", 0.5)))
        s -> Apre le impostazione dei sensori nella pagina automatica

        root.bind("<o>", lambda event: START())
        o -> Permette di avviare i sensori e dunque l'algoritmo

        root.bind("<v>", lambda event: change_color_webcam())
        v -> Permette di avviare la videocamera selezionata come predefinita dal pc
"""

class circuit_window:
 
    def __init__(self,locomotive_window,nscambi,container,GUI):
        self.locomotive_window = locomotive_window
    
        self.nscambi = nscambi
        #self.serial_port = data.serial_ports[0] -- Non permette dinamicità
        self.GUI = GUI
        self.container = container
        #richiamo del'oggetto algo
        self.algo = self.container.algo
        #creazione dell'oggetto camera
        self.camera = cam.Camera(self)
        #Flag che si utilizza per creare una sola volta i deviatoi
        self.flag = False

    #Funzione che permette di cambiare il colore del sensore quando passa un treno
    def change_Sensors(self,text,RFIDtag):
        id = utilities.CalcolaIDtreno('RFIDtag',RFIDtag)
        data.canvas_array[0].itemconfig(data.Sensors[text][3], fill=data.locomotives_data[id]['Colore'])
        data.canvas_array[0].after(2000, lambda:data.canvas_array[0].itemconfig(data.Sensors[text][3], fill=data.Sensors[text][4]))

    #Funzione per cambiare i deviatoi
    def change_Turnouts(self,text,button):
        #gestione grafica degli scambi
        print("ASD")
        if button == "":
            pass
        else:
            current_color = button.cget("background")
            if current_color == "#f08080":
                new_color = "#8fbc8f"
                new_text  =    "/"
            else:
                new_color = "#f08080"
                new_text  =    "|"
            # new_color = "#8fbc8f"   if current_color == "#f08080" else "#f08080"
            # new_text  =    "/"      if current_color == "#f08080" else "|"
            button.config(background=new_color,text=new_text)

        #Controlla che la porta relativa la centralina abbia il permesso e che esista il percorso
        if utilities.is_serial_port_available(data.serial_ports[0]):
            comandi.cambia_deviatoio(data.Turnouts[text][1])
        else:
            print("MOCC")
        #Cambio lo stato del Turnout, su questa logica si basa il colore rosso 
        self.change_color(text,data.Turnouts[text][0])
        data.Turnouts[text][0] = not data.Turnouts[text][0]
        
    #Funzione che ccambia il colore dello scambio in base a come è nel circuito
    def change_color(self,text,activated):
        if text not in {'Cambio 3', 'Cambio 4', 'Cambio 5'}:
            #Se il cambio è fromato da 2 curve
            if activated:
                data.canvas_array[0].itemconfig(data.Turnouts[text][2], outline="red")
                data.canvas_array[0].itemconfig(data.Turnouts[text][3], outline="black")   
            else:
                data.canvas_array[0].itemconfig(data.Turnouts[text][3], outline="red")
                data.canvas_array[0].itemconfig(data.Turnouts[text][2], outline="black")
        else:
            #Se il cambio è fromato da 1 curva ed un segmento
            if activated:
                data.canvas_array[0].itemconfig(data.Turnouts[text][2], fill="red")
                data.canvas_array[0].itemconfig(data.Turnouts[text][3], outline="black")
            else:
                data.canvas_array[0].itemconfig(data.Turnouts[text][3], outline="red")
                data.canvas_array[0].itemconfig(data.Turnouts[text][2], fill="black")

    #Funzione che apre la finestra delle impostazioni RFID
    def open_RFID_window(self):
        #GUI = self.GUI
        locomotive_window = self.GUI.open_locomotive_window("RFID", data.Textlines[17], "312x360",self.locomotive_window)
        if locomotive_window:
            RFID_window(locomotive_window,self.algo,self.locomotive_window,self.GUI)     

    #Funzione principale del circuito, qui si trova il canvas
    def open_circuit_window(self,automatico):
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
            current_color = self.webcam.cget("background")
            new_color = "green" if current_color == "blue" else "blue"
            new_text = data.Textlines[54] if current_color == "blue" else data.Textlines[53]
            
            if current_color == "blue" :
                
                #Controlla che la cam sia aperta ed esista, in caso contrario va a controllare
                if not self.camera.cam_exist:
                    self.camera.esiste()

                #Controlla che la cam sia aperta ed esista
                if self.camera.cam_exist:
                    self.webcam.config(background=new_color,text=new_text)
                    self.camera.cattura_webcam()
                else:
                    utilities.show_error_box(data.Textlines[36],self.locomotive_window,"main")
            else:
                self.webcam.config(background=new_color,text=new_text)
                self.camera.chiudi_finestra_webcam()

    # Funzione per creare un label con un checkbutton
        def create_label_with_button(canvas, x, y, text):
            label = canvas.create_text(x, y, text=data.Textlines[97] +" "+ text[-1], anchor=tk.W)  # Crea il testo sul canvas
            #crea tutti i bottoni dgli scambi
            if data.Turnouts[text][0]:
                color = "#8fbc8f"
                text_turnout = "/"
            else:
                color = "#f08080"
                text_turnout = "|"
            button = tk.Button(canvas, text=text_turnout, width=3, height=1,bg=color ,command=lambda: self.change_Turnouts(text,button))
            #Otteniamo il numero dello scambio
            id = text[-1]
            root.bind("<KeyPress-{}>".format(id), lambda event: self.change_Turnouts(text,button))
            canvas.create_window(x + 55, y + 0, window=button, anchor=tk.W)  # Crea il bottone vicino al testo sul canvas
            return label, button


    #Funzione che da inizio se possibile all'algoritmo, essa avvia i sensori
        def START():
            #gestione grafica degllo start dell'Auto version
            current_color = start_button.cget("background")            

            #Controllo sulla porta dei sensori
            if utilities.is_serial_port_available(data.serial_ports[1]):
                lenght = len(data.locomotives_data)
                if not lenght > 3: 
                    #Caso in cui deve accendersi
                    if current_color == "red":
                        #Se ci sono meno di due locomotive, manda un messaggio e avvisa che il processo non parte
                        if lenght not in [2,3]:
                            utilities.show_info(data.Textlines[67],self.locomotive_window)
                            root.focus_set()
                            # self.RFID_button.config(state='normal')
                            #Abilita il tasto
                        # elif not data.calibred: self.RFID_button.config(state='normal')
                        
                        if self.GUI.on_button.cget("background") != "red":
                            self.GUI.on_off()
                        new_color = "#00ff00"
                        self.algo.start_algo(self)
                        self.RFID_button.config(state='normal')
                        #Assegnazione del tasto
                        root.bind("<s>", lambda event: self.open_RFID_window())
                        check_control_button_state(True)
                    
                    else: #Caso in cui deve spegnersi
                        new_color = "red"
                        self.algo.stop_algo()
                        self.RFID_button.config(state='disabled')
                        #Disfuznione del tasto
                        root.unbind("<s>")
                        check_control_button_state(False)
    
                    start_button.config(background=new_color)
                else:
                    utilities.show_error_box(data.Textlines[67],self.locomotive_window,"main")
            else:
                utilities.show_error_box(data.Textlines[21]+f"{data.serial_ports[1]} "+data.Textlines[22] + ".\n"+ data.Textlines[37],self.locomotive_window,"main")
                data.serial_port_info[data.serial_ports[1]][0] = False

        def check_control_button_state(auto):
            if auto:
                self.locomotive_label.configure(text=data.Textlines[93])
                self.locomotive_window.grab_set()
                #Tolgo i bottoni che non posso schiacciare
                # for i in data.Turnouts:
                #     root.unbind("<KeyPress-{}>".format(i[-1]))
            else:
                self.locomotive_label.configure(text=data.Textlines[94])
                self.tag_label.configure(text="")
                self.tag_color.configure(background="SystemButtonFace")
                self.locomotive_window.grab_release()

        #---------CREAZIONE DELLA PAGINA---------

        root = self.locomotive_window

        canvas_width = root.winfo_width()
        canvas_height = root.winfo_height()-50

        frame = tk.Frame(root)
        frame.pack(anchor=tk.NW)

        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
        canvas.pack(side=tk.LEFT, expand=True)

        
        #tengo in memoria il canvas
        data.canvas_array[0] = canvas

        image_RFID_path = utilities.asset_path('controllo','png')
        image_RFID = utilities.process_image(image_RFID_path, 'resize', 40, 40)
        self.RFID_button = tk.Button(frame, image= image_RFID, borderwidth=0, 
                                        command=lambda:self.open_RFID_window())
        self.RFID_button.pack(side="left", padx=(10,5),pady=(5,0))
        self.RFID_button.config(state='disabled')

        image_power_path = utilities.asset_path('power_icon','png')
        image_power = utilities.process_image(image_power_path,'resize',35,35)
        start_button = tk.Button(frame, image=image_power,bg="red", 
                                    command=START)
        start_button.pack(padx=(10,5),side=tk.LEFT)
        root.bind("<o>", lambda event: START())

        # tabella che fa vedere cio che vedono i sensori
        self.tag_label = tk.Label(frame, text="", relief = tk.SUNKEN, width=10, height=2)
        self.tag_label.pack(side="left", padx=(5,0))
        self.tag_label.config(state="disabled")
        # data.label2 = tag_label
        
        self.tag_color = tk.Label(frame, text="", relief = tk.SUNKEN, width=2, height=2)
        self.tag_color.pack(side="left",padx=(0,5))
        self.tag_color.config(state="disabled")

        self.webcam = tk.Button(frame, text=data.Textlines[53], height=2,bg="blue" ,
                            command=lambda: change_color_webcam())
        self.webcam.pack(padx=5,side=tk.LEFT)
        root.bind("<v>", lambda event: change_color_webcam())

        self.locomotive_label = tk.Label(frame, text=data.Textlines[93])
        self.locomotive_label.pack(padx=(280,0),pady=10,side=tk.LEFT)
        
        canvas.create_text(10, 400, text="|3|", anchor=tk.W) 
        canvas.create_text(50, 400, text="|2|", anchor=tk.W) 
        canvas.create_text(870,370, text="|1|", anchor=tk.W) 

    #creazione dei bottoni per i deviatoi
        cambio1, button1 = create_label_with_button(canvas, 10, 60, "Cambio 1")
        cambio2, button2 = create_label_with_button(canvas, 200, canvas_height-630, "Cambio 2")
        cambio3, button3 = create_label_with_button(canvas, 375, canvas_height-20, "Cambio 3")
        cambio4, button4 = create_label_with_button(canvas, 675, canvas_height-20, "Cambio 4")
        cambio5, button5 = create_label_with_button(canvas, 1050, canvas_height-450, "Cambio 5")
        cambio6, button6 = create_label_with_button(canvas, 875, 60, "Cambio 6")
        cambio7, button7 = create_label_with_button(canvas, 150, canvas_height-500, "Cambio 7")
        cambio8, button8 = create_label_with_button(canvas, 415, canvas_height-150, "Cambio 8")
        
        # self.container.attributes("-alpha", 1)
       
        check_control_button_state(automatico)
        #----DISEGNO CIRCUITO---- link docs: https://www.pythontutorial.net/tkinter/tkinter-canvas/

        # Percorso dell'immagine originale
        stop_path       = utilities.asset_path('stop_treno','png')
        casetta_path    = utilities.asset_path('casetta','png')
        sensore_path    = utilities.asset_path('sensore_rfid','jpg')

        # binario_path = 'interfaccia_grafica\\assets\\binario.png'

        # Ridimensiona l'immagine utilizzando la funzione resize_image
        stop_treno = utilities.process_image(stop_path,'resize', 50, 50)
        casetta = utilities.process_image(casetta_path,'resize', 100, 100)
        # binario = process_image(binario_path,'resize', 100, 100)
        sensore = utilities.process_image(sensore_path,'resize', 40, 40)
        # sensore_rotated1 = utilities.process_image(sensore_path,'rotate', -90, 40, 40)  # Ruota a sinistra
        sensore_rotated2 = utilities.process_image(sensore_path,'rotate', -180, 40, 40)  # Ruota di 180
        sensore_rotated3 = utilities.process_image(sensore_path,'rotate', 90, 40, 40)  # Ruota a destra

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
        
        #Immagine sensore 1, con barra di passaggio
        canvas.create_image((137, 30),image=sensore)
        Sensore1 = canvas.create_rectangle(112, 4, 162, 12, fill=data.Sensors['Sensore 1'][4])
        data.Sensors['Sensore 1'][3] = Sensore1
        # canvas.itemconfig(RSensore1, fill="green")

        #Immagine sensore 2, con barra di passaggio
        canvas.create_image((350, 60),image=sensore_rotated2)
        Sensore2 = canvas.create_rectangle(325, 78, 375, 86, fill=data.Sensors['Sensore 2'][4])
        data.Sensors['Sensore 2'][3] = Sensore2
        # canvas.itemconfig(Sensore2, fill="green")

        #Immagine sensore 3, con barra di passaggio
        canvas.create_image((550, 682),image=sensore_rotated2)
        Sensore3 = canvas.create_rectangle(525, 700, 575, 708, fill=data.Sensors['Sensore 3'][4])
        data.Sensors['Sensore 3'][3] = Sensore3
        # canvas.itemconfig(Sensore3, fill="green")
        
        #Immagine sensore 4, con barra di passaggio
        canvas.create_image((900, 630),image=sensore)
        Sensore4 = canvas.create_rectangle(875, 604, 925, 612, fill=data.Sensors['Sensore 4'][4])
        data.Sensors['Sensore 4'][3] = Sensore4
        # canvas.itemconfig(Sensore4, fill="green")
        
        #Immagine sensore 5, con barra di passaggio
        canvas.create_image((1145, 400),image=sensore_rotated3)
        Sensore5 = canvas.create_rectangle(1119, 375, 1127, 425, fill=data.Sensors['Sensore 5'][4])
        data.Sensors['Sensore 5'][3] = Sensore5
        # canvas.itemconfig(Sensore5, fill="green")
        
        #Immagine sensore 6, con barra di passaggio
        canvas.create_image((950, 150),image=sensore_rotated2)
        Sensore6 = canvas.create_rectangle(925, 168, 975, 176, fill=data.Sensors['Sensore 6'][4])
        data.Sensors['Sensore 6'][3] = Sensore6
        # canvas.itemconfig(Sensore6, fill="green")

        #Immagine sensore 7, con barra di passaggio
        canvas.create_image((155, 300),image=sensore_rotated3)
        Sensore7 = canvas.create_rectangle(129, 275, 137, 325, fill=data.Sensors['Sensore 7'][4])
        data.Sensors['Sensore 7'][3] = Sensore7
        # canvas.itemconfig(Sensore7, fill="green")

        #Immagine sensore 8, con barra di passaggio
        canvas.create_image((390, 500),image=sensore)
        Sensore8 = canvas.create_rectangle(365, 474, 415, 482, fill=data.Sensors['Sensore 8'][4])
        data.Sensors['Sensore 8'][3] = Sensore8
        # canvas.itemconfig(Sensore8, fill="green")


        #linee sinistra con stop
        canvas.create_line((30, 155), (30, canvas_height-160), width=8, fill='black')
        canvas.create_line((70, 150), (70, canvas_height-60), width=8, fill='black')
        canvas.create_line((30, 155), (30, canvas_height-160), width=4, fill='white')
        canvas.create_line((70, 150), (70, canvas_height-60), width=4, fill='white')

        #linea in alto dritta
        canvas.create_line((293, 31), (1000, 31), width=8, fill='black')
        canvas.create_line((293, 31), (1000, 31), width=4, fill='white')
        
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

        #Curva interna tra scambio 6 e X
        cambio6def  = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=100, extent=40, width=8, outline="black")
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=100, extent=40, width=4, outline="white")

        #Curva interna tra scambio 8 e 7
        canvas.create_arc((230, canvas_height-110), (900, canvas_height-563), style=tk.ARC, start=274, extent=207, width=8, outline="black")
        canvas.create_arc((230, canvas_height-110), (900, canvas_height-563), style=tk.ARC, start=244, extent=237, width=4, outline="white")

        #Curva interna tra scambio 8 e X
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=139, extent=88, width=8, outline="black")
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=139, extent=88, width=4, outline="white")

        #Curva interna tra scambio 3 e 2
        cambio3     = canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=145, extent=100, width=8, outline="black")
        canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=145, extent=100, width=4, outline="white")

        #Curva tra scambio 5 e 6
        cambio5  = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=36, extent=37, width=8, outline="black")
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=36, extent=37, width=4, outline="white")

        #id scambio 1 - Impostazioni di memoria
        if data.Turnouts['Cambio 1'][0]:
            cambio1def  = canvas.create_arc((28, 270), (400, 70), style=tk.ARC, start=134, extent= 38, width=8, outline="black")
            canvas.create_arc((28, 270), (400, 70), style=tk.ARC, start=134, extent= 38, width=4, outline="white")
            # canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=180, extent=-90, width=4, outline="black")
            cambio1     = canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=156, extent=24, width=8, outline="red")
            canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=156, extent=24, width=4, outline="white")
        else:
            cambio1def  = canvas.create_arc((28, 270), (400, 70), style=tk.ARC, start=134, extent= 38, width=8, outline="red")
            canvas.create_arc((28, 270), (400, 70), style=tk.ARC, start=134, extent= 38, width=4, outline="white")
            # canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=180, extent=-90, width=4, outline="black")
            cambio1     = canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=156, extent=24, width=8, outline="black")
            canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=156, extent=24, width=4, outline="white")
        # canvas.create_oval((28, 270), (400, 70), outline="black", width=2)
        data.Turnouts['Cambio 1'][2] = cambio1def
        data.Turnouts['Cambio 1'][3] = cambio1

        #id scambio 2 - Impostazioni di memoria
        if data.Turnouts['Cambio 2'][0]:
            cambio2     = canvas.create_arc((100, 270), (500, 30), style=tk.ARC, start=96, extent=84, width=8, outline="red")
            canvas.create_arc((100, 270), (500, 30), style=tk.ARC, start=96, extent=84, width=4, outline="white")

            cambio2def  = canvas.create_arc((68, 260), (475, 30), style=tk.ARC, start=84, extent=74, width=8, outline="black")
            canvas.create_arc((68, 260), (475, 30), style=tk.ARC, start=84, extent=74, width=4, outline="white")
        else:
            cambio2     = canvas.create_arc((100, 270), (500, 30), style=tk.ARC, start=96, extent=84, width=8, outline="black")
            canvas.create_arc((100, 270), (500, 30), style=tk.ARC, start=96, extent=84, width=4, outline="white")

            cambio2def  = canvas.create_arc((68, 260), (475, 30), style=tk.ARC, start=84, extent=74, width=8, outline="red")
            canvas.create_arc((68, 260), (475, 30), style=tk.ARC, start=84, extent=74, width=4, outline="white")
        # canvas.create_oval((68, 270), (475, 30), outline="black", width=2)
        data.Turnouts['Cambio 2'][2] = cambio2def
        data.Turnouts['Cambio 2'][3] = cambio2

        #id scambio 3 - Impostazioni di memoria
        if data.Turnouts['Cambio 3'][0]:
            cambio3     = canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=215, extent=30, width=8, outline="red")
            canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=215, extent=30, width=4, outline="white")

            cambio3def  = canvas.create_line((270, canvas_height-50), (470, canvas_height-50), width=8, fill='black')
            canvas.create_line((270, canvas_height-50), (470, canvas_height-50), width=4, fill='white')
        else:
            cambio3     = canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=215, extent=30, width=8, outline="black")
            canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=215, extent=30, width=4, outline="white")

            cambio3def  = canvas.create_line((270, canvas_height-50), (470, canvas_height-50), width=8, fill='red')
            canvas.create_line((270, canvas_height-50), (470, canvas_height-50), width=4, fill='white')
        # canvas.create_oval((175, canvas_height-50), (1200, canvas_height-640), outline="black", width=2)
        data.Turnouts['Cambio 3'][2] = cambio3def
        data.Turnouts['Cambio 3'][3] = cambio3


        #id scambio 4 - Impostazioni di memoria
        if data.Turnouts['Cambio 4'][0]:
            cambio4def  = canvas.create_line((470, canvas_height-50), (700, canvas_height-50), width=8, fill='black')
            canvas.create_line((470, canvas_height-50), (700, canvas_height-50), width=4, fill='white')

            cambio4     = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=246, extent=20, width=8, outline="red")
            canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=226, extent=40, width=4, outline="white")
        else:
            cambio4def  = canvas.create_line((470, canvas_height-50), (700, canvas_height-50), width=8, fill='red')
            canvas.create_line((470, canvas_height-50), (700, canvas_height-50), width=4, fill='white')

            cambio4     = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=246, extent=20, width=8, outline="black")
            canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=226, extent=40, width=4, outline="white")
        

        data.Turnouts['Cambio 4'][2] = cambio4def
        data.Turnouts['Cambio 4'][3] = cambio4
        # GUI.Turnouts['Cambio 4'].append(cambio4)
        # canvas.create_oval((250, canvas_height-50), (1200, canvas_height-600), outline="black", width=2)
        
        #id scambio 5 - Impostazioni di memoria
        if data.Turnouts['Cambio 5'][0]:
            cambio5  = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=19, extent=27, width=8, outline="red")
            canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=19, extent=27, width=4, outline="white")

            cambio5def = canvas.create_line((1175, 150), (1175, 267), width=8, fill='black')
            canvas.create_line((1175, 150), (1175, 267), width=4, fill='white')
        else:
            cambio5  = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=19, extent=27, width=8, outline="black")
            canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=19, extent=27, width=4, outline="white")

            cambio5def = canvas.create_line((1175, 150), (1175, 267), width=8, fill='red')
            canvas.create_line((1175, 150), (1175, 267), width=4, fill='white')
        data.Turnouts['Cambio 5'][2] = cambio5def
        data.Turnouts['Cambio 5'][3] = cambio5

        # canvas.create_oval((250, canvas_height-50), (1200, canvas_height-600), outline="black", width=2)
        
        #id scambio 6 - Impostazioni di memoria
        if data.Turnouts['Cambio 6'][0]:
            cambio6def  = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=73, extent=45, width=8, outline="black")
            canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=73, extent=45, width=4, outline="white")

            cambio6 = canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=68, extent=43, width=8, outline="red")
            canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=68, extent=85, width=4, outline="white")
        else:
            cambio6def  = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=73, extent=45, width=8, outline="red")
            canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=73, extent=45, width=4, outline="white")

            cambio6 = canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=68, extent=43, width=8, outline="black")
            canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=68, extent=85, width=4, outline="white")

        data.Turnouts['Cambio 6'][2] = cambio6def
        data.Turnouts['Cambio 6'][3] = cambio6
        # GUI.Turnouts['Cambio 6'].append(cambio6def)
        # canvas.create_oval((250, canvas_height-50), (1200, canvas_height-600), outline="black", width=2)
        
        
        #id scambio 7 - Impostazioni di memoria
        if data.Turnouts['Cambio 7'][0]:
            cambio7 = canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=111, extent=42, width=8, outline="red")
            canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=68, extent=85, width=4, outline="white")

            cambio7def  = canvas.create_arc((208, canvas_height-300), (900, canvas_height-546), style=tk.ARC, start=117, extent=50, width=8, outline="black")
            canvas.create_arc((208, canvas_height-300), (900, canvas_height-546), style=tk.ARC, start=117, extent=50, width=4, outline="white")
        else:
            cambio7 = canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=111, extent=42, width=8, outline="black")
            canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=68, extent=85, width=4, outline="white")

            cambio7def  = canvas.create_arc((208, canvas_height-300), (900, canvas_height-546), style=tk.ARC, start=117, extent=50, width=8, outline="red")
            canvas.create_arc((208, canvas_height-300), (900, canvas_height-546), style=tk.ARC, start=117, extent=50, width=4, outline="white")
            # canvas.create_oval((210, canvas_height-300), (900, canvas_height-546), outline="black", width=2)

        data.Turnouts['Cambio 7'][2] = cambio7def
        data.Turnouts['Cambio 7'][3] = cambio7

        #id scambio 8 - Impostazioni di memoria
        if data.Turnouts['Cambio 8'][0]:
            cambio8def  = canvas.create_arc((230, canvas_height-110), (900, canvas_height-563), style=tk.ARC, start=244, extent=30, width=8, outline="black")
            canvas.create_arc((230, canvas_height-110), (900, canvas_height-563), style=tk.ARC, start=244, extent=30, width=4, outline="white")

            cambio8     = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=225, extent=21, width=8, outline="red")
            canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=225, extent=21, width=4, outline="white")
        else:
            cambio8def  = canvas.create_arc((230, canvas_height-110), (900, canvas_height-563), style=tk.ARC, start=244, extent=30, width=8, outline="red")
            canvas.create_arc((230, canvas_height-110), (900, canvas_height-563), style=tk.ARC, start=244, extent=30, width=4, outline="white")     

            cambio8     = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=225, extent=21, width=8, outline="black")
            canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=225, extent=21, width=4, outline="white")   
        data.Turnouts['Cambio 8'][2] = cambio8def
        data.Turnouts['Cambio 8'][3] = cambio8
        # canvas.create_oval((230, canvas_height-110), (900, canvas_height-563), outline="black", width=2)

        
        #gestione dei pin ARDUINO
        if utilities.is_serial_port_available(data.serial_ports[0]):
            #Se la finestra è chiusa allora crea i deviatoi, serve a non creare i deviatoi ogno volta che si switcha da auto a manuale
            if not self.flag:
                #Comando che accende il led di controllo
                comandi.crea_deviatoio(36,36)
                # comandi.crea_deviatoio(1,41)
                # database.Turnouts['Cambio 1'][1] = 1
                for i in range (self.nscambi):
                    i+=1
                    str = 'Cambio {}'.format(i)
                    if i == 3: 
                        comandi.crea_deviatoio(i,i+37) # va sul pin 40
                    elif i == 4:
                        comandi.crea_deviatoio(i,i+34) # va sul pin 38
                    else:
                        comandi.crea_deviatoio(i,i+40) # vanno nel loro pin corrispondente + 40 
                    
                    data.Turnouts[str][1] = i
        
        #Rende la finestra visibile quando ha finito di crearsi
        if not self.flag: 
            self.locomotive_window.deiconify()
            self.flag = True
            
        # Eseguire il loop principale
        root.mainloop()