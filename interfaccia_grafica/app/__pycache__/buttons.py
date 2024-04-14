import comandi_refactored

class Buttons:

    def __init__(self,color):
        self.color = color

    #funzione che serve per la gestione del bottone ON/OFF della corrente
    def on_off(self,GUI):

        if self.color == "red":
            on=1
        else:
            on=0
            
        comandi_refactored.open_current(on)
        #cambia il colore al bottone
        new_color = "#00ff00" if self.color == "red" else "red"
        GUI.on_button.config(background=new_color)
        GUI.check_control_button_state()


    #funzione che serve per la gesetione dell'avvio e dell'arresto del sistema senza togliere la corrente
    def GENERAL_STOP_START(self,GUI):
        contatore_velocita  = 0
        start = False
        is0   = False
        i=0
        #ciclo che si esegue per ogni locomotiva
        for i in range (len(GUI.locomotives_data)):
            #se la velocita è 0 si aumenta il contatore, e is0 è settato a True
            if GUI.locomotives_data[i]['Velocita'] == 0:
                contatore_velocita=contatore_velocita+1
                is0 = True
            #in base al colore del bottone, si attiva
            if self.color == "#f08080":
                #ferma completamente il sistema
                memoria = GUI.locomotives_data[i]['ID']
                ID      = GUI.locomotives_data[i]['LocoID']
                #se la locomotiva era gia ferma, il comando non gli viene mandato
                if not is0:
                    #predno in memoria la velocita corrente e poi gli assegno il valore
                    GUI.locomotives_data[i]['VelocitaM'] = GUI.locomotives_data[i]['Velocita']
                    GUI.locomotives_data[i]['Velocita']  = 0
                    comandi_refactored.STOP(memoria,ID)
            else:
                #ripristina il sistema come era prima
                memoria     = GUI.locomotives_data[i]['ID']
                ID          = GUI.locomotives_data[i]['LocoID']
                velocita    = GUI.locomotives_data[i]['VelocitaM'] 
                direzione   = GUI.locomotives_data[i]['Direzione'] 
                start = True

                #se la locomotiva era ferma il comadno non gli viene mandato
                if not is0 or GUI.locomotives_data[i]['VelocitaM']!=0:
                    #predno in memoria la velocita corrente e poi gli assegno il valore
                    GUI.locomotives_data[i]['VelocitaM'] = GUI.locomotives_data[i]['Velocita']
                    GUI.locomotives_data[i]['Velocita']  = velocita
                    comandi_refactored.throttle(memoria,ID,velocita,direzione)
            i=i+1
            is0 = False

        #cambia lo stile del bottone a seconda di come va il sistema, verde se è fermo e rosso se è in movimento
        if contatore_velocita != len(GUI.locomotives_data) or start:  
            new_color = "#8fbc8f" if self.color == "#f08080" else "#f08080"
            new_text = "AVVIO GENERALE" if self.color == "#f08080" else "STOP GENERALE"
            GUI.STOP_button.config(background=new_color,text=new_text)
            GUI.check_control_button_state()
