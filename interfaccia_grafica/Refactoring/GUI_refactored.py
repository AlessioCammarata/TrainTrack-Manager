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
        self.container.bind("<FocusIn>", lambda event: self.container.focus_set())
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

        #ROOT principale

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
        self.locomotive_label = tk.Label(self.container, text=data.Textlines[2], bg="#c0c0c0")
        self.locomotive_label.pack(side="left",pady=(5,0), padx=(300,300))
        # self.locomotive_label.place(relx=0.5, rely=0.05, anchor="center")

        #Selezione lingua
        self.image_flag_Path = utilities.asset_path(f'{data.languages[0]}','png')
        self.image_flag = utilities.process_image(self.image_flag_Path, 'resize', 25, 20)
        self.var_language = tk.StringVar()
        self.flag_button = ttk.Menubutton(self.container, image=self.image_flag)
        self.flag = tk.Menu(self.flag_button, tearoff=0)
        self.flag_button.pack(side = "left")

    #stile del bottone controlla locomotiva e del suo menu
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
        self.info_button.pack(side="left", padx=(0,0),pady=(5,0))
        self.container.bind("<i>", lambda event: self.open_info_window())

        #Tabella
        self.columns = (data.Textlines[3], data.Textlines[4], data.Textlines[5], data.Textlines[6])
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(side='top')

        # Bottoni
        # Aggiungi locomotiva
        self.add_button = tk.Button(self, text=data.Textlines[7], height=2, 
                                    command=self.open_locomotive_creation_window)
        self.add_button.pack(side="left", padx=5)
        self.locomotive_creation_window = None
        self.container.bind("<plus>", lambda event: self.open_locomotive_creation_window())

        # Rimuovi locomotiva
        self.remove_button = tk.Button(self, text=data.Textlines[8], height=2, 
                                       command=self.open_locomotive_remove_window)
        self.remove_button.pack(side="left", padx=5)
        self.remove_button.config(state='disabled')
        self.locomotive_remove_window = None
        

        # Modifica locomotiva
        self.modify_button = tk.Button(self, text=data.Textlines[9], height=2, 
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
        self.STOP_button = tk.Button(self, text=data.Textlines[10], background="#f08080", height=2, width=15, 
                                    command=self.GENERAL_STOP_START)
        self.STOP_button.pack(side="left", padx=5)
        self.STOP_button.config(state='disabled')
        

        #self.on_offButton = buttons.Buttons()

        #Inserimento di max finestre nel locomotive control window in base al max_loco
        for i in range(data.max_loco):
            self.locomotive_control_window.append(None)
            data.variabili_apertura["locomotive_control_var"].append(False)

        #Fa riferimento alla pagina creata nel circuit
        self.locomotive_RFID_window = None
    '''
                    ___    _   _    ___   
            o O O  / __|  | | | |  |_ _|  
           o      | (_ |  | |_| |   | |   
          TS__[O]  \___|   \___/   |___|  
         {======|_|"""""|_|"""""|_|"""""| 
        ./o--000'"`-0-0-'"`-0-0-'"`-0-0-' 
    '''

    def open_locomotive_window(self, window_type : str, window_title: str, window_size: str, root):
        att = f'locomotive_{window_type}_window'
        window_var = getattr(self, att)
        data.variabili_apertura[f'locomotive_{window_type}_var'] = False # utilities.set_variabilechiusura(window_type)

        if window_var is None or not window_var.winfo_exists():
            window_var = tk.Toplevel(root)
            data.variabili_apertura[f'locomotive_{window_type}_var'] = True
            #if necessario, la control è gestita tramite un vettore
            if att == 'locomotive_control_window':
                self.locomotive_control_window[window_type] = window_var
            else:
                setattr(self, att, window_var)
            window_var.transient(root)
            window_var.protocol("WM_DELETE_WINDOW", lambda:utilities.on_close(window_var,window_type))

            #Seleziona la pagina appena creata
            window_var.focus_set()

            return windows.Windows(window_var, window_title, window_size)

        utilities.show_error_box(data.Textlines[20], "focus_page/_", window_var)

    def open_settings_window(self):
        locomotive_window = self.open_locomotive_window("settings", data.Textlines[11], "400x200",self.container)
        if locomotive_window:
            locomotive_window.settings_window(self)

    def open_locomotive_creation_window(self):
        locomotive_window = self.open_locomotive_window("creation", data.Textlines[12], "250x170",self.container)
        if locomotive_window:
            locomotive_window.creation_window(self)
            
    def open_locomotive_remove_window(self):
        locomotive_window = self.open_locomotive_window("remove", data.Textlines[13], "250x150",self.container)
        if locomotive_window:
            locomotive_window.remove_window(self)

    def open_locomotive_modify_window(self):
        locomotive_window = self.open_locomotive_window("modify", data.Textlines[14], "300x200",self.container)
        if locomotive_window:
            locomotive_window.modify_window(self)

    def open_control(self):
        #global locomotive_circuit_window
        
        if self.locomotive_circuit_window is None or not self.locomotive_circuit_window.winfo_exists():
            open=True
            #Setto la variabile a False poiche serve per creare i deviatoi una volta sola, all'interno del codice la setto a True dopo la prima esecuzione
            data.variabili_apertura["locomotive_circuit_var"] = False
            
            #Nel caso in cui la seriale non sia collegata, si chiede all'utente se vuole continuare
            if not utilities.is_serial_port_available(self.serial_port):
                open = utilities.are_you_sure(data.Textlines[21] +f"{self.serial_port} " + data.Textlines[41])
            
            if open:
                #creazione di circuit per decidere il tipo di controllo del sistema
                self.locomotive_circuit_window = tk.Toplevel(self.container)
                self.locomotive_circuit_window.bind("<Escape>", lambda event: (utilities.on_close(self.locomotive_circuit_window,"circuit"),
                                                                                self.container.algo.stop_algo(),
                                                                                self.container.attributes("-alpha", 1),
                                                                                self.locomotive_circuit_window.grab_release(),
                                                                                ))
                #locomotive_circuit_window.transient(self.root)
                self.locomotive_circuit_window.protocol("WM_DELETE_WINDOW", lambda:(utilities.on_close(self.locomotive_circuit_window,"circuit"),
                                                                                    self.container.algo.stop_algo(),
                                                                                    self.container.attributes("-alpha", 1),
                                                                                    self.locomotive_circuit_window.grab_release(),
                                                                                    ))
                #Seleziona la pagina appena creata
                self.locomotive_circuit_window.focus_set()

                locomotive_circuit_window1 = windows.circuit_window(self.locomotive_circuit_window,data.Textlines[15],len(data.Turnouts),self.container,self)
                locomotive_circuit_window1.open_circuit_window(False)

        else: 
            utilities.show_error_box(data.Textlines[20],"focus_page/_",self.locomotive_circuit_window)
    
    def open_locomotive_control(self):
        #global locomotive_control_window

        locomotiva      = self.var_locomotive.get()
        id_controllo    = utilities.CalcolaIDtreno('Nome',locomotiva)

        if id_controllo is None:
            id_controllo = data.var_supporto
            locomotiva   = data.locomotives_data[id_controllo]['Nome'] 


        

        if self.locomotive_control_window[id_controllo] is None or not self.locomotive_control_window[id_controllo].winfo_exists():
            #Apri solo se il button è sullo stato normal, non si puo togliere il print
            print(self.control_button['state'])
            if self.control_button['state'] == 'normal':
                data.variabili_apertura["locomotive_control_var"][id_controllo] = True
                self.locomotive_control_window[id_controllo] = tk.Toplevel(self.container)
                self.locomotive_control_window[id_controllo].transient(self.container)
                self.locomotive_control_window[id_controllo].iconbitmap(utilities.asset_path('icon_control','ico'))
                self.locomotive_control_window[id_controllo].protocol("WM_DELETE_WINDOW", lambda:utilities.on_close(self.locomotive_control_window[id_controllo],f"{id_controllo}"))

                #Seleziona la pagina appena creata
                self.locomotive_control_window[id_controllo].focus_set()

                locomotive_control_window1 = windows.Windows(self.locomotive_control_window[id_controllo],locomotiva,"300x250")
                locomotive_control_window1.control_window(self,locomotiva,id_controllo)

        else:
            utilities.show_error_box(data.Textlines[20],"focus_page/_",self.locomotive_control_window[id_controllo])

    def open_info_window(self):
        info_text = data.Textlines[60] + "\n" + data.Textlines[61] + "\n"+ data.Textlines[62] +"\n"+ data.Textlines[63]
        info_window = tk.Toplevel(self)
        #Seleziona la pagina appena creata
        info_window.focus_set()
        info_window.title(data.Textlines[16])
        info_window.geometry("275x150")
        info_window.transient(self)

        info_window.protocol("WM_DELETE_WINDOW", lambda: info_window.destroy())
        info_window.bind('<Return>', lambda event: info_window.destroy())
        info_window.bind("<Escape>", lambda event: info_window.destroy())

        label = tk.Label(info_window, text=info_text)
        label.pack(padx=5, pady=10)

        close_button = tk.Button(info_window, text=data.Textlines[43], command=info_window.destroy)
        close_button.pack(pady=10)

    #funzione che serve per la gestione del bottone ON/OFF della corrente
    def on_off(self):
        current_color = self.on_button.cget("background")

        #controlla se la seriale è collegata correttamente
        if utilities.is_serial_port_available(self.serial_port):
            on_offButton = buttons.Buttons(current_color)
            on_offButton.on_off(self)

        else:
            utilities.show_error_box(data.Textlines[21] +f"{self.serial_port} " + data.Textlines[22],"focus_page/_",self.container)


    #funzione che serve per la gesetione dell'avvio e dell'arresto del sistema senza togliere la corrente
    def GENERAL_STOP_START(self):
        print("A")
        current_color       = self.STOP_button.cget("background")
        
        if utilities.is_serial_port_available(self.serial_port):
            STOP_button = buttons.Buttons(current_color)
            STOP_button.GENERAL_STOP_START_button(self)
           
        else:
            utilities.show_error_box(data.Textlines[21] +f"{self.serial_port} " + data.Textlines[22],"focus_page/_",self.container)
        

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
                locomotive['Colore'],
                locomotive['Nome']
            ),tags=('color'))

        self.tree.tag_configure('color', background='#EDEDED')

        for col in self.columns:
            self.tree.column(col, anchor='center')  # Imposta l'allineamento al centro per tutte le colonne


        self.locomotive_names = [locomotive['Nome'] for locomotive in data.locomotives_data]
        self.check_control_button_state()
        
        self.control_button["menu"] = self.control
        self.control.delete(0, "end")
        i=0
        #Forse si puo ottimizzare
        for loco in self.locomotive_names:
            # index   = utilities.CalcolaIDtreno('Nome',loco)
            #id      = database.locomotives_data[i]['ID']
            #Basta cosi, se riordino il dizionario locomotives_data
            id = i+1
            #Se il tasto non ha funzioni associati, entra - Forse si puo scrivere meglio
            if not self.container.bind("<KeyPress-{}>".format(id)):
                if id < 10:
                    self.container.bind("<KeyPress-{}>".format(id), lambda event: (self.set_var_keypress_locomotive_control(id),self.open_locomotive_control()))
                elif id < 20:
                    if not self.container.bind("<Control-KeyPress-{}>".format(id-10)):
                        self.container.bind("<Control-KeyPress-{}>".format(id-10), lambda event: (self.set_var_keypress_locomotive_control(id),self.open_locomotive_control()))
                else:
                    utilities.show_error_box(data.Textlines[23],"close_window/locomotive_creation_var","")
            i+=1
            self.control.add_radiobutton(
                label=loco,
                value=loco,
                variable=self.var_locomotive,
                command= self.open_locomotive_control)

    #Aiuta la gestione dei tasti per aprire la pagina di controllo relativa alla locomotiva
    def set_var_keypress_locomotive_control(self,id):
        id_controllo = utilities.CalcolaIDtreno('ID',id)
        data.var_supporto = id_controllo
        print(id)

    def change_language(self):
        language      = self.var_language.get()
        if utilities.are_you_sure("CANCELLO TUTTO??"):
            #utilities.translate(language)
            self.container.on_close_root()
            # Identifica l'indice della stringa nel vettore
            index = data.languages.index(language)
            # Rimuovi la stringa dal suo attuale indice
            data.languages.pop(index)
            # Inserisci la stringa nella prima posizione del vettore
            data.languages.insert(0, language)
            print(data.languages)
            self.after(20,self.container.reopen_window())