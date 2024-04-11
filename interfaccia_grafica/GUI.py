'''
This file represent the GUI of the program, with this lines of code you could be able to manage all the data related to the locomotives.
You can add, remove, modify locomotives data and also you can open the other windows in order to perform the system.
'''

import tkinter as tk
from tkinter import ttk
import random
import function
import circuito
import comandi
import algorithm

#from tkfontawesome import icon_to_image
# locomotives_data =      []           # Lista per salvare i dati delle locomotive
locomotive_names =      []           # Lista per i nomi delle locomotive
max_loco         =       3           # Numero max di locomotive che il sistema lavora
max_length_name  =      20           # Numero max di caratteri che il nome puo avere
max_size_loco_id =   10293           # Numero max dell'indirizzo che si puo dare ad una locomotiva
K_velocita       = 126/100           # Costante basata sulla velocita massima possibile di una locomotiva (0-126)

#creazione delle variabili delle pagine
locomotive_creation_window  =   None
locomotive_remove_window    =   None
locomotive_modify_window    =   None
locomotive_circuit_window   =   None
locomotive_control_window   =   []

#Inserimento di max finestre nel locomotive control window in base al max_loco
for i in range(max_loco):
    locomotive_control_window.append(None)
    function.variabili_chiusura["locomotive_control_var"].append(False)

#per lo stile del menu a tendina, serve a togliere la freccetta
indicatoron = [('Menubutton.border',
  {'sticky': 'nswe',
   'children': [('Menubutton.focus',
     {'sticky': 'nswe',
      'children': [
       ('Menubutton.padding',
        {'expand': '1',
         'sticky': 'we',
         'children': [('Menubutton.label',
           {'side': 'left', 'sticky': ''})]})]})]})]


#funzione per salvare locomotive nel vettore sotto forma di dizionari
def open_locomotive_creation_window():
    global locomotive_creation_window
    function.variabili_chiusura["locomotive_creation_var"] = False
    if locomotive_creation_window is None or not locomotive_creation_window.winfo_exists():
        #,"close_/locomotive_creation_window"
        #creazione finestra
        locomotive_creation_window = tk.Toplevel(root)
        locomotive_creation_window.title("Creazione Locomotiva")
        locomotive_creation_window.geometry("250x170")
        #per disabilitare il ridimensionamento
        locomotive_creation_window.resizable(False, False)

        # Funzione per gestire il salvataggio dei dati inseriti nel form
        def save_locomotive():
            global locomotive_names
            global id
            name            = name_entry.get()
            loco_id         = loco_id_entry.get()
            color           = var_color.get()
            #se il colore non è selezionato, ne verra selezionato uno casualmente tra quelli nel vettore che verra rimosso dal vettore in quanto selezionato
            if color == "Default":
                color = random.choice([colore for colore in function.color_available if colore != "Default" ])
            function.color_available.remove(color)
            controllo_loco  = len(function.locomotives_data)<max_loco #Controllo per vedere che il numero delle locomotive non sia al limite

            #controllo sugli input
            if name == "" or not loco_id.isdigit() or color.isdigit() or int(loco_id)==0:
                function.show_error_box("Input inseriti incorrettamente","close_window/locomotive_creation_var","")
                
                #open_locomotive_creation_window()
            elif len(name)>max_length_name or int(loco_id)>max_size_loco_id:
                function.show_error_box("Hai superato il limite di lunghezza/grandezza","close_window/locomotive_creation_var","")
                #open_locomotive_creation_window()
            else:
                
                #controllo se esistono dei buchi tra gli ID
                if len(function.locomotives_data) == 0:
                    id = 1
                else: 
                    id = function.locomotives_data[-1]['ID'] +1
                

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
                if function.locomotives_data:
                    while nome_unico:
                        nome_unico = name != function.locomotives_data[j]['Nome']
                        unicita = nome_unico

                        j = j+1
                        if j == len(function.locomotives_data):  
                            nome_unico = False
                else: 
                    unicita=True
                
                #Controllo sulla dimensione del circuito
                if unicita and controllo_loco:
                    function.locomotives_data.append(locomotive)
                    update_table()
                    #Aggiornamento dei bottoni a seconda degli input
                    locomotive_names = [locomotive['Nome'] for locomotive in function.locomotives_data]

                else: 
                    function.show_error_box("Non puoi inserire piu di una locomotiva con lo stesso nome (max 3 locomotive per questo circuito)","close_window/locomotive_creation_var","")
                    # open_locomotive_creation_window()

            #chiude la finestra 
            function.on_close(locomotive_creation_window,-1)
            #controlla che nel vettore ci sia ancora spazio e che la var di chiusura sia True
            if  function.variabili_chiusura["locomotive_creation_var"] and controllo_loco:
                locomotive_creation_window.after(0,open_locomotive_creation_window())
            #locomotive_creation_window.destroy()
        


        # Creazione del form per la nuova locomotiva
        name_label = tk.Label(locomotive_creation_window, text="Nome:")
        name_label.pack()
        name_entry = tk.Entry(locomotive_creation_window)
        name_entry.pack()

        loco_id_label = tk.Label(locomotive_creation_window, text="LocoID:")
        loco_id_label.pack()
        loco_id_entry = tk.Entry(locomotive_creation_window)
        loco_id_entry.pack()

        color_label = tk.Label(locomotive_creation_window, text="Colore*:")
        color_label.pack()

