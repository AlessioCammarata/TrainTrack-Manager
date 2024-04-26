import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import data
import os
import serial

'''

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
    if data.SO['windows']:
        return data.path + "\\assets\\" + asset_name + "." + extenction
    elif data.SO['linux']:
        return data.path + "/assets/" + asset_name + "." + extenction

# Funzione che riassume i resize e i rotate
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
        
        #Test, non serve ora come ora
        case 'opacity':
            # Imposta l'opacità desiderata (0 per trasparente, 1 per opaco)
            opacity = args[0]  # Opacità al 50%
            image = img.convert("RGBA")
            alpha = int(255 * opacity)
            image.putalpha(alpha)

            # Converte l'immagine in un oggetto PhotoImage di Tkinter
            return ImageTk.PhotoImage(image)
    return img
            
#Funzione per impostare la var di chiusura, quando si chiude la finestra
def set_variabilechiusura(window_type):
    data.variabili_apertura[f'locomotive_{window_type}_var'] = False

#funzione per gli errori
def show_error_box(descrizione,finestra,finestra_padre,importance):

    #Ci sono degli errori che non devono attivare la var
    if importance != "main":
        data.control_var_errore = True
    #divisione del messaggio dalla modalita
    finestra_padre.grab_set()
    #matcha il tipo di modalita
    messagebox.showerror("ERRORE", descrizione)
    finestra_padre.grab_release()

    finestra.focus_set()

#Funzione per WARNING
def are_you_sure(descrizione):
    risposta = messagebox.askyesno("ATTENZIONE", descrizione+"\n"+data.Textlines[65], icon='warning')
    return risposta

#Funzione per INFO
def show_info(descrizione):
    return messagebox.showinfo("AVVISO", descrizione)

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
    #se la funzione on_close è chiamata dallo show_error_box, non è necessario chiudere la finestra

#Controlla il SO, e scrive il path a seconda del SO
def find_port_path(function_port):
    if data.SO['linux']:
        port_path = f"/dev/{function_port}"  # Per sistemi Unix-like (Linux, macOS)
    elif data.SO['windows']:
        port_path = f"COM{function_port}"  # Per sistemi Windows
    else:
        show_error_box("Non ho il tuo SO bro","_/_","")
    return port_path

#Funzione che controlla se la porta seriale chiamata è collegata o meno e se è stata inizializzata - in caso non sia stata inizializzata, la inizializza
def is_serial_port_available(function_port):
    if data.serial_port_info[function_port][1]:
        # Costruisci il percorso del dispositivo della porta seriale
        port_path = find_port_path(function_port)  
        exist = os.path.exists(port_path)

        if exist and not data.serial_port_info[function_port][0]:
            data.serial_port_info[function_port][0] = True
            serial.Serial(port_path,baudrate=115200,timeout=1)
        # Verifica l'esistenza del percorso della porta seriale

        exist_inizialized = exist and data.serial_port_info[function_port][0]
        return exist_inizialized
    else: return False
    
#Funzione che controlla solo che sia collegata una porta al pc
def port_exist(function_port):
    # Costruisci il percorso del dispositivo della porta seriale
    port_path = find_port_path(function_port)  
    exist = os.path.exists(port_path)
    print(f"port exist:{port_path} e {exist}")
    print(data.serial_ports)
    return exist

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

def translate():
    print(data.languages[0])
    data.Textlines = []
    # Apro il file in modalità lettura
    with open(data.path + "\\languages\\file{}.txt".format(data.languages[0]), 'r',encoding='utf-8') as file:
        # Leggo ogni riga del file
        for line in file:
            # Aggiungo la riga alla lista
            data.Textlines.append(line.strip())