import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import comandi
import os

locomotives_data =      []           # Lista per salvare i dati delle locomotive

# Dizionario per tenere in memoria l'apertura delle pagine
variabili_chiusura = {                   
    "locomotive_creation_var": False,
    "locomotive_remove_var":   False,
    "locomotive_modify_var":   False,
    "locomotive_circuit_var":   False,
    "locomotive_control_var":  []
}

color_available = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange", "Pink", "Brown", "Gray", "Cyan","Default"]

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

#creazione in memoria dei sensori
# Sensors["Terminate"] = [Bool di boot per algo]
# Sensors[Sensore 1] = [Ultimo messaggio ricevuto,Memoria dell'ultimo treno passato all'indietro,Memoria dell'ultimo treno passato in avanti] |fase di test|
Sensors = {
    "Terminate":   [False],
    "Sensore 1":   ["","",""],
    "Sensore 2":   ["","",""],
    "Sensore 3":   [""],
    "Sensore 4":   [""],
    "Sensore 5":   [""],
    "Sensore 6":   [""],
    "Sensore 7":   [""],
    "Sensore 8":   [""]
}

#array dei canvas
canvas_array = [""]

'''
            ___                                              _            
    o O O  / __|    ___    _ _      ___      _ _   __ _     | |     ___   
   o      | (_ |   / -_)  | ' \    / -_)    | '_| / _` |    | |    (_-<   
  TS__[O]  \___|   \___|  |_||_|   \___|   _|_|_  \__,_|   _|_|_   /__/_  
 {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'

'''

#Funzione che riassume i resize e i rotate
def process_image(image_path, operation, *args):
    # Apri l'immagine utilizzando PIL
    img = Image.open(image_path)

    if operation == 'resize':
        # Ridimensiona l'immagine
        processed_img = img.resize((args[0], args[1]), Image.BILINEAR)
        return ImageTk.PhotoImage(processed_img)
    elif operation == 'rotate':
        # Ruota l'immagine di un certo angolo e ridimensiona
        rotated_img = img.rotate(args[0], expand=True)
        processed_img = rotated_img.resize((args[1], args[2]), Image.BILINEAR)
        return ImageTk.PhotoImage(processed_img)
    else:
        # Gestisci altri casi o restituisci l'immagine originale
        processed_img = img
        return processed_img
    
#funzione per gli errori
#def show_error_box(descrizione):
def show_error_box(descrizione,modalita,finestra):

    #divisione del messaggio dalla modalita
    modalita = modalita.split("/")
    #matcha il tipo di modalita
    messagebox.showerror("ERRORE", descrizione)
    match modalita[0]:
        case "close_window":
            #prende l'informazione nascosta
            variabili_chiusura[modalita[1]] = True
            pass
        case "focus_page":
            finestra.focus_set()
        case "serial_port":
            comandi.inizialized[0] = False
            if finestra != "":
                finestra.focus_set()
        case _:
            print(";)")

#Funzione per WARNING
def are_you_sure(descrizione):
    risposta = messagebox.askyesno("ATTENZIONE", descrizione+"\nSei sicuro di voler continuare?",icon='warning')
    return risposta

#Calcola l'ID del treno dalle info - Elemento, stringa che dice che elemento si analizza - info, informazione da cui si vuole partire
def CalcolaIDtreno(elemento,info):
    ID_treno = next((i for i, item in enumerate(locomotives_data) if item[elemento] == info ),None)
    return ID_treno

#Gestione della funzione di controllo per la chiusura della finestra
def on_close(finestra,id_controllo):

    #il locomotive control window neccessita di un parametro in piu, la posizione del nome
    if id_controllo != -1:
        finestra[id_controllo].destroy()
        finestra[id_controllo] = None
    else:
        finestra.destroy()
        finestra = None
    #se la funzione on_close è chiamata dallo show_error_box, non è necessario chiudere la finestra


'''
            ___      _                               _      _     
    o O O  / __|    (_)      _ _    __     _  _     (_)    | |_   
   o      | (__     | |     | '_|  / _|   | +| |    | |    |  _|  
  TS__[O]  \___|   _|_|_   _|_|_   \__|_   \_,_|   _|_|_   _\__|  
 {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
'''

#Funzione per cambiare i deviatoi
def change_Turnouts(text,button):
    #gestione grafica degli scambi
    if button == "":
        pass
    else:
        current_color = button.cget("background")
        new_color = "#8fbc8f" if current_color == "#f08080" else "#f08080"
        new_text = "/" if current_color == "#f08080" else "|"
        button.config(background=new_color,text=new_text)

    if comandi.is_serial_port_available(""):
        comandi.cambia_deviatoio(Turnouts[text][1])

        #print("fuori ",Turnouts[text][1])
        if not Turnouts[text][0]:
            change_color(text,Turnouts[text][0])
            Turnouts[text][0] = True
            
        else:
            controlla_scambi_doppi(text)
            Turnouts[text][0] = False 

#Funzione che controlla se lo scambio_doppio è selezionato da almeno 1 dei due, se è cosi non cambia il centrale ma l'altro, senno lo cambia
def controlla_scambi_doppi(text):
    if Turnouts[text][3] == Turnouts['Cambio 4'][3]:
        #qui siamo entrati sia nel caso in cui text è 4 sia se è 8
        if Turnouts['Cambio 4'][0] and Turnouts['Cambio 8'][0]:
            #dato che una è una curva e l'altra è un segmento, bisogna specificare il caso
            if text == 'Cambio 4':
                canvas_array[0].itemconfig(Turnouts[text][2], fill="red")
            else:
                canvas_array[0].itemconfig(Turnouts[text][2], outline="red")
        else:
            #nel caso in cui non siano entrambi attivi, esegue semplicemente la funzione
            change_color(text,Turnouts[text][0])
        
    elif Turnouts[text][3] == Turnouts['Cambio 6'][3]:
        #qui siamo entrati sia nel caso in cui text è 6 sia se è 7
        if Turnouts['Cambio 6'][0] and Turnouts['Cambio 7'][0]:
            #dato che sono entrambe curve basta un solo comando, non si cambia quello comune
            canvas_array[0].itemconfig(Turnouts[text][2], outline="red")
        else:
            #nel caso in cui non siano entrambi attivi, esegue semplicemente la funzione
            change_color(text,Turnouts[text][0])
    else:
        #nel caso in cui non siano tra gli scambi doppi, esegue semplicemente la funzione
        change_color(text,Turnouts[text][0])

    #Funzione che ccambia il colore dello0 scambio in base a come è nel circuito
def change_color(text,activated):
    print(Turnouts[text])
    if text not in {'Cambio 3', 'Cambio 4', 'Cambio 5'}:
        #Se il cambio è fromato da 2 curve
        if activated:
            canvas_array[0].itemconfig(Turnouts[text][2], outline="red")
            canvas_array[0].itemconfig(Turnouts[text][3], outline="black")   
        else:
            canvas_array[0].itemconfig(Turnouts[text][3], outline="red")
            canvas_array[0].itemconfig(Turnouts[text][2], outline="black")
    else:
        #Se il cambio è fromato da 1 curva ed un segmento
        if activated:
            canvas_array[0].itemconfig(Turnouts[text][2], fill="red")
            canvas_array[0].itemconfig(Turnouts[text][3], outline="black")
        else:
            canvas_array[0].itemconfig(Turnouts[text][3], outline="red")
            canvas_array[0].itemconfig(Turnouts[text][2], fill="black")