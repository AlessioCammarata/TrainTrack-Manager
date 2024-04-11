import tkinter as tk
import GUI_refactored
import utilities
import data
from algorithm import Algorithm

utilities.translate("EN")
# @singleton
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #Specifiche del root - style e icon
        self.title(data.Textlines[1])
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close_root)

        self.iconbitmap(utilities.asset_path("window_logo", "ico"))
        self.configure(bg="#c0c0c0")
        
        #creazione dell'oggetto algo, mi serve la GUI
        self.algo = Algorithm()

    def on_close_root(self):
        self.destroy()
        self.algo.stop_algo()
        

if __name__ == "__main__":

    app = App()
    gui = GUI_refactored.GUI(app)
    app.mainloop()