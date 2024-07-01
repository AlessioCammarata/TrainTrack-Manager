import tkinter as tk
import GUI_refactored
import utilities
import data
from algorithm import Algorithm
import os
import platform

# @singleton
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #Specifiche del root - style e icon
        self.title("Gestione Locomotive")
        self.resizable(False, False)
        self.geometry("900x335")

        self.iconbitmap(utilities.asset_path("window_logo", "ico"))
        self.configure(bg="#c0c0c0")
        
        #creazione dell'oggetto algo, mi serve la GUI
        self.algo = Algorithm()

    def on_close_root(self):
        self.destroy()
        self.algo.stop_algo(True)

    def refresh(self):
        self.title(data.Textlines[1])

def setup():
    
    #Ottengo il nome del sistema operativo
    sistema_operativo = platform.system()
    if sistema_operativo == "Darwin": sistema_operativo = "macOS"
    
    data.SO = sistema_operativo
    data.architecture = platform.machine()
    
    print(sistema_operativo)
    #cerco la dir attuale e Salvo la parent dir attuale in data - MISERVERUNPEZZOINPIUPERILTESTING
    folder_path = os.path.abspath(os.path.join(os.getcwd(),'interfaccia_grafica'))
    
    # SOLO DURANTE IL FILE ESECUTIVO
    # parent_directory = os.path.dirname(os.path.dirname(folder_path))
    # data.path = parent_directory
    data.path = folder_path

    #Aggiorno la lingua, con quella standard+.
    utilities.translate()
    
    #Assegnazione diretta standard del nome della prima porta
    data.name = data.Textlines[98] #Sconosciuto

    #Aggiorno le porte collegate nel caso in cui ci siano
    utilities.set_port_var()

    return True

if __name__ == "__main__" and setup():

    app = App()
    gui = GUI_refactored.GUI(app)
    app.mainloop()