#Il numero dei colori all'interno del vettore deve essere almeno pari al numero di locomoitive massime del sistema, senno errore
        var_color = tk.StringVar(value=function.color_available[-1])
        color_button = ttk.Menubutton(locomotive_creation_window,text="Default",width=19)
        color = tk.Menu(color_button, tearoff=0)
        color_button.pack()

        color_button["menu"] = color
        color.delete(0, "end")
        for item in function.color_available:
            color.add_radiobutton(
                label=item,
                value=item,
                variable=var_color,
                command=lambda:color_button.configure(text=var_color.get())
                )
        
        style1 = ttk.Style()
        style1.configure('UniqueCustom.TMenubutton',padding=(),background="white")  #background ="#add8e6" 
        color_button.config(style='UniqueCustom.TMenubutton')

        save_button = tk.Button(locomotive_creation_window, text="Salva", command=save_locomotive)
        save_button.pack(pady=(10,0))

        locomotive_creation_window.bind('<Return>', lambda event: save_locomotive())
        locomotive_creation_window.protocol("WM_DELETE_WINDOW", lambda:function.on_close(locomotive_creation_window,-1))
    else:
        function.show_error_box("Non puoi aprire un altra pagina","focus_page/_",locomotive_creation_window)
        #locomotive_creation_window.focus_set()
    
    
#Funzione per pagina per rimuovere una locomotiva dalla memoria
def open_locomotive_remove_window():
    global locomotive_remove_window
    function.variabili_chiusura["locomotive_remove_var"] = False
    if locomotive_remove_window is None or not locomotive_remove_window.winfo_exists():
        #creazione finestra del rimuovi
        locomotive_remove_window = tk.Toplevel(root)
        locomotive_remove_window.title("Rimozione Locomotiva")
        locomotive_remove_window.geometry("250x150")
        #per disabilitare il ridimensionamento
        locomotive_remove_window.resizable(False, False)
        locomotive_remove_window.transient(root)
        

        def remove_locomotive():
            name    = name_entry.get()
            id      = ID_entry.get()
            # print(CalcolaIDtreno("Nome",name))
            # 
            #controllo sugli input
            if name == "" or not id.isdigit() or int(id) < 1:
                function.show_error_box("Input inseriti incorrettamente","close_window/locomotive_remove_var","")
                #open_locomotive_remove_window()
            else:
                id = int(id)
                #controllo per vedere qual è l'ultimo ID
                if id <= function.locomotives_data[-1]['ID']:
                    #prende l'indice dell'elememento in cui trova l'ID
                    index = function.CalcolaIDtreno('ID',id)

                    #controllo su se trova l'indice e il nome equaivale a quello inserito 
                    if index is not None and name == function.locomotives_data[index]['Nome']:
                        #prima di rimuovere la locomotiva, aggiungo il colore che le apparteneva al vettore dei colori disponibili
                        function.color_available.insert(0,function.locomotives_data[index]['Colore'])
                        function.locomotives_data.remove(function.locomotives_data[index])
                        update_table()
                        
                    else: 
                        function.show_error_box("Id e nome non coincidono con nessuna locomotiva registrata","close_window/locomotive_remove_var","")
                        #open_locomotive_remove_window()
                else:
                    function.show_error_box("ID non valido","close_window/locomotive_remove_var","")
                    #open_locomotive_remove_window()
            #chiude la finestra 
            function.on_close(locomotive_remove_window,-1)
            if  function.variabili_chiusura["locomotive_remove_var"]:
                locomotive_remove_window.after(20,open_locomotive_remove_window())
            #locomotive_remove_window.destroy()

            
        # Creazione del form per la nuova locomotiva
        name_label = tk.Label(locomotive_remove_window, text="Nome:")
        name_label.pack()
        name_entry = tk.Entry(locomotive_remove_window)
        name_entry.pack()

        ID_label = tk.Label(locomotive_remove_window, text="ID:")
        ID_label.pack()
        ID_entry = tk.Entry(locomotive_remove_window)
        ID_entry.pack()

        remove_button = tk.Button(locomotive_remove_window, text="Rimuovi", command=remove_locomotive)
        remove_button.pack()

        locomotive_remove_window.bind('<Return>', lambda event: remove_locomotive())
        locomotive_remove_window.protocol("WM_DELETE_WINDOW", lambda: function.on_close(locomotive_remove_window,-1))
    else:   
        function.show_error_box("Non puoi aprire un altra pagina","focus_page/_",locomotive_remove_window)

