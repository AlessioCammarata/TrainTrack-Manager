import tkinter as tk
import app.GUI_refactored as GUI_refactored
import app.utilities as utilities
import app.data as data
from app.algorithm import Algorithm
import os
import platform


#            __  __             _            
#      o O O|  \/  |  __ _     (_)    _ _    
#     o     | |\/| | / _` |    | |   | ' \   
#    TS__[O]|_|__|_| \__,_|   _|_|_  |_||_|  
#   {======|_|"""""|_|"""""|_|"""""|_|"""""| 
#  ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'


# @singleton
class App(tk.Tk):
    """
# APP

The app class is useful to create the root page. In these class you define the parameters of the root window.\n
Inside this class you can call 2 different method

    """
    def __init__(self):
        """
        - This is the constructor of the App Class\n 
          Here are defined the specific of the root window as the icon or the window-size.\n\n
          Furthermore an instance of algorithm is created because it is necessary to free the serial ports at the end of execution. 
        """
        super().__init__()

        #Specifiche del root - style e icon
        self.title("Gestione Locomotive")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close_root)
        self.geometry("900x335")

        self.iconbitmap(utilities.asset_path("window_logo", "ico"))
        self.configure(bg="#c0c0c0")
        
        #creazione dell'oggetto algo, mi serve la GUI
        self.algo = Algorithm()

    def on_close_root(self):
        """- This function is useful to **close the root window and to stop the algorithm** if it was started."""
        self.destroy()
        self.algo.stop_algo()

    def refresh(self):
        """- This function is useful to **refresh** the page when a language change occurs."""
        self.title(data.Textlines[1])


def setup():
    """
    - During the **setup** function are determined some important depndencies like the current path of the project, the current SO and processor architecture and also the current language \n 
      which is standard set on italian language. Moreover if you have connected the serial ports of your arduino devices, they are automatically connected and setted into the data cache.\n
      If you want to modify the latter, just go to the settings and set the configuration according to your needs.
    """
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
    # utilities.get_name_arduino("COM7")
    
    #Aggiorno le porte collegate nel caso in cui ci siano
    print(utilities.set_port_var())

    return True

if __name__ == "__main__" and setup():

    app = App()
    gui = GUI_refactored.GUI(app)
    app.mainloop()