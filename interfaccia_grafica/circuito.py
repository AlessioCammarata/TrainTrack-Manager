'''
The purpose of this file is to create a viosual idea of the system.
With these lines of code you could be able to see what is oing on on the system, in every sector of the system,
You can be capable to choose if you want to control the system with the manual feature or with the automatized feature.
The first implies the control of every switch on the system and also the locomotives would stop or go only if they receive the command from the user,
With the second feature the sytem would became automatic, so locomotives on the system within the help of the sensors in the circuit, will go on or stop automatically.
'''

import tkinter as tk
# from PIL import Image, ImageTk
import function
import comandi
import test_cam
import algorithm
import time

nscambi= len(function.Turnouts)
#controlloCam = test_cam.cattura_webcam("","esiste")

def open_control_window(automatico,window):


        # # Funzione per gestire il click del mouse su un segmento del circuito
        # def segment_clicked(event):
        #     # Ottenere le coordinate del click del mouse
        #     x, y = event.x, event.y
            
        #     # Esempio di come gestire il click su un segmento specifico
        #     # Verifica se il click è avvenuto in diverse zone del semicer1chio
        #     if 150 <= x <= 250 and 50 <= y <= 150:
        #         print("Zona 1 cliccata")
        #     elif 100 <= x <= 300 and 150 <= y <= 200:
        #         print("Zona 2 cliccata")
        #     # Aggiungi altre condizioni per le altre zone del semicerchio...

    # #Funzione per cambiare i deviatoi
    #     def change_Turnouts(text,button):
    #         #gestione grafica degli scambi
    #         current_color = button.cget("background")
    #         new_color = "#8fbc8f" if current_color == "#f08080" else "#f08080"
    #         new_text = "/" if current_color == "#f08080" else "|"
    #         button.config(background=new_color,text=new_text)

    #         comandi.cambia_deviatoio(function.Turnouts[text][1])

    #         #print("fuori ",Turnouts[text][1])
    #         if not function.Turnouts[text][0]:
    #             function.change_color(text,function.Turnouts[text][0])
    #             function.Turnouts[text][0] = True
              
    #         else:
    #             function.controlla_scambi_doppi(text)
    #             function.Turnouts[text][0] = False 
                    
    # #Funzione che controlla se lo scambio_doppio è selezionato da almeno 1 dei due, se è cosi non cambia il centrale ma l'altro, senno lo cambia
    #     def controlla_scambi_doppi(text):
    #         if function.Turnouts[text][3] == function.Turnouts['Cambio 4'][3]:
    #             #qui siamo entrati sia nel caso in cui text è 4 sia se è 8
    #             if function.Turnouts['Cambio 4'][0] and function.Turnouts['Cambio 8'][0]:
    #                 #dato che una è una curva e l'altra è un segmento, bisogna specificare il caso
    #                 if text == 'Cambio 4':
    #                     canvas.itemconfig(function.Turnouts[text][2], fill="red")
    #                 else:
    #                     canvas.itemconfig(function.Turnouts[text][2], outline="red")
    #             else:
    #                 #nel caso in cui non siano entrambi attivi, esegue semplicemente la funzione
    #                 function.change_color(canvas,text,function.Turnouts[text][0])
                
    #         elif function.Turnouts[text][3] == function.Turnouts['Cambio 6'][3]:
    #             #qui siamo entrati sia nel caso in cui text è 6 sia se è 7
    #             if function.Turnouts['Cambio 6'][0] and function.Turnouts['Cambio 7'][0]:
    #                 #dato che sono entrambe curve basta un solo comando, non si cambia quello comune
    #                 canvas.itemconfig(function.Turnouts[text][2], outline="red")
    #             else:
    #                 #nel caso in cui non siano entrambi attivi, esegue semplicemente la funzione
    #                 function.change_color(canvas,text,function.Turnouts[text][0])
    #         else:
    #             #nel caso in cui non siano tra gli scambi doppi, esegue semplicemente la funzione
    #             function.change_color(canvas,text,function.Turnouts[text][0])

    # #Funzione che ccambia il colore dello0 scambio in base a come è nel circuito
    #     def change_color(text,activated):
    #         if text not in {'Cambio 3', 'Cambio 4', 'Cambio 5'}:
    #             #Se il cambio è fromato da 2 curve
    #             if activated:
    #                 canvas.itemconfig(function.Turnouts[text][2], outline="red")
    #                 canvas.itemconfig(function.Turnouts[text][3], outline="black")   
    #             else:
    #                 canvas.itemconfig(function.Turnouts[text][3], outline="red")
    #                 canvas.itemconfig(function.Turnouts[text][2], outline="black")
    #         else:
    #             #Se il cambio è fromato da 1 curva ed un segmento
    #             if activated:
    #                 canvas.itemconfig(function.Turnouts[text][2], fill="red")
    #                 canvas.itemconfig(function.Turnouts[text][3], outline="black")
    #             else:
    #                 canvas.itemconfig(function.Turnouts[text][3], outline="red")
    #                 canvas.itemconfig(function.Turnouts[text][2], fill="black")



    #funzione che gestisce il bottone che attiva la webcam
        def change_color_webcam():
            current_color = webcam.cget("background")
            new_color = "green" if current_color == "blue" else "blue"
            new_text = "VIDEO ON" if current_color == "blue" else "VIDEO OFF"
            
            if current_color == "blue" :
                controlloCam = test_cam.cattura_webcam("","esiste")
                if controlloCam:
                    webcam.config(background=new_color,text=new_text)
                    test_cam.cattura_webcam(root,"")
                else:
                    function.show_error_box("Collega una videocamera","focus_page/_",root)
            else:
                webcam.config(background=new_color,text=new_text)
                test_cam.cattura_webcam(root,"chiudi")

    #funzione che gestisce il cambio da manuale a automatico
        def change_window(text,root):
            #root.destroy()
            #controllo per effettuare correttamente il cap.release
            if text=="MANUALE" and test_cam.impostazioni[0]!="": 
                test_cam.cattura_webcam(root,"chiudi")
            #Distrugge tutti i widget presenti nella pagina corrente
            for widget in root.winfo_children():
                widget.destroy()
            #avvia la pagina selezionata
            if text == "MANUALE":
                algorithm.algo("stop")
                open_control_window(False,root)
            else: 
                open_control_window(True,root)


    # Funzione per creare un label con un checkbutton
        def create_label_with_button(canvas, x, y, text):
            label = canvas.create_text(x, y, text=text, anchor=tk.W)  # Crea il testo sul canvas
            if automatico:
                pass
                #button = tk.Button(canvas, text="OFF", width=3, height=1,bg="blue" ,command=lambda: change_color_webcam(text,button))
            else:
                button = tk.Button(canvas, text="|", width=3, height=1,bg="#f08080" ,command=lambda: function.change_Turnouts(text,button))
            canvas.create_window(x + 55, y + 0, window=button, anchor=tk.W)  # Crea il bottone vicino al testo sul canvas
            return label, button

        def START():
            #gestione grafica degllo start dell'Auto version
            current_color = start_button.cget("background")
            new_color = "#00ff00" if current_color == "red" else "red"
            start_button.config(background=new_color)

            algorithm.algo("start") if current_color == "red" else algorithm.algo("stop")

        #---------CREAZIONE DELLA PAGINA---------

        root = window

        canvas_width = 1200
        canvas_height = 700

        frame = tk.Frame(root)
        frame.pack(anchor=tk.NW)

        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
        canvas.pack(side=tk.LEFT, expand=True)
        function.canvas_array[0] = canvas

        if automatico:
            text = "MANUALE"
            feature_button = tk.Button(frame, text=text, height = 2, command=lambda:change_window(text,root))
            feature_button.pack(side=tk.LEFT)

            image_power_path="interfaccia_grafica\\assets\\power_icon.png"
            image_power = function.process_image(image_power_path,'resize',35,35)
            start_button = tk.Button(frame, image=image_power,bg="red", command=START)
            start_button.pack(padx=(10,5),side=tk.LEFT)
            
            webcam = tk.Button(frame, text="VIDEO OFF", height=2,bg="blue" ,command=lambda: change_color_webcam())
            webcam.pack(padx=5,side=tk.LEFT)

            locomotive_label = tk.Label(frame, text="CONTROLLO AUTOMATICO CIRCUITO")
            locomotive_label.pack(padx=(340,0),pady=10,side=tk.LEFT)

            #webcam = create_label_with_button(canvas,600,350,"Attiva Webcam")
        else:
            text = "AUTOMATICO"
            feature_button = tk.Button(frame, text=text, height = 2, command=lambda:change_window(text,root))
            feature_button.pack(side=tk.LEFT)

            locomotive_label = tk.Label(frame, text="CONTROLLO MANUALE CIRCUITO")
            locomotive_label.pack(padx=462,pady=10,side=tk.LEFT, anchor=tk.NW)

        #creazione dei bottoni per i deviatoi
            cambio1, button1 = create_label_with_button(canvas, 10, 60, "Cambio 1")
            cambio2, button2 = create_label_with_button(canvas, 200, canvas_height-630, "Cambio 2")
            cambio3, button3 = create_label_with_button(canvas, 375, canvas_height-20, "Cambio 3")
            cambio4, button4 = create_label_with_button(canvas, 675, canvas_height-20, "Cambio 4")
            cambio5, button5 = create_label_with_button(canvas, 1050, canvas_height-450, "Cambio 5")
            cambio6, button6 = create_label_with_button(canvas, 875, 60, "Cambio 6")
            cambio7, button7 = create_label_with_button(canvas, 150, canvas_height-500, "Cambio 7")
            cambio8, button8 = create_label_with_button(canvas, 415, canvas_height-150, "Cambio 8")

        
        # feature_button.pack(side=tk.LEFT)
        #locomotive_label.pack(padx=472,pady=10,side=tk.LEFT)
  


        #----DISEGNO CIRCUITO---- link docs: https://www.pythontutorial.net/tkinter/tkinter-canvas/

        # Percorso dell'immagine originale
        stop_path = 'interfaccia_grafica\\assets\\stop_treno.png'
        casetta_path = 'interfaccia_grafica\\assets\\casetta.png'
        sensore_path = 'interfaccia_grafica\\assets\\sensore_rfid.jpg'
        # binario_path = 'interfaccia_grafica\\assets\\binario.png'

        # Ridimensiona l'immagine utilizzando la funzione resize_image
        stop_treno = function.process_image(stop_path,'resize', 50, 50)
        casetta = function.process_image(casetta_path,'resize', 100, 100)
        # binario = process_image(binario_path,'resize', 100, 100)
        sensore = function.process_image(sensore_path,'resize', 50, 50)
        sensore_rotated1 = function.process_image(sensore_path,'rotate', -90, 50, 50)  # Ruota a sinistra
        sensore_rotated2 = function.process_image(sensore_path,'rotate', -180, 50, 50)  # Ruota di 180
        sensore_rotated3 = function.process_image(sensore_path,'rotate', 90, 50, 50)  # Ruota a destra

        canvas.create_image(
            (30, canvas_height-150),
            image=stop_treno,
        )

        canvas.create_image(
            (70, canvas_height-50),
            image=stop_treno,
        )

        canvas.create_image(
            (700, 450),
            image=casetta,
        )

        canvas.create_image(
            (780, 300),
            image=casetta,
        )

        canvas.create_image(
            (900, 620),
            image=sensore,
        )

        canvas.create_image(
            (135, 300),
            image=sensore_rotated1,
        )

        canvas.create_image(
            (1145, 400),
            image=sensore_rotated3,
        )

        canvas.create_image(
            (350, 70),
            image=sensore_rotated2,
        )

        #linee sinistra con stop
        canvas.create_line((30, 155), (30, canvas_height-160), width=8, fill='black')
        canvas.create_line((70, 150), (70, canvas_height-60), width=8, fill='black')
        canvas.create_line((30, 155), (30, canvas_height-160), width=4, fill='white')
        canvas.create_line((70, 150), (70, canvas_height-60), width=4, fill='white')

        #linea in alto dritta
        canvas.create_line((293, 31), (1000, 31), width=8, fill='black')
        canvas.create_line((293, 31), (1000, 31), width=4, fill='white')

        # Disegna l'immagine come sfondo centrata sulla linea superiore
        # x = 270
        # for i in range(8):
        #     canvas.create_image(x, -20, anchor=tk.NW, image=binario)
        #     x += 95
        #     i +=1
        # canvas.create_image(365, -20, anchor=tk.NW, image=binario)
        
        #curva esterna in alto a destra
        canvas.create_arc((825, 270), (1175, 30), style=tk.ARC, start=0, extent=90, width=8, outline="black")
        canvas.create_arc((825, 270), (1175, 30), style=tk.ARC, start=0, extent=90, width=4, outline="white")
        # canvas.create_oval((825, 270), (1175, 30), outline="black", width=2)

        #linea destra esterna dritta
        canvas.create_line((1175, 150), (1175, canvas_height-170), width=8, fill='black')
        canvas.create_line((1175, 150), (1175, canvas_height-170), width=4, fill='white')

        #curva esterna in basso a destra
        canvas.create_arc((825, canvas_height-50), (1175, canvas_height-290), style=tk.ARC, start=0, extent=-90, width=8, outline="black")
        canvas.create_arc((825, canvas_height-50), (1175, canvas_height-290), style=tk.ARC, start=0, extent=-90, width=4, outline="white")
        # canvas.create_oval((825, canvas_height-50), (1175, canvas_height-290), outline="black", width=2)

        #linea in basso esterna dritta
        canvas.create_line((270, canvas_height-50), (1000, canvas_height-50), width=8, fill='black')
        canvas.create_line((270, canvas_height-50), (1000, canvas_height-50), width=4, fill="white")

        #curva esterna in basso a sinistra
        canvas.create_arc((100, canvas_height-50), (450, canvas_height-290), style=tk.ARC, start=270, extent=-90, width=8, outline="black")
        canvas.create_arc((100, canvas_height-50), (450, canvas_height-290), style=tk.ARC, start=270, extent=-90, width=4, outline="white")
        # canvas.create_oval((50, 270), (400, 30), outline="black", width=2)

        #linea sinistra interna dritta
        canvas.create_line((100, 150), (100, canvas_height-170), width=8, fill='black')
        canvas.create_line((100, 150), (100, canvas_height-170), width=4, fill='white')

        #id scambio 1
        cambio1def  = canvas.create_arc((28, 270), (400, 70), style=tk.ARC, start=134, extent= 38, width=8, outline="red")
        canvas.create_arc((28, 270), (400, 70), style=tk.ARC, start=134, extent= 38, width=4, outline="white")
        # canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=180, extent=-90, width=4, outline="black")
        cambio1     = canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=156, extent=24, width=8, outline="black")
        canvas.create_arc((68, 270), (380, 30), style=tk.ARC, start=156, extent=24, width=4, outline="white")
        # canvas.create_oval((28, 270), (400, 70), outline="black", width=2)
        function.Turnouts['Cambio 1'][2] = cambio1def
        function.Turnouts['Cambio 1'][3] = cambio1
        # function.Turnouts['Cambio 1'].append(cambio1def)
        # function.Turnouts['Cambio 1'].append(cambio1)

        #id scambio 2
        cambio2     = canvas.create_arc((100, 270), (500, 30), style=tk.ARC, start=96, extent=84, width=8, outline="black")
        canvas.create_arc((100, 270), (500, 30), style=tk.ARC, start=96, extent=84, width=4, outline="white")

        cambio2def  = canvas.create_arc((68, 260), (475, 30), style=tk.ARC, start=84, extent=74, width=8, outline="red")
        canvas.create_arc((68, 260), (475, 30), style=tk.ARC, start=84, extent=74, width=4, outline="white")
        # canvas.create_oval((68, 270), (475, 30), outline="black", width=2)
        function.Turnouts['Cambio 2'][2] = cambio2def
        function.Turnouts['Cambio 2'][3] = cambio2
        # function.Turnouts['Cambio 2'].append(cambio2def)
        # function.Turnouts['Cambio 2'].append(cambio2)

        #id scambio 3
        cambio3     = canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=145, extent=100, width=8, outline="black")
        canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=145, extent=100, width=4, outline="white")

        cambio3def  = canvas.create_line((270, canvas_height-50), (470, canvas_height-50), width=8, fill='red')
        canvas.create_line((270, canvas_height-50), (470, canvas_height-50), width=4, fill='white')
        # canvas.create_oval((175, canvas_height-50), (1200, canvas_height-640), outline="black", width=2)
        function.Turnouts['Cambio 3'][2] = cambio3def
        function.Turnouts['Cambio 3'][3] = cambio3
        # function.Turnouts['Cambio 3'].append(cambio3def)
        # function.Turnouts['Cambio 3'].append(cambio3)


        #id scambio 4
        cambio4def  = canvas.create_line((470, canvas_height-50), (700, canvas_height-50), width=8, fill='red')
        canvas.create_line((470, canvas_height-50), (700, canvas_height-50), width=4, fill='white')
        function.Turnouts['Cambio 4'][2] = cambio4def
        # function.Turnouts['Cambio 4'].append(cambio4def)

        #id scambio 4/8
        cambio4     = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=226, extent=40, width=8, outline="black")
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=226, extent=40, width=4, outline="white")
        function.Turnouts['Cambio 4'][3] = cambio4
        # function.Turnouts['Cambio 4'].append(cambio4)
        # canvas.create_oval((250, canvas_height-50), (1200, canvas_height-600), outline="black", width=2)
        
        #id scambio 5
        cambio5  = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=19, extent=54, width=8, outline="black")
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=19, extent=54, width=4, outline="white")

        cambio5def = canvas.create_line((1175, 150), (1175, 267), width=8, fill='red')
        canvas.create_line((1175, 150), (1175, 267), width=4, fill='white')
        function.Turnouts['Cambio 5'][2] = cambio5def
        function.Turnouts['Cambio 5'][3] = cambio5
        # function.Turnouts['Cambio 5'].append(cambio5def)
        # function.Turnouts['Cambio 5'].append(cambio5)

        # canvas.create_oval((250, canvas_height-50), (1200, canvas_height-600), outline="black", width=2)
        
        #id scambio 6
        cambio6def  = canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=73, extent=65, width=8, outline="red")
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=73, extent=65, width=4, outline="white")

        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=139, extent=88, width=8, outline="black")
        canvas.create_arc((280, canvas_height-50), (1200, canvas_height-630), style=tk.ARC, start=139, extent=88, width=4, outline="white")
        function.Turnouts['Cambio 6'][2] = cambio6def
        # function.Turnouts['Cambio 6'].append(cambio6def)
        # canvas.create_oval((250, canvas_height-50), (1200, canvas_height-600), outline="black", width=2)
        
        
        #id scambio 6/7
        cambio7 = canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=68, extent=85, width=8, outline="black")
        canvas.create_arc((175, canvas_height-20), (1200, canvas_height-640), style=tk.ARC, start=68, extent=85, width=4, outline="white")
        # Turnouts['Cambio 5'].append(cambio5def)
        function.Turnouts['Cambio 6'][3] = cambio7
        # function.Turnouts['Cambio 6'].append(cambio7)
        # canvas.create_oval((175, canvas_height-50), (1200, canvas_height-640), outline="black", width=2)

        #id scambio 7
        cambio7def  = canvas.create_arc((208, canvas_height-300), (900, canvas_height-546), style=tk.ARC, start=117, extent=50, width=8, outline="red")
        canvas.create_arc((208, canvas_height-300), (900, canvas_height-546), style=tk.ARC, start=117, extent=50, width=4, outline="white")
        # canvas.create_oval((210, canvas_height-300), (900, canvas_height-546), outline="black", width=2)
        function.Turnouts['Cambio 7'][2] = cambio7def
        function.Turnouts['Cambio 7'][3] = cambio7
        # function.Turnouts['Cambio 7'].append(cambio7def)
        # function.Turnouts['Cambio 7'].append(cambio7)

        #id scambio 8
        cambio8def  = canvas.create_arc((230, canvas_height-110), (900, canvas_height-563), style=tk.ARC, start=244, extent=237, width=8, outline="red")
        canvas.create_arc((230, canvas_height-110), (900, canvas_height-563), style=tk.ARC, start=244, extent=237, width=4, outline="white")
        function.Turnouts['Cambio 8'][2] = cambio8def
        function.Turnouts['Cambio 8'][3] = cambio4
        # function.Turnouts['Cambio 8'].append(cambio8def)
        # function.Turnouts['Cambio 8'].append(cambio4)
        # canvas.create_oval((230, canvas_height-110), (900, canvas_height-563), outline="black", width=2)
        
        # canvas = tk.Canvas(root, width=800, height=400, bg="white")
        # canvas.pack()
        

        #const = automatico
        #gestione dei pin ARDUINO
        if comandi.is_serial_port_available(""):
            if not function.variabili_chiusura["locomotive_circuit_var"]:
                function.variabili_chiusura["locomotive_circuit_var"] = True
                for i in range (nscambi):
                    i+=1
                    str = 'Cambio {}'.format(i)
                    if i == 3: 
                        comandi.crea_deviatoio(i,i+37) # va sul pin 40
                    elif i == 4:
                        comandi.crea_deviatoio(i,i+34) # va sul pin 38
                    else:
                        comandi.crea_deviatoio(i,i+40) # vanno nel loro pin corrispondente + 40 
                    function.Turnouts[str][1] = i

 

        # # Aggiungere la gestione del click del mouse sui label
        # cambi_label.bind("<Button-1>", lambda event: label_clicked(event, "Cambi"))
        # semafori_label.bind("<Button-1>", lambda event: label_clicked(event, "Semafori"))

        # # Funzione per gestire il click del mouse sui label
        # def label_clicked(event, label_text):
        #     print("Label cliccato:", label_text)

        # Eseguire il loop principale
        root.mainloop()
#open_control_window(False)