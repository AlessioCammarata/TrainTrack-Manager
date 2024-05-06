import tkinter as tk
from tkinter import ttk
import windows
import buttons
import utilities
import data

#from tkfontawesome import icon_to_image

class GUI(tk.Frame):
    def __init__(self, container):

        super().__init__(container)
        self.container = container
        self.serial_port = data.serial_ports[0]
        self.locomotive_names = []
        #self.container.bind("<FocusIn>", lambda event: self.container.focus_set())

        '''
                        ___    _   _    ___   
                o O O  / __|  | | | |  |_ _|  
               o      | (_ |  | |_| |   | |   
              TS__[O]  \___|   \___/   |___|  
             {======|_|"""""|_|"""""|_|"""""| 
            ./o--000'"`-0-0-'"`-0-0-'"`-0-0-' 
    
    SHORTCUTS
        
        self.container.bind("<KeyPress-{}>".format(id), lambda event: (self.set_var_keypress_locomotive_control(id),self.open_locomotive_control())) 
        -> Permette di aprire la pagina relativa ai comandi di una locomotiva premendo il suo ID, per: ID < 10
        1 -> loco ID 1
        2 -> loco ID 2
        3 -> loco ID 3
        4 -> loco ID 4
        5 -> loco ID 5
        6 -> loco ID 6
        7 -> loco ID 7
        8 -> loco ID 8
        9 -> loco ID 9

        self.container.bind("<Control-KeyPress-{}>".format(id), lambda event: (self.set_var_keypress_locomotive_control(id),self.open_locomotive_control())) 
        -> Permette di aprire la pagina relativa ai comandi di una locomotiva premendo il suo ID, per: ID < 20
        Control-0 -> lodo ID 10
        Control-1 -> loco ID 11
        Control-2 -> loco ID 12
        Control-3 -> loco ID 13
        Control-4 -> loco ID 14
        Control-5 -> loco ID 15
        Control-6 -> loco ID 16
        Control-7 -> loco ID 17
        Control-8 -> loco ID 18
        Control-9 -> loco ID 19

        self.container.bind("<c>", lambda event: self.open_control())
        c -> Apre la finestra circuit

        self.container.bind("<s>", lambda event: self.open_settings_window())
        s -> Apre le impostazione del sistema

        self.container.bind("<o>", lambda event: self.on_off())
        o -> Permette di dare la corrente ai binari

        self.container.bind("<i>", lambda event: self.open_info_window())
        i -> Apre le Informazioni generali

        self.container.bind("<plus>", lambda event: self.open_locomotive_creation_window())
        + -> Preme il tasto aggiungi locomotiva

        self.container.bind("<minus>", lambda event: self.open_locomotive_remove_window())
        - -> Preme il tasto rimuovi locomotiva

        self.container.bind("<m>", lambda event: self.open_locomotive_modify_window())
        m -> Preme il tasto modifica locomotiva

        self.container.bind("<Return>", lambda event: self.GENERAL_STOP_START())
        Enter -> Ferma o avvia il sistema senza togliere la corrente
        '''

        #FRAME dei bottoni e del menu

        self.pack(side="bottom", pady=10)
        self.configure(bg="#c0c0c0")
        
        # impostazioni
        self.image_settings_path = utilities.asset_path('controllo','png')
        self.image_settings = utilities.process_image(self.image_settings_path, 'resize', 35, 35)
        self.settings_button = tk.Button(self.container, image= self.image_settings, bg="#c0c0c0", borderwidth=0, 
                                       command=self.open_settings_window)
        self.settings_button.pack(side="left", padx=(20,0),pady=(5,0))
        self.locomotive_settings_window = None
        self.container.bind("<s>", lambda event: self.open_settings_window())

        # Labels
        # Database Locomotive
        self.locomotive_label = tk.Label(self.container, text="DATABASE LOCOMOTIVE", bg="#c0c0c0", width=20)
        self.locomotive_label.pack(side="left",pady=(5,0), padx=(300,300))
        # self.locomotive_label.place(relx=0.5, rely=0.05, anchor="center")

        #Selezione lingua
        self.image_flag_Path = utilities.asset_path(f'{data.languages[0]}','png')
        self.image_flag = utilities.process_image(self.image_flag_Path, 'resize', 25, 20)
        self.var_language = tk.StringVar()
        self.flag_button = ttk.Menubutton(self.container, image=self.image_flag)
        self.flag = tk.Menu(self.flag_button, tearoff=0)
        self.flag_button.pack(side = "left")

    #stile del bottone per cambiare lingua e del suo menu, Assegno un valore ad ogni menubutton, seguendo il vettore data.languages
        self.style1 = ttk.Style()
        self.flag_button.config(style='Custom.TMenubutton')
        self.style1.configure('Custom.TMenubutton', background="#c0c0c0")
        self.style1.layout('Custom.TMenubutton', utilities.indicatoron)

        self.flag_button["menu"] = self.flag
        self.flag.delete(0, "end")
        for language in data.languages:
            self.flag.add_radiobutton(
                label=language,
                value=language,
                variable=self.var_language,
                command= self.change_language)

        #informazioni
        self.image_info_path = utilities.asset_path('info','png')
        self.image_info = utilities.process_image(self.image_info_path, 'resize', 45, 35)
        self.info_button = tk.Button(self.container, image= self.image_info, bg="#c0c0c0", borderwidth=0, 
                                       command=self.open_info_window)
        self.info_button.pack(side="left",  padx=(0,0),pady=(5,0))
        self.container.bind("<i>", lambda event: self.open_info_window())
        self.locomotive_info_window = None

        #Tabella
        self.columns = ("ID Locale", "ID Locomotive", "Colore", "Nome")
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(side='top')

        # Bottoni
        # Aggiungi locomotiva
        self.add_button = tk.Button(self, text="AGGIUNGI LOCOMOTIVA", height=2, width=20, 
                                    command=self.open_locomotive_creation_window)
        self.add_button.pack(side="left", padx=5)
        self.locomotive_creation_window = None
        self.container.bind("<plus>", lambda event: self.open_locomotive_creation_window())

        # Rimuovi locomotiva
        self.remove_button = tk.Button(self, text="RIMUOVI LOCOMOTIVA", height=2, width=20,
                                       command=self.open_locomotive_remove_window)
        self.remove_button.pack(side="left", padx=5)
        self.remove_button.config(state='disabled')
        self.locomotive_remove_window = None
        

        # Modifica locomotiva
        self.modify_button = tk.Button(self, text="MODIFICA LOCOMOTIVA", height=2, width=22,
                                       command=self.open_locomotive_modify_window)
        self.modify_button.pack(side="left", padx=5)
        self.modify_button.config(state='disabled')
        self.locomotive_modify_window = None
        

        # Controlla locomotiva
        self.image_control_path = utilities.asset_path('locomotiva','png')
        self.image_control = utilities.process_image(self.image_control_path, 'resize', 45, 35)
        self.var_locomotive = tk.StringVar()
        self.control_button = ttk.Menubutton(self, image=self.image_control)
        self.control = tk.Menu(self.control_button, tearoff=0)
        self.control_button.pack(side="left", padx=(100, 0))
        self.control_button.config(state='disabled')
        self.locomotive_control_window = []

    #stile del bottone controlla locomotiva e del suo menu
        self.style = ttk.Style()
        self.control_button.config(style='Custom.TMenubutton')
        self.style.configure('Custom.TMenubutton', background="#c0c0c0")
        self.style.layout('Custom.TMenubutton', utilities.indicatoron)
        

        # Circuit button
        self.image_path = utilities.asset_path('controller','png')
        self.image = utilities.process_image(self.image_path, 'resize', 35, 35)
        self.circuit_button = tk.Button(self, image=self.image, bg="#c0c0c0", borderwidth=0, 
                                        command=self.open_control)
        self.circuit_button.pack(side="left", padx=(10, 5))
        self.locomotive_circuit_window = None
        self.container.bind("<c>", lambda event: self.open_control())

        # Power button 
        self.image_power_path = utilities.asset_path('power_icon','png')
        self.image_power = utilities.process_image(self.image_power_path, 'resize', 35, 35)
        self.on_button = tk.Button(self, image=self.image_power, background="red", 
                                   command=self.on_off)
        self.on_button.pack(side="left", padx=5)
        self.container.bind("<o>", lambda event: self.on_off())

        # Stop generale
        self.STOP_button = tk.Button(self, text="STOP GENERALE", background="#f08080", height=2, width=15, 
                                    command=self.GENERAL_STOP_START)
        self.STOP_button.pack(side="left", padx=5)
        self.STOP_button.config(state='disabled')

        #Inserimento di max finestre nel locomotive control window in base al max_loco
        for i in range(data.max_loco):
            self.locomotive_control_window.append(None)
            data.variabili_apertura["locomotive_control_var"].append(False)

        #Fa riferimento alla pagina creata nel circuit, serve poiche quando chiamo la funzione dal circuit essa va a cercarla.
        self.locomotive_RFID_window = None
        
    '''
                    ___    _   _    ___   
            o O O  / __|  | | | |  |_ _|  
           o      | (_ |  | |_| |   | |   
          TS__[O]  \___|   \___/   |___|  
         {======|_|"""""|_|"""""|_|"""""| 
        ./o--000'"`-0-0-'"`-0-0-'"`-0-0-' 
    '''
   #Funzione che gestisce e semplifica la creazione dei TopLevel dell'applicazione.
    def open_locomotive_window(self, window_type : str, window_title: str, window_size: str, root):
        att = f'locomotive_{window_type}_window'
        window_var = getattr(self, att)
        data.variabili_apertura[f'locomotive_{window_type}_var'] = False # utilities.set_variabilechiusura(window_type)

        #Controllo per vedere se la finestra è gia aperta
        if window_var is None or not window_var.winfo_exists():
            window_var = tk.Toplevel(root)
            #Nasconde la finestra
            window_var.withdraw()
            if window_type == 'info':
                window_var.iconbitmap(utilities.asset_path("info", "ico"))
            elif window_type in ['settings', 'RFID']:
                window_var.iconbitmap(utilities.asset_path("controllo", "ico"))
            else: window_var.iconbitmap(utilities.asset_path("icon_control", "ico"))

            data.variabili_apertura[f'locomotive_{window_type}_var'] = True

            #Si setta l'attributo a window_var
            setattr(self, att, window_var)
            window_var.transient(root)
            window_var.protocol("WM_DELETE_WINDOW", lambda:utilities.on_close(window_var,window_type))
            
            #Seleziona la pagina appena creata
            window_var.focus_set()
            window_var.title(window_title)
            
            #Fissa le finestra in maniera relativa al padre
            width = self.winfo_rootx()
            height = self.winfo_rooty()

            window_var.tk.call('wm', 'geometry', window_var._w, f"{width}x{height}+{width-50}+{height-50}")
            window_var.geometry(window_size)
            window_var.update_idletasks()

            window_var.resizable(False, False)
            # window_var.transient(root)

            #Rende la finestra visibile di nuovo
            if not window_type == "circuit": window_var.deiconify()
            
            return window_var

        utilities.show_error_box(data.Textlines[20],window_var,"main")

    #Apre la pagina delle impostazioni
    def open_settings_window(self):
        locomotive_window = self.open_locomotive_window("settings", data.Textlines[11], "400x200",self.container)
        if locomotive_window:
            windows.settings_window(locomotive_window,self)

    #Apre la pagina della creazione locomotive
    def open_locomotive_creation_window(self):
        locomotive_window = self.open_locomotive_window("creation", data.Textlines[12], "250x170",self.container)
        if locomotive_window:
            windows.creation_window(locomotive_window,self)

    #Apre la pagina della rimozione locomotive      
    def open_locomotive_remove_window(self):
        locomotive_window = self.open_locomotive_window("remove", data.Textlines[13], "250x150",self.container)
        if locomotive_window:
            windows.remove_window(locomotive_window,self)

    #Apre la pagina della modifica locomotive
    def open_locomotive_modify_window(self):
        locomotive_window = self.open_locomotive_window("modify", data.Textlines[14], "300x200",self.container)
        if locomotive_window:
            windows.modify_window(locomotive_window,self)

    #Apre la pagina per controllare il circuito
    def open_control(self):

        open=True
                    
            
        #Nel caso in cui la seriale non sia collegata, si chiede all'utente se vuole continuare
        if not utilities.is_serial_port_available(self.serial_port):
            open = utilities.are_you_sure(data.Textlines[21] +f"{self.serial_port} " + data.Textlines[41],self)
        
        if open :
            #creazione di circuit per decidere il tipo di controllo del sistema
            locomotive_window = self.open_locomotive_window("circuit",data.Textlines[15], "1200x758",self.container)
            
            if locomotive_window:

                #Impostazioni di pagina, al premere del tasto ESC e al premere della x rossa, chiude la finestra, ferma l'algoritmo, toglie l'opacita e rilascia la pagina padre

                locomotive_window.bind("<Escape>", lambda event: (utilities.on_close(locomotive_window,"circuit"),
                                                                                self.container.algo.stop_algo(),
                                                                                # self.container.attributes("-alpha", 1),
                                                                                locomotive_window.grab_release(),
                                                                                ))
                #locomotive_circuit_window.transient(self.root)
                locomotive_window.protocol("WM_DELETE_WINDOW", lambda:(utilities.on_close(locomotive_window,"circuit"),
                                                                                    self.container.algo.stop_algo(),
                                                                                    # self.container.attributes("-alpha", 1),
                                                                                    locomotive_window.grab_release(),
                                                                                    ))
    
                locomotive_circuit_window1 = windows.circuit_window(locomotive_window,len(data.Turnouts),self.container,self)
                #Il parametro indica se è automatico o no
                locomotive_circuit_window1.open_circuit_window(False)

    #Apre la pagina per controllare locomotive    
    def open_locomotive_control(self):

        locomotiva      = self.var_locomotive.get()
        id_controllo    = utilities.CalcolaIDtreno('Nome',locomotiva)

        #Nel caso in cui la funzione viene chiamata da tastiera, l'impostazione dell'id avviene dalla funzione set_var_keypress_locomotive_control
        if id_controllo is None:
            id_controllo = data.var_supporto
            locomotiva   = data.locomotives_data[id_controllo]['Nome'] 


        if self.locomotive_control_window[id_controllo] is None or not self.locomotive_control_window[id_controllo].winfo_exists():
            #Apri solo se il button è sullo stato normal, non si puo togliere il print(self.control_button['state']), 
            # Equivale a questo : self.control_button['state'] == 'normal'
            if self.on_button.cget("background") == "#00ff00":
                #Creazione della finestra di controllo
                data.variabili_apertura["locomotive_control_var"][id_controllo] = True
                self.locomotive_control_window[id_controllo] = tk.Toplevel(self.container)
                self.locomotive_control_window[id_controllo].transient(self.container)
                self.locomotive_control_window[id_controllo].iconbitmap(utilities.asset_path('icon_control','ico'))
                self.locomotive_control_window[id_controllo].protocol("WM_DELETE_WINDOW", lambda:utilities.on_close(self.locomotive_control_window[id_controllo],f"{id_controllo}"))

                #Seleziona la pagina appena creata
                self.locomotive_control_window[id_controllo].focus_set()
                self.locomotive_control_window[id_controllo].title(locomotiva)
                self.locomotive_control_window[id_controllo].geometry("300x250")
                self.locomotive_control_window[id_controllo].resizable(False, False)


                windows.control_window(self.locomotive_control_window[id_controllo],self,locomotiva,id_controllo)

        else:
            utilities.show_error_box(data.Textlines[20],self.locomotive_control_window[id_controllo],"main")

    def open_info_window(self):

        #Creazione della finestra per le informazioni
        locomotive_window = self.open_locomotive_window("info", data.Textlines[16], "600x400",self.container)
        if locomotive_window:

            #Serie di informazioni sull'applicazione
            info_text = (
                    data.Textlines[100] +     "\n\n\n"
                    "1. "+data.Textlines[101]+"\n\n"
                    " - "+data.Textlines[102]+"\n\n"
                    " - "+data.Textlines[103]+"\n\n\n"
                    "2. "+data.Textlines[104]+"\n\n"
                    " - "+data.Textlines[105]+"\n\n"
                    " - "+data.Textlines[106]+"\n\n"
                    " - "+data.Textlines[107]+"\n\n"
                    " - "+data.Textlines[108]+"\n\n"
                    " - "+data.Textlines[109]+"\n\n"
                    " - "+data.Textlines[110]+"\n\n"
                    " - "+data.Textlines[111]+"\n\n"
                    " - "+data.Textlines[112]+"\n\n"
                    " - "+data.Textlines[113]
                )
            
            label_title = tk.Label(locomotive_window, text=data.Textlines[114], font=('Helvetica', 14, 'bold'))
            label_title.pack(pady=10)
            
            text = tk.Text(locomotive_window, wrap='word', width=60, height=20)
            text.insert(tk.END, info_text)
            text.config(state='disabled')
            text.pack(padx=10, pady=5)
            
            locomotive_window.transient(self.container)

            #Comandi da tastiera e x rossa
            locomotive_window.protocol("WM_DELETE_WINDOW", lambda: locomotive_window.destroy())
            locomotive_window.bind('<Return>', lambda event: locomotive_window.destroy())
            locomotive_window.bind("<Escape>", lambda event: locomotive_window.destroy())

            close_button = tk.Button(locomotive_window, text=data.Textlines[43], command=locomotive_window.destroy)
            close_button.pack(pady=10)
        
    #funzione che serve per la gestione del bottone ON/OFF della corrente
    def on_off(self):
        current_color = self.on_button.cget("background")

        #controlla se la seriale è collegata correttamente
        if utilities.is_serial_port_available(self.serial_port):
            on_offButton = buttons.Buttons(current_color)
            on_offButton.on_off(self)

        else:
            utilities.show_error_box(data.Textlines[21] +f"{self.serial_port} " + data.Textlines[22],self,"main")


    #funzione che serve per la gesetione dell'avvio e dell'arresto del sistema senza togliere la corrente
    def GENERAL_STOP_START(self):
        print("A")
        current_color       = self.STOP_button.cget("background")
        
        if utilities.is_serial_port_available(self.serial_port):
            STOP_button = buttons.Buttons(current_color)
            STOP_button.GENERAL_STOP_START_button(self)
           
        else:
            utilities.show_error_box(data.Textlines[21] +f"{self.serial_port} " + data.Textlines[22],self,"main")
        
    #Funzione che gestisce lo stato dei bottoni nella pagina principale
    def check_control_button_state(self):
        if data.locomotives_data:
            self.remove_button.config(state='normal')
            self.container.bind("<minus>", lambda event: self.open_locomotive_remove_window())

            self.modify_button.config(state='normal')
            self.container.bind("<m>", lambda event: self.open_locomotive_modify_window())
            if self.on_button.cget("background") == "#00ff00":
                self.control_button.config(state='normal')
                print("B")
                self.STOP_button.config(state='normal')
                self.container.bind("<Return>", lambda event: self.GENERAL_STOP_START())
            else:
                self.control_button.config(state='disabled')

                self.STOP_button.config(state='disabled')
                self.container.unbind("<Return>")
        else:
            self.control_button.config(state='disabled')

            self.remove_button.config(state='disabled')
            self.container.unbind("<minus>")
            self.modify_button.config(state='disabled')
            self.container.unbind("<m>")
        
    #funzione per aggioranre la tabella - all'interno c'è anche la funzione che gestisce il menu a tendina del controllo
    def update_table(self):
        
        # Pulizia della tabella
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Riempimento della tabella con i dati delle locomotive
        for locomotive in data.locomotives_data:
            self.tree.insert('', tk.END, values=(
                locomotive['ID'],
                locomotive['LocoID'],
                data.colors[locomotive['Colore']],
                locomotive['Nome']
            ),tags=('color'))
            if locomotive['RFIDtag'] == "":
                data.calibred = False

        self.tree.tag_configure('color', background='#EDEDED')

        for col in self.columns:
            self.tree.column(col, anchor='center')  # Imposta l'allineamento al centro per tutte le colonne


        self.locomotive_names = [locomotive['Nome'] for locomotive in data.locomotives_data]
        self.check_control_button_state()
        
        self.control_button["menu"] = self.control
        self.control.delete(0, "end")

        #Riordinando il dizionario locomotives_data, ad ogni id assegna il tasto corrispondente
        #Questo ciclo for itera su ogni elemento della lista self.locomotive_names. La funzione enumerate() ottiene una coppia di valori durante l'iterazione: l'indice dell'elemento e l'elemento stesso.
        # start=1: Questo parametro opzionale specifica da quale indice iniziare la numerazione degli indici. L'indice inizia da 1 anziché da 0.
        #Questo permette di eseguire operazioni sull'elemento e sull'indice contemporaneamente durante l'iterazione.
        for id, loco in enumerate(self.locomotive_names, start=1):
            # Costruisci il pattern del tasto da associare
            key_pattern = "<KeyPress-{}>".format(id) if id < 10 else "<Control-KeyPress-{}>".format(id - 10)

            # Controlla se il tasto non ha già una funzione associata
            if not self.container.bind(key_pattern):
                self.container.bind(key_pattern, lambda event, loco_id=id: (self.set_var_keypress_locomotive_control(loco_id), self.open_locomotive_control()))
            
            #Aggiorna il menubutton con le locomotive inserite
            self.control.add_radiobutton(
                label=loco,
                value=loco,
                variable=self.var_locomotive,
                command= self.open_locomotive_control)
            
        if len(self.locomotive_names) == data.max_loco_standard: utilities.show_info(data.Textlines[23],self)
            
    #Aiuta la gestione dei tasti per aprire la pagina di controllo relativa alla locomotiva
    def set_var_keypress_locomotive_control(self,id):
        id_controllo = utilities.CalcolaIDtreno('ID',id)
        data.var_supporto = id_controllo
        print(id)

    #Funzione che permette di tradurre tutti i testi visibili all'interno dell'app
    def change_language(self):
        language      = self.var_language.get()
        if language != data.languages[0] and utilities.are_you_sure(data.Textlines[66],self):
            # Identifica l'indice della stringa nel vettore
            index = data.languages.index(language)
            # Rimuovi la stringa dal suo attuale indice
            data.languages.pop(index)
            # Inserisci la stringa nella prima posizione del vettore
            data.languages.insert(0, language)
            #Traduce il file inserito nella prima posizione
            utilities.translate()

            #Aggiorna la pagina con la nuova lingua inserita
            self.container.refresh()
            self.refresh()
            self.update_table()

    #Funzione che serve per aggiornare la lingua della pagina principale
    def refresh(self):
        #Prendo tutti i widget della pagina
        children = self.container.winfo_children()

        for child in children:
             # Chiudi solo le finestre Toplevel
            if isinstance(child, tk.Toplevel):
                child.destroy()

        #Cambio il nome dei label nella lingua giusta, anche il link dell'immagine
        self.locomotive_label.configure(text=data.Textlines[2])
        
        #cambio il nome delle colonne della tabella
        self.columns = (data.Textlines[3], data.Textlines[4], data.Textlines[5], data.Textlines[80])
        self.tree['columns'] = self.columns

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')

        #Aggiornamento dei labels
        self.add_button.configure(text=data.Textlines[7])
        self.remove_button.configure(text=data.Textlines[8])
        self.modify_button.configure(text=data.Textlines[9])
        self.STOP_button.configure(text=data.Textlines[10])
        self.image_flag_Path = utilities.asset_path(f'{data.languages[0]}','png')
        self.image_flag = utilities.process_image(self.image_flag_Path, 'resize', 25, 20)
        self.flag_button.configure(image=self.image_flag)