#Funzione per pagina per modificare le locomotive in memoria
def open_locomotive_modify_window():
    global locomotive_modify_window
    function.variabili_chiusura["locomotive_modify_var"] = False
    if locomotive_modify_window is None or not locomotive_modify_window.winfo_exists():
        #creazione finestra per modificare loco
        locomotive_modify_window = tk.Toplevel(root)
        locomotive_modify_window.title("Modifica Locomotiva")
        locomotive_modify_window.geometry("300x200")
        #per disabilitare il ridimensionamento
        locomotive_modify_window.resizable(False, False)


        def modify_locomotive(): # Qui puoi gestire i dati inseriti nel form (es. salvataggio, stampa, etc.)
            name        = name_entry.get()
            id          = ID_entry.get()
            loco_id     = loco_id_entry.get()
            color       = var_color.get()

            #controlli sugli input
            if not loco_id.isdigit() or not id.isdigit() or int(loco_id)==0 or int(id)==0:
                function.show_error_box("Input inseriti incorrettamente","close_window/locomotive_modify_var","")
                #open_locomotive_modify_window()
            elif len(name)>max_length_name or int(loco_id)>max_size_loco_id:
                function.show_error_box("Hai superato il limite di lunghezza/grandezza","close_window/locomotive_modify_var","")
            else:
                id          = int(id)
                nome_unico  = True
                j=0
                #prende l'indice dell'elememento in cui trova l'ID
                index_to_replace = function.CalcolaIDtreno('ID',id)
                if index_to_replace is not None:
                    #se gli do una stringa vuota mi mette in automatico il noemche corrisponde all'ID
                    if name != '':
                        #controllo per vedere se il nome è gia stato usato all'interno del vettore
                        while nome_unico:
                            nome_unico = name != function.locomotives_data[j]['Nome']
                            unicita = nome_unico
                            j = j+1
                            if j == len(function.locomotives_data):  
                                nome_unico = False

                        if function.locomotives_data[index_to_replace]['Nome'] == name:
                            unicita = True
                    else:
                        name = function.locomotives_data[index_to_replace]['Nome']
                        unicita = True

                    #controlla che ci sia stata corrispondenza per l'indice e che il nome non sia gia stato utilizzato
                    if unicita:

                        #Sostituisci il dizionario all'indice trovato con il nuovo dizionario
                        if function.locomotives_data[index_to_replace]['LocoID'] != loco_id:
                            if function.are_you_sure("Prima di continuare assicurati di avere solo la locomotiva alla quale si vuole cambiare l'indirizzo sui binari"):
                                if color != "Default":
                                    #prima di sostituire la locomotiva, aggiungo il colore che le apparteneva al vettore dei colori disponibili
                                    function.color_available.insert(0,function.locomotives_data[index_to_replace]['Colore'])
                                    function.color_available.remove(color)
                                else:
                                    #assegno il colore che gia ha
                                    color = function.locomotives_data[index_to_replace]['Colore']
                                new_dict = {'ID':id,'Nome': name, 'LocoID':loco_id, 'Colore':color, 'Velocita':0, 'VelocitaM':0, 'Direzione':1}
                                if comandi.is_serial_port_available(""):
                                    comandi.change_id(function.locomotives_data[index_to_replace]['LocoID'],loco_id)
                                else: print("Serial port COM4 not available")
                                function.locomotives_data[index_to_replace] = new_dict
                            else:
                                function.variabili_chiusura["locomotive_modify_var"] = True
                        else:
                            if color != "Default":
                                #prima di sostituire la locomotiva, aggiungo il colore che le apparteneva al vettore dei colori disponibili
                                function.color_available.insert(0,function.locomotives_data[index_to_replace]['Colore'])
                                function.color_available.remove(color)
                            else:
                                #assegno il colore che gia ha
                                color = function.locomotives_data[index_to_replace]['Colore']
                            new_dict = {'ID':id,'Nome': name, 'LocoID':loco_id, 'Colore':color, 'Velocita':0, 'VelocitaM':0, 'Direzione':1}
                            function.locomotives_data[index_to_replace] = new_dict
                        update_table()
                    
                    else:
                        function.show_error_box("Nome gia inserito","close_window/locomotive_modify_var","")
                        #open_locomotive_modify_window()
                else:
                    function.show_error_box("Indice non valido","close_window/locomotive_modify_var","")
            #chiude la finestra  
            function.on_close(locomotive_modify_window,-1)
            if function.variabili_chiusura["locomotive_modify_var"]:
                locomotive_modify_window.after(20,open_locomotive_modify_window())
            #locomotive_modify_window.destroy()
        
        # Creazione del form per la nuova locomotiva
        ID_label = tk.Label(locomotive_modify_window, text="ID della locomotiva da modificare:")
        ID_label.pack()
        ID_entry = tk.Entry(locomotive_modify_window)
        ID_entry.pack()

        name_label = tk.Label(locomotive_modify_window, text="Nuovo Nome:")
        name_label.pack()
        name_entry = tk.Entry(locomotive_modify_window)
        name_entry.pack()

        loco_id_label = tk.Label(locomotive_modify_window, text="Nuovo LocoID:")
        loco_id_label.pack()
        loco_id_entry = tk.Entry(locomotive_modify_window)
        loco_id_entry.pack()

        color_label = tk.Label(locomotive_modify_window, text="Colore*:")
        color_label.pack()

