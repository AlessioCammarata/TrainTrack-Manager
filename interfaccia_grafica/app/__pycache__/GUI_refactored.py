import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import comandi_refactored
import algorithm_refactored
import windows
import buttons

#from tkfontawesome import icon_to_image

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

class GUI:
    def __init__(self, root):

        '''
                        ___      _             _                 _            
                o O O  / __|    | |     ___   | |__    __ _     | |     ___   
               o      | (_ |    | |    / _ \  | '_ \  / _` |    | |    (_-<   
              TS__[O]  \___|   _|_|_   \___/  |_.__/  \__,_|   _|_|_   /__/_  
             {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
            ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'  
        '''
        
        self.locomotives_data =      []           # Lista per salvare i dati delle locomotive
        self.locomotive_names =      []           # Lista per i nomi delle locomotive
        self.max_loco         =       3           # Numero max di locomotive che il sistema lavora
        self.max_length_name  =      20           # Numero max di caratteri che il nome puo avere
        self.max_size_loco_id =   10293           # Numero max dell'indirizzo che si puo dare ad una locomotiva
        self.K_velocita       = 126/100           # Costante basata sulla velocita massima possibile di una locomotiva (0-126)

        # Dizionario per tenere in memoria l'apertura delle pagine
        self.variabili_chiusura = {                   
            "locomotive_creation_var": False,
            "locomotive_remove_var":   False,
            "locomotive_modify_var":   False,
            "locomotive_circuit_var":   False,
            "locomotive_control_var":  []
        }

        self.color_available = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange", "Pink", "Brown", "Gray", "Cyan","Default"]

        #Creazione in memoria dei deviatoi
        # Turnout["Cambio1"] = [Stato Turnout, ID turnout, canvasdef, canvas]
        self.Turnouts = {                   
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
        self.Sensors = {
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
        self.canvas_array = [""]
        
        #creazione dell'oggetto algo
        self.algo = algorithm_refactored.Algorithm(self)

        '''
                        ___    _   _    ___   
                o O O  / __|  | | | |  |_ _|  
               o      | (_ |  | |_| |   | |   
              TS__[O]  \___|   \___/   |___|  
             {======|_|"""""|_|"""""|_|"""""| 
            ./o--000'"`-0-0-'"`-0-0-'"`-0-0-' 
        '''
        self.locomotive_creation_window = None
        self.locomotive_remove_window = None
        self.locomotive_modify_window = None
        self.locomotive_circuit_window = None
        self.locomotive_control_window = []


        self.root = root
        self.root.title("Gestione Locomotive")
        self.root.configure(bg="#c0c0c0")
        self.root.iconbitmap("interfaccia_grafica\\assets\\window_logo.ico")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close_root)
        self.root.resizable(False, False)

        self.root_frame = tk.Frame()
        self.root_frame.pack(side="bottom", pady=10)
        self.root_frame.configure(bg="#c0c0c0")

        self.locomotive_label = tk.Label(root, text="DATABASE LOCOMOTIVE", bg="#c0c0c0")
        self.locomotive_label.pack(pady=10)

        self.columns = ('ID Locale', 'ID Locomotive', 'Colore', 'Nome')
        self.tree = ttk.Treeview(root, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack()

        self.add_button = tk.Button(self.root_frame, text="AGGIUNGI LOCOMOTIVA", height=2, command=self.open_locomotive_creation_window)
        self.add_button.pack(side="left", padx=5)

        self.remove_button = tk.Button(self.root_frame, text="RIMUOVI LOCOMOTIVA", height=2, command=self.open_locomotive_remove_window)
        self.remove_button.pack(side="left", padx=5)
        self.remove_button.config(state='disabled')

        self.modify_button = tk.Button(self.root_frame, text="MODIFICA LOCOMOTIVA", height=2, command=self.open_locomotive_modify_window)
        self.modify_button.pack(side="left", padx=5)
        self.modify_button.config(state='disabled')

        self.image_control_path = "interfaccia_grafica\\assets\\controller.png"
        self.image_control = self.process_image(self.image_control_path, 'resize', 35, 35)
        self.var_locomotive = tk.StringVar()
        self.control_button = ttk.Menubutton(self.root_frame, image=self.image_control)
        self.control = tk.Menu(self.control_button, tearoff=0)
        self.control_button.pack(side="left", padx=(100, 0))
        self.control_button.config(state='disabled')

        self.style = ttk.Style()
        self.control_button.config(style='Custom.TMenubutton')
        self.style.configure('Custom.TMenubutton', background="#c0c0c0")
        self.style.layout('Custom.TMenubutton', indicatoron)

        self.image_path = "interfaccia_grafica\\assets\\controllo.png"
        self.image = self.process_image(self.image_path, 'resize', 35, 35)
        self.circuit_button = tk.Button(self.root_frame, image=self.image, bg="#c0c0c0", borderwidth=0, command=self.open_control)
        self.circuit_button.pack(side="left", padx=(10, 5))

        self.image_power_path = "interfaccia_grafica\\assets\\power_icon.png"
        self.image_power = self.process_image(self.image_power_path, 'resize', 35, 35)
        self.on_button = tk.Button(self.root_frame, image=self.image_power, background="red", command=self.on_off)
        self.on_button.pack(side="left", padx=5)

        self.STOP_button = tk.Button(self.root_frame, text="STOP GENERALE", background="#f08080", height=2, width=15, command=self.GENERAL_STOP_START)
        self.STOP_button.pack(side="left", padx=5)
        self.STOP_button.config(state='disabled')

        #self.on_offButton = buttons.Buttons()

        #Inserimento di max finestre nel locomotive control window in base al max_loco
        for i in range(self.max_loco):
            self.locomotive_control_window.append(None)
            self.variabili_chiusura["locomotive_control_var"].append(False)

    '''
                    ___                                              _            
            o O O  / __|    ___    _ _      ___      _ _   __ _     | |     ___   
           o      | (_ |   / -_)  | ' \    / -_)    | '_| / _` |    | |    (_-<   
          TS__[O]  \___|   \___|  |_||_|   \___|   _|_|_  \__,_|   _|_|_   /__/_  
         {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
        ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'

    '''

    #Funzione che riassume i resize e i rotate
    def process_image(self,image_path, operation, *args):
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
    def show_error_box(self,descrizione,modalita,finestra):

        #divisione del messaggio dalla modalita
        modalita = modalita.split("/")
        #matcha il tipo di modalita
        messagebox.showerror("ERRORE", descrizione)
        match modalita[0]:
            case "close_window":
                #prende l'informazione nascosta
                self.variabili_chiusura[modalita[1]] = True
                pass
            case "focus_page":
                finestra.focus_set()
            case "serial_port":
                comandi_refactored.inizialized[0] = False
                if finestra != "":
                    finestra.focus_set()
            case _:
                print(";)")

    #Funzione per WARNING
    def are_you_sure(self,descrizione):
        risposta = messagebox.askyesno("ATTENZIONE", descrizione+"\nSei sicuro di voler continuare?",icon='warning')
        return risposta

    #Calcola l'ID del treno dalle info - Elemento, stringa che dice che elemento si analizza - info, informazione da cui si vuole partire
    def CalcolaIDtreno(self,elemento,info):
        ID_treno = next((i for i, item in enumerate(self.locomotives_data) if item[elemento] == info ),None)
        return ID_treno

    #Gestione della funzione di controllo per la chiusura della finestra
    def on_close(self,finestra,id_controllo):

        #il locomotive control window neccessita di un parametro in piu, la posizione del nome
        if id_controllo != -1:
            finestra[id_controllo].destroy()
            finestra[id_controllo] = None
        else:
            finestra.destroy()
            finestra = None
        #se la funzione on_close è chiamata dallo show_error_box, non è necessario chiudere la finestra

    '''
                    ___    _   _    ___   
            o O O  / __|  | | | |  |_ _|  
           o      | (_ |  | |_| |   | |   
          TS__[O]  \___|   \___/   |___|  
         {======|_|"""""|_|"""""|_|"""""| 
        ./o--000'"`-0-0-'"`-0-0-'"`-0-0-' 
    '''
    def on_close_root(self):

        self.root.destroy()
        self.algo.algo("stop")

    def open_locomotive_creation_window(self):
        # global locomotive_creation_window
        self.variabili_chiusura["locomotive_creation_var"] = False
        if self.locomotive_creation_window is None or not self.locomotive_creation_window.winfo_exists():
            self.locomotive_creation_window = tk.Toplevel(self.root)
            self.locomotive_creation_window.transient(self.root)
            self.locomotive_creation_window.protocol("WM_DELETE_WINDOW", lambda:self.on_close(self.locomotive_creation_window,-1))

            locomotive_creation_window1 = windows.Windows(self.locomotive_creation_window,"Creazione locomotiva","250x170")
            locomotive_creation_window1.creation_window(self)

            
        else:
            self.show_error_box("Non puoi aprire un altra pagina","focus_page/_",self.locomotive_creation_window)
        
        
    def open_locomotive_remove_window(self):
        #global self.locomotive_remove_window
        self.variabili_chiusura["locomotive_remove_var"] = False
        if self.locomotive_remove_window is None or not self.locomotive_remove_window.winfo_exists():
            self.locomotive_remove_window = tk.Toplevel(self.root)
            self.locomotive_remove_window.transient(self.root)
            self.locomotive_remove_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close(self.locomotive_remove_window,-1))

            locomotive_remove_window1 = windows.Windows(self.locomotive_remove_window,"Rimozione Locomotiva","250x150")
            locomotive_remove_window1.remove_window(self)

            
        else:   
            self.show_error_box("Non puoi aprire un altra pagina","focus_page/_",self.locomotive_remove_window)

    def open_locomotive_modify_window(self):
        #global locomotive_modify_window
        self.variabili_chiusura["locomotive_modify_var"] = False
        if self.locomotive_modify_window is None or not self.locomotive_modify_window.winfo_exists():
            #creazione finestra per modificare loco
            self.locomotive_modify_window = tk.Toplevel(self.root)
            self.locomotive_modify_window.transient(self.root)
            self.locomotive_modify_window.protocol("WM_DELETE_WINDOW", lambda:self.on_close(self.locomotive_modify_window,-1))

            locomotive_modify_window1 = windows.Windows(self.locomotive_modify_window,"Modifica Locomotiva","300x200")
            locomotive_modify_window1.modify_window(self)


        else:
            self.show_error_box("Non puoi aprire un altra pagina","focus_page/_",self.locomotive_modify_window)

    def open_control(self):
        #global locomotive_circuit_window

        if self.locomotive_circuit_window is None or not self.locomotive_circuit_window.winfo_exists():
            open=True
            self.variabili_chiusura["locomotive_circuit_var"] = False

            #Nel caso in cui la seriale non sia collegata, si chiede all'utente se vuole continuare
            if not comandi_refactored.is_serial_port_available(""):
                open = self.are_you_sure("La porta seriale COM4 è scollegata")
            
            if open:
                #creazione ficircuit per decider il tipo di controllo del sistema
            
                self.locomotive_circuit_window = tk.Toplevel(self.root)
                #locomotive_circuit_window.transient(self.root)
                self.locomotive_circuit_window.protocol("WM_DELETE_WINDOW", lambda:(self.on_close(self.locomotive_circuit_window,-1),self.algo.algo("stop")))

                locomotive_circuit_window1 = windows.circuit_window(self.locomotive_circuit_window,"Gestione controlcircuituale/auto",len(self.Turnouts),self.algo)
                locomotive_circuit_window1.open_circuit_window(self,False)


        else: 
            self.show_error_box("Non puoi aprire un altra pagina","focus_page/_",self.locomotive_circuit_window)
    
    def open_locomotive_control(self):
        #global locomotive_control_window
        locomotiva      = self.var_locomotive.get()
        id_controllo    = self.CalcolaIDtreno('Nome',locomotiva)
        self.variabili_chiusura["locomotive_control_var"][id_controllo] = False

        if self.locomotive_control_window[id_controllo] is None or not self.locomotive_control_window[id_controllo].winfo_exists():
            
            self.locomotive_control_window[id_controllo] = tk.Toplevel(self.root)
            self.locomotive_control_window[id_controllo].transient(self.root)
            self.locomotive_control_window[id_controllo].iconbitmap("interfaccia_grafica\\assets\\icon_control.ico")
            self.locomotive_control_window[id_controllo].protocol("WM_DELETE_WINDOW", lambda:self.on_close(self.locomotive_control_window,id_controllo))

            locomotive_control_window1 = windows.Windows(self.locomotive_control_window[id_controllo],locomotiva,"300x250")
            locomotive_control_window1.control_window(self,locomotiva,id_controllo)

        else:
            self.show_error_box("Non puoi aprire un altra pagina","focus_page/_",self.locomotive_control_window[id_controllo])

    #funzione che serve per la gestione del bottone ON/OFF della corrente
    def on_off(self):
        current_color = self.on_button.cget("background")

        #controlla se la seriale è collegata correttamente
        if comandi_refactored.is_serial_port_available(""):
            on_offButton = buttons.Buttons(current_color)
            on_offButton.on_off(self)

        else:
            self.show_error_box("Serial port COM4 not available","focus_page/_",self.root)


    #funzione che serve per la gesetione dell'avvio e dell'arresto del sistema senza togliere la corrente
    def GENERAL_STOP_START(self):
        current_color       = self.STOP_button.cget("background")
        
        if comandi_refactored.is_serial_port_available(""):
            STOP_button = buttons.Buttons(current_color)
            STOP_button.GENERAL_STOP_START(self)
           
        else:
            self.show_error_box("Serial port COM4 not available","focus_page/_",self.root)
        

    def check_control_button_state(self):
        if self.locomotives_data:
            self.remove_button.config(state='normal')
            self.modify_button.config(state='normal')
            if self.on_button.cget("background") == "#00ff00":
                self.control_button.config(state='normal')
                self.STOP_button.config(state='normal')
            else:
                self.control_button.config(state='disabled')
                self.STOP_button.config(state='disabled')
        else:
            self.control_button.config(state='disabled')
            self.remove_button.config(state='disabled')
            self.modify_button.config(state='disabled')
        

    #funzione per aggioranre la tabella - all'interno c'è anche la funzione che gestisce il menu a tendina del controllo
    def update_table(self):
        global locomotive_names
        # Pulizia della tabella
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Riempimento della tabella con i dati delle locomotive
        for locomotive in self.locomotives_data:
            self.tree.insert('', tk.END, values=(
                locomotive['ID'],
                locomotive['LocoID'],
                locomotive['Colore'],
                locomotive['Nome']
            ),tags=('color'))

        self.tree.tag_configure('color', background='#EDEDED')

        for col in self.columns:
            self.tree.column(col, anchor='center')  # Imposta l'allineamento al centro per tutte le colonne


        locomotive_names = [locomotive['Nome'] for locomotive in self.locomotives_data]
        self.check_control_button_state()
        
        self.control_button["menu"] = self.control
        self.control.delete(0, "end")
        for loco in locomotive_names:
            self.control.add_radiobutton(
                label=loco,
                value=loco,
                variable=self.var_locomotive,
                command= self.open_locomotive_control)