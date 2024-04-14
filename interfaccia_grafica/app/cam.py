import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

'''

                ___                   
        o O O  / __|   __ _    _ __   
       o      | (__   / _` |  | '  \  
      TS__[O]  \___|  \__,_|  |_|_|_| 
     {======|_|"""""|_|"""""|_|"""""| 
    ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'

'''

class Camera:
    def __init__(self,root):
        self.root = root
        self.impostazioni = ["",""]
        self.tk_img = None
        self.width = 400
        self.height = 300

    def cattura_webcam(self,open):

        def mostra_frame():

            # Leggi il frame dalla webcam
            ret, frame = cap.read()
            # Converti il frame da BGR a RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hsv = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2HSV)
            # Definisci gli intervalli di colori da individuare per rosso, verde e blu
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([20, 255, 255])

            # lower_green = np.array([40, 40, 40])
            # upper_green = np.array([80, 255, 255])

            lower_blue = np.array([100, 50, 50])
            upper_blue = np.array([140, 255, 255])

            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])


            # Crea le maschere per i colori
            mask_red = cv2.inRange(hsv, lower_red, upper_red)
            # mask_green = cv2.inRange(rgb_frame, lower_green, upper_green)
            mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
            mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

            # Combina le maschere
            # mask_combined = cv2.bitwise_or(mask_red, cv2.bitwise_or(mask_green, mask_blue))
            mask_combined = cv2.bitwise_or(mask_red, mask_blue , cv2.bitwise_not(mask_yellow))

            # Applica la maschera combinata al frame originale
            result = cv2.bitwise_and(rgb_frame, rgb_frame, mask=mask_combined)

            # Converte l'array NumPy in un oggetto immagine di PIL
            pil_img = Image.fromarray(result)
            pil_img = pil_img.resize((self.width, self.height), Image.BILINEAR)


            # Converte l'oggetto immagine PIL in un oggetto immagine Tkinter
            self.tk_img = ImageTk.PhotoImage(image=pil_img)

            # Mostra l'immagine sulla canvas
            canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
            canvas.img = self.tk_img  # Mantieni un riferimento all'oggetto PhotoImage per evitare la garbage collection

            # Richiama questa funzione ogni 10 millisecondi
            canvas.after(10, mostra_frame)

        def chiudi_finestra_webcam(cap,canvas):
            cap.release()
            canvas.destroy()
            print("CANVA destroyed")

        self.tk_img = None

        if open == "chiudi":
            chiudi_finestra_webcam(self.impostazioni[1],self.impostazioni[0])
            self.impostazioni = ["",""]
        else:
            cap = cv2.VideoCapture(0)
            self.impostazioni[1] = cap
            #controllo sulla presenza di una cam
            if not self.impostazioni[1].isOpened():
                return False
            else:
                if open == "esiste":
                    self.impostazioni[1].release()
                    return True
                
                canvas = tk.Canvas(self.root, width=self.width, height=self.height)
                canvas.pack(anchor=tk.NW)
                self.impostazioni[0] = canvas
                # Chiama la funzione per mostrare il frame
                mostra_frame()
                # Esegui la finestra Tkinter
                self.root.mainloop()
                # Rilascia il dispositivo di acquisizione video quando la finestra Tkinter è chiusa
                cap.release()