#Il numero dei colori all'interno del vettore deve essere almeno pari al numero di locomoitive massime del sistema, senno errore
        var_color = tk.StringVar(value=function.color_available[-1])
        color_button = ttk.Menubutton(locomotive_modify_window,text="Default",width=19)
        color = tk.Menu(color_button, tearoff=0)
        color_button.pack()

        color_button["menu"] = color
        color.delete(0, "end")
        for item in function.color_available:
            color.add_radiobutton(
                label=item,
                value=item,
                variable=var_color,
                command=lambda:color_button.configure(text=var_color.get())
                )
        
        # style1 = ttk.Style()
        # style1.configure('UniqueCustom.TMenubutton', borderwidth=1, relief="solid", padding=()) 
        color_button.config(style='UniqueCustom.TMenubutton')

        modify_button = tk.Button(locomotive_modify_window, text="Modifica", command=modify_locomotive)
        modify_button.pack(pady=(10,0))

        locomotive_modify_window.bind('<Return>', lambda event: modify_locomotive())
        locomotive_modify_window.protocol("WM_DELETE_WINDOW", lambda:function.on_close(locomotive_modify_window,-1))
    else:
        function.show_error_box("Non puoi aprire un altra pagina","focus_page/_",locomotive_modify_window)
  
#Funzione per pagina per controllare gli scambi e il circuito
def open_control():
    global locomotive_circuit_window
    # function.variabili_chiusura["locomotive_circuit_var"] = False # In realta non serve
    if locomotive_circuit_window is None or not locomotive_circuit_window.winfo_exists():
        function.variabili_chiusura["locomotive_circuit_var"] = False
        #flag per l'apertura della pagina
        open=True
        
        #Nel caso in cui la seriale non sia collegata, si chiede all'utente se vuole continuare
        if not comandi.is_serial_port_available(""):
            open = function.are_you_sure("La porta seriale COM4 è scollegata")
                
        
        if open:
            #creazione ficircuit per decider il tipo di controllo del sistema
            locomotive_circuit_window = tk.Toplevel(root)
            locomotive_circuit_window.title("Gestione controlcircuituale/auto")
            locomotive_circuit_window.protocol("WM_DELETE_WINDOW", lambda:(function.on_close(locomotive_circuit_window,-1),algorithm.algo("stop")))
            locomotive_circuit_window.resizable(False, False)

            circuito.open_control_window(False,locomotive_circuit_window)

    else: 
        function.show_error_box("Non puoi aprire un altra pagina","focus_page/_",locomotive_circuit_window)

#Funzione per pagina per controllare le locomotive
def open_locomotive_control():
    global locomotive_control_window
    locomotiva = var_locomotive.get()
    id_controllo = function.CalcolaIDtreno('Nome',locomotiva)
    function.variabili_chiusura["locomotive_control_var"][id_controllo] = False

    if locomotive_control_window[id_controllo] is None or not locomotive_control_window[id_controllo].winfo_exists():
        #creazione della pagina
        locomotive_control_window[id_controllo] = tk.Toplevel(root)
        locomotive_control_window[id_controllo].title(locomotiva)
        locomotive_control_window[id_controllo].geometry("300x250")
        #per disabilitare il ridimensionamento
        locomotive_control_window[id_controllo].resizable(False, False)
        locomotive_control_window[id_controllo].iconbitmap("interfaccia_grafica\\assets\\icon_control.ico")
        
        speed_label = tk.Label(locomotive_control_window[id_controllo], text="Regola la velocità:")
        speed_label.pack(pady=10)

        #creazione dello slider
        speed_slider = tk.Scale(locomotive_control_window[id_controllo], from_=0, to=100, orient=tk.HORIZONTAL)
        speed_slider.pack(pady=5)

        #funzione per settare lo slider alla velocita salvata
        speed_slider.set(function.locomotives_data[id_controllo]['Velocita'])
        check_control_button_state()
    
        root_control = tk.Frame(locomotive_control_window[id_controllo])
        root_control.pack(pady=5)
        #root_control.configure(bg="#c0c0c0")

        #funzione per il throttle delle locomotive
        def throttle_command(direzione):
            #prendere gli input da mandare al comando
            velocita        = speed_slider.get()
            id_loco         = function.CalcolaIDtreno('Nome',locomotiva)
            memoria         = function.locomotives_data[id_loco]['ID']
            ID              = function.locomotives_data[id_loco]['LocoID']
            #Impostare la velocita in memoria e la direzione
            function.locomotives_data[id_loco]['Velocita']  = velocita
            function.locomotives_data[id_loco]['Direzione'] = direzione
            #moltiplicazione per la costante e approssimazione
            velocita_effettiva = velocita*K_velocita
            if comandi.is_serial_port_available(""):
                #mando il comando di throttle
                comandi.throttle(memoria,ID,round(velocita_effettiva),direzione)
            else: function.show_error_box("Serial port COM4 not available","focus_page/_",locomotive_control_window[id_controllo])

        #funzione per arrestare la locomotiva - setta lo slider a 0
        def stop_command():
            #prendere gli input da mandare al comando
            id_loco     = function.CalcolaIDtreno('Nome',locomotiva)
            memoria     = function.locomotives_data[id_loco]['ID']
            ID          = function.locomotives_data[id_loco]['LocoID']
            #Impostare la velocita in memoria e la direzione
            function.locomotives_data[id_loco]['VelocitaM']  = function.locomotives_data[id_loco]['Velocita']
            function.locomotives_data[id_loco]['Velocita']   = 0
            if comandi.is_serial_port_available(""):
                comandi.STOP(memoria,ID)
                speed_slider.set(0)
            else: function.show_error_box("Serial port COM4 not available","focus_page/_",locomotive_control_window[id_controllo])
            
        
        #creazione del form
        direction_label = tk.Label(root_control, text="Direzione:")
        direction_label.pack(side=tk.TOP, pady=5)

        forward_button = tk.Button(root_control, text="Avanti",command=lambda:throttle_command(1))
        forward_button.pack(side=tk.LEFT, padx=5,pady=5)

        backward_button = tk.Button(root_control, text="Indietro",command=lambda:throttle_command(0))
        backward_button.pack(side=tk.LEFT, padx=5,pady=5)

        stop_button = tk.Button(locomotive_control_window[id_controllo], bg="#f08080", text="Arresta",command=stop_command)
        stop_button.pack(pady=5)

        locomotive_control_window[id_controllo].bind('<Return>', lambda event: stop_command())
        locomotive_control_window[id_controllo].protocol("WM_DELETE_WINDOW", lambda:function.on_close(locomotive_control_window,id_controllo))
    else:
        function.show_error_box("Non puoi aprire un altra pagina","focus_page/_",locomotive_control_window[id_controllo])
        # locomotive_control_window[id_controllo].focus_set()

#controllo sull'abilitazione dei bottoni
def check_control_button_state():
    if function.locomotives_data:
        remove_button.config(state='normal')
        modify_button.config(state='normal')
        if on_button.cget("background") == "#00ff00":
            control_button.config(state='normal')
            STOP_button.config(state='normal')
        else:
            control_button.config(state='disabled')
            STOP_button.config(state='disabled')
    else:
        control_button.config(state='disabled')
        remove_button.config(state='disabled')
        modify_button.config(state='disabled')
        

#funzione per aggioranre la tabella - all'interno c'è anche la funzione che gestisce il menu a tendina del controllo
def update_table():
    global locomotive_names
    # Pulizia della tabella
    for row in tree.get_children():
        tree.delete(row)

    # Riempimento della tabella con i dati delle locomotive
    for locomotive in function.locomotives_data:
        tree.insert('', tk.END, values=(
            locomotive['ID'],
            locomotive['LocoID'],
            locomotive['Colore'],
            locomotive['Nome']
        ),tags=('color'))

    tree.tag_configure('color', background='#EDEDED')

    for col in columns:
        tree.column(col, anchor='center')  # Imposta l'allineamento al centro per tutte le colonne


    locomotive_names = [locomotive['Nome'] for locomotive in function.locomotives_data]
    check_control_button_state()
    
    control_button["menu"] = control
    control.delete(0, "end")
    for loco in locomotive_names:
        control.add_radiobutton(
            label=loco,
            value=loco,
            variable=var_locomotive,
            command= open_locomotive_control)
        
    
#funzione che serve per la gestione del bottone ON/OFF della corrente
def on_off():
    current_color = on_button.cget("background")
    if current_color == "red":
        on=1
    else:
        on=0
    #controlla se la seriale è collegata correttamente
    if comandi.is_serial_port_available(""):
        comandi.open_current(on)
        #cambia il colore al bottone
        new_color = "#00ff00" if current_color == "red" else "red"
        on_button.config(background=new_color)
        check_control_button_state()
    else:
        function.show_error_box("Serial port COM4 not available","focus_page/_",root)


#funzione che serve per la gesetione dell'avvio e dell'arresto del sistema senza togliere la corrente
def GENERAL_STOP_START():
    current_color       = STOP_button.cget("background")
    contatore_velocita  = 0
    start = False
    is0   = False
    i=0
    if comandi.is_serial_port_available(""):
        #ciclo che si esegue per ogni locomotiva
        for i in range (len(function.locomotives_data)):
            #se la velocita è 0 si aumenta il contatore, e is0 è settato a True
            if function.locomotives_data[i]['Velocita'] == 0:
                contatore_velocita=contatore_velocita+1
                is0 = True
            #in base al colore del bottone, si attiva
            if current_color == "#f08080":
                #ferma completamente il sistema
                memoria = function.locomotives_data[i]['ID']
                ID      = function.locomotives_data[i]['LocoID']
                #se la locomotiva era gia ferma, il comando non gli viene mandato
                if not is0:
                    #predno in memoria la velocita corrente e poi gli assegno il valore
                    function.locomotives_data[i]['VelocitaM'] = function.locomotives_data[i]['Velocita']
                    function.locomotives_data[i]['Velocita']  = 0
                    comandi.STOP(memoria,ID)
            else:
                #ripristina il sistema come era prima
                memoria     = function.locomotives_data[i]['ID']
                ID          = function.locomotives_data[i]['LocoID']
                velocita    = function.locomotives_data[i]['VelocitaM'] 
                direzione   = function.locomotives_data[i]['Direzione'] 
                start = True

                #se la locomotiva era ferma il comadno non gli viene mandato
                if not is0 or function.locomotives_data[i]['VelocitaM']!=0:
                    #predno in memoria la velocita corrente e poi gli assegno il valore
                    function.locomotives_data[i]['VelocitaM'] = function.locomotives_data[i]['Velocita']
                    function.locomotives_data[i]['Velocita']  = velocita
                    comandi.throttle(memoria,ID,velocita,direzione)
            i=i+1
            is0 = False
    else:
        function.show_error_box("Serial port COM4 not available","focus_page/_",root)
    #cambia lo stile del bottone a seconda di come va il sistema, verde se è fermo e rosso se è in movimento
    if contatore_velocita != len(function.locomotives_data) or start:  
        new_color = "#8fbc8f" if current_color == "#f08080" else "#f08080"
        new_text = "AVVIO GENERALE" if current_color == "#f08080" else "STOP GENERALE"
        STOP_button.config(background=new_color,text=new_text)
        check_control_button_state()
        
