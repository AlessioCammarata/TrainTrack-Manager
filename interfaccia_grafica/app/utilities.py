import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import app.data as data
import os
import serial

'''
.. code-block:: txt

               _   _    _        _       _       _      _        _                    
        o O O | | | |  | |_     (_)     | |     (_)    | |_     (_)     ___     ___   
       o      | |_| |  |  _|    | |     | |     | |    |  _|    | |    / -_)   (_-<   
      TS__[O]  \___/   _\__|   _|_|_   _|_|_   _|_|_   _\__|   _|_|_   \___|   /__/_  
     {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
    ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'

'''

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


# def image_path(image_name: str):
#     image_path = asset_path(image_name, "png")
#     img = Image.open(image_path)
#     return ImageTk.PhotoImage(img)

#Funzione che riassume il path relativo
def asset_path(asset_name: str, extenction: str) -> str:  
                    # Per sistemi Windows                                                Per sistemi Unix-like (Linux, macOS)
    return data.path + "\\assets\\" + asset_name + "." + extenction if data.SO == 'Windows' else data.path + "/assets/" + asset_name + "." + extenction

# Funzione che riassume i resize e i rotate, viene utilizzata per preparare le immagini a essere posizionate nel canvas
def process_image(image_path, operation, *args):
    img = Image.open(image_path)

    match operation:
        case 'resize':
            processed_img = img.resize((args[0], args[1]), Image.BILINEAR)
            return ImageTk.PhotoImage(processed_img)

        case 'rotate':
            rotated_img = img.rotate(args[0], expand=True)
            processed_img = rotated_img.resize((args[1], args[2]), Image.BILINEAR)
            return ImageTk.PhotoImage(processed_img)
        
            
#Funzione per impostare la var di chiusura, quando si chiude la finestra
def set_variabilechiusura(window_type):
    data.variabili_apertura[f'locomotive_{window_type}_var'] = False

#funzione per gli errori
def show_error_box(descrizione,finestra_padre,importance):

    #Ci sono degli errori che non devono attivare la var
    if importance != "main":
        data.control_var_errore = True

    finestra_padre.grab_set()
    messagebox.showerror("ERRORE", descrizione,  parent = finestra_padre)
    finestra_padre.grab_release()

#Funzione per WARNING - Grab del padre
def are_you_sure(descrizione,finestra_padre):
    finestra_padre.grab_set()
    risposta = messagebox.askyesno("ATTENZIONE", descrizione+"\n"+data.Textlines[65], icon='warning', parent = finestra_padre)
    finestra_padre.grab_release()
    return risposta

#Funzione per INFO - Grab del padre
def show_info(descrizione,finestra_padre):
    finestra_padre.grab_set()
    messagebox.showinfo("AVVISO", descrizione, parent = finestra_padre)
    finestra_padre.grab_release()
    

#Calcola l'ID del treno dalle info - Elemento, stringa che dice che elemento si analizza - info, informazione da cui si vuole partire
def CalcolaIDtreno(elemento,info):
    ID_treno = next((i for i, item in enumerate(data.locomotives_data) if item[elemento] == info ),None)
    return ID_treno

#Gestione della funzione di controllo per la chiusura della finestra
def on_close(finestra,window_type):
    if not window_type.isdigit():
        set_variabilechiusura(window_type)
    else:
        data.variabili_apertura[f'locomotive_control_var'][int(window_type)] = False
    finestra.destroy()
    finestra = None

#Controlla il SO, e scrive il path a seconda del SO
def find_port_path(function_port):

            # Per sistemi Windows                       Per sistemi Unix-like (Linux, macOS)
    return f"COM{function_port}" if data.SO == 'Windows' else f"/dev/{function_port}"  
    

#Funzione che controlla se la porta seriale chiamata è collegata o meno e se è stata inizializzata - in caso non sia stata inizializzata, la inizializza
def is_serial_port_available(function_port):
    if data.root:
        # show_info("ROOT")
        return True
    if data.serial_port_info[function_port][1]:
        # Costruisci il percorso del dispositivo della porta seriale
        port_path = find_port_path(function_port)  
        exist = os.path.exists(port_path)

        #Nel caso in cui la porta non sia stata inizializzzìata, la inizializza.
        if exist and not data.serial_port_info[function_port][0]:
            data.serial_port_info[function_port][0] = True
            serial.Serial(port_path,baudrate=115200,timeout=1)
        # Verifica l'esistenza del percorso della porta seriale

        exist_inizialized = exist and data.serial_port_info[function_port][0]
        return exist_inizialized
    # else: 
    return False
    
#Funzione che controlla solo che sia collegata una porta al pc
def port_exist(function_port):
    # Costruisci il percorso del dispositivo della porta seriale
    port_path = find_port_path(function_port)  
    exist = os.path.exists(port_path)
    print(f"port exist:{port_path} e {exist}")
    # print(data.serial_ports)
    return exist

#Funzione utilizzata allo start per impostare le porte gia collegate, nel caso, in memoria
def set_port_var(*args):
    ports_available = ["",""]
    port1_enable = True
    port2_enable = True

    if not args:
        
        #Controlla le prime 10 porte se sono libere - si puo cambiare
        flag = 0
        for i in range(data.port_range):
            if port_exist(i) and flag<len(data.serial_ports):
               ports_available[flag] = i
               flag+=1 
            i+=1

        #Reimposta i valori standard nel caso in cui sia stato modificato qualcosa - Esce nel caso in cui non ci sia nessuna porta collegata
        if flag < 2: 
            ports_available[1] = data.serial_ports[1]
            port2_enable = False
            if flag < 1: 
                ports_available[0] = data.serial_ports[0]
                return data.Textlines[32] + "\n" + data.Textlines[33]
    else:
        ports_available[0]  = args[0]
        ports_available[1]  = args[1]

    #Dizionario temporale che aggiorna le chiavi
    temp_dict = {
                    ports_available[0]: data.serial_port_info.pop(data.serial_ports[0]),
                    ports_available[1]: data.serial_port_info.pop(data.serial_ports[1])
                }
    
    #assegnazione delle porte nel vettore
    data.serial_ports[0] = ports_available[0]
    data.serial_ports[1] = ports_available[1]

    # Aggiornare il dizionario originale con le nuove chiavi
    data.serial_port_info.update(temp_dict)

    if not args:
        #Imposta a True se entrambe sono gia attaccate, in caso contrario lascia le impostazioni base
        data.serial_port_info[data.serial_ports[0]][1]      = port1_enable
        data.serial_port_info[data.serial_ports[1]][1]      = port2_enable

    return data.serial_ports

#Funzione che permette di aggiornare la tabella delle calibrazioni RFID
def update_circuit_table(columns,tree):
        
    for col in columns:
        tree.heading(col, text=col)
    tree.grid(row=1, column=0, padx=5, pady=5, sticky="nswe")

    for row in tree.get_children():
        tree.delete(row)

        # Riempimento della tabella con i dati delle locomotive
    i=0
    for locomotive in data.locomotives_data:
        i += 1
        if locomotive['RFIDtag'] == "":
            data.calibred = False
        tree.insert('', tk.END, values=(
            locomotive['ID'],
            locomotive['RFIDtag'],
            locomotive['Nome']
        ),tags=(i))
        tree.tag_configure(i, background=locomotive['Colore'])

    for col in columns:
        tree.column(col, anchor='center', width=100)  # Imposta l'allineamento al centro per tutte le colonne

#Funzione che aggiorna il textlines con la nuova lingua selezionata
def translate():
    print(data.languages[0])
    data.Textlines = []
    # Apro il file in modalità lettura
    relative_path = "\\languages\\file{}.txt".format(data.languages[0]) if data.SO == 'Windows' else "/languages/file{}.txt".format(data.languages[0])
    with open(data.path + relative_path , 'r',encoding='utf-8') as file:
        # Leggo ogni riga del file
        for line in file:
            # Aggiungo la riga alla lista
            data.Textlines.append(line.strip())
    color_update()

#Funzione che aggiorna la traduzione dei colori
def color_update():
    i=0
    for colors in data.colors:
        data.colors[colors] = data.Textlines[140+i]
        i += 1
