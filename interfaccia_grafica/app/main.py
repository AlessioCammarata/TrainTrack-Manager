import tkinter as tk
import GUI_refactored
import utilities
import data
from algorithm import Algorithm
import os

# @singleton
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #Specifiche del root - style e icon
        self.title("Gestione Locomotive")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close_root)

        self.iconbitmap(utilities.asset_path("window_logo", "ico"))
        self.configure(bg="#c0c0c0")
        
        #creazione dell'oggetto algo, mi serve la GUI
        self.algo = Algorithm()

    def on_close_root(self):
        self.destroy()
        self.algo.stop_algo()

    def refresh(self):
        self.title(data.Textlines[1])


if __name__ == "__main__":
    #cerco la dir attuale e Salvo la parent dir attuale in data - MISERVERUNPEZZOINPIUPERILTESTING
    folder_path = os.path.abspath(os.path.join(os.getcwd()))
    
    # SOLO DURANTE IL FILE ESECUTIVO
    # parent_directory = os.path.dirname(os.path.dirname(folder_path))
    # data.path = parent_directory
    data.path = folder_path

    utilities.translate()
    app = App()
    gui = GUI_refactored.GUI(app)
    app.mainloop()