root = tk.Tk()
root.title("Gestione Locomotive")
root.configure(bg="#c0c0c0")
root.iconbitmap("interfaccia_grafica\\assets\\window_logo.ico")
#funzione da eseguire alla chiusura della pagina
root.protocol("WM_DELETE_WINDOW", lambda:(root.destroy(),algorithm.algo("stop")))
#per disabilitare il ridimensionamento
root.resizable(False, False)

root1 = tk.Frame()
root1.pack(side="bottom", pady=10)
root1.configure(bg="#c0c0c0")

locomotive_label = tk.Label(root, text="DATABASE LOCOMOTIVE",bg="#c0c0c0")
locomotive_label.pack(pady=10)

#Creazione tabella fisica
columns = ('ID Locale', 'ID Locomotive', 'Colore', 'Nome')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack()

# Pulsante per aggiungere una locomotiva
add_button = tk.Button(root1, text="AGGIUNGI LOCOMOTIVA",height=2,command= open_locomotive_creation_window)
add_button.pack(side="left", padx=5)

#Pulsante per rimuovere una locomotiva
remove_button = tk.Button(root1, text="RIMUOVI LOCOMOTIVA",height=2,command= open_locomotive_remove_window)
remove_button.pack(side="left", padx=5)
remove_button.config(state='disabled')

#Pulsante per modificare una locomotiva
modify_button = tk.Button(root1, text="MODIFICA LOCOMOTIVA",height=2,command=open_locomotive_modify_window)
modify_button.pack(side="left", padx=5)
modify_button.config(state='disabled')

# Creazione del Menubutton
image_control_path = "interfaccia_grafica\\assets\\controller.png"
image_control = function.process_image(image_control_path,'resize',35,35)
var_locomotive = tk.StringVar()
control_button = ttk.Menubutton(root1, image=image_control)
control = tk.Menu(control_button, tearoff=0)
control_button.pack(side="left",padx=(100,0))

# Imposta il colore di sfondo del bottone CONTROLLA
style = ttk.Style()
control_button.config(state='disabled',style='Custom.TMenubutton')
style.configure('Custom.TMenubutton', background ="#c0c0c0")  #background ="#add8e6"
style.layout('Custom.TMenubutton',indicatoron)

#Tasto per il controllo del - 
image_path = "interfaccia_grafica\\assets\\controllo.png"
image = function.process_image(image_path,'resize',35,35)
circuit_button = tk.Button(root1,image=image, bg="#c0c0c0",borderwidth=0, command=open_control)
circuit_button.pack(side="left", padx=(10,5))

# Accendi spegni corrente
image_power_path="interfaccia_grafica\\assets\\power_icon.png"
image_power = function.process_image(image_power_path,'resize',35,35)
on_button = tk.Button(root1, image=image_power, background="red", command=on_off)
on_button.pack(side="left", padx=5)


#bottone per lo stop/avvio generale
STOP_button = tk.Button(root1, text="STOP GENERALE", background="#f08080", height=2, width=15, command=GENERAL_STOP_START)
STOP_button.pack(side="left", padx=5)
STOP_button.config(state='disabled')

root.mainloop()

