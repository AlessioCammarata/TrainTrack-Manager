import comandi
import data

'''

                ___             _       _                             
        o O O  | _ )   _  _    | |_    | |_     ___    _ _      ___   
       o       | _ \  | +| |   |  _|   |  _|   / _ \  | ' \    (_-<   
      TS__[O]  |___/   \_,_|   _\__|   _\__|   \___/  |_||_|   /__/_  
     {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
    ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'

'''

class Buttons:

    def __init__(self,color):
        self.color = color

    #funzione che serve per la gestione del bottone ON/OFF della corrente
    def on_off(self,GUI):

        if self.color == "red":
            on=1
        else:
            on=0

        comandi.open_current(on)

        #cambia il colore al bottone
        new_color = "#00ff00" if self.color == "red" else "red"
        GUI.on_button.config(background=new_color)
        GUI.check_control_button_state()


    #funzione che serve per la gesetione dell'avvio e dell'arresto del sistema senza togliere la corrente
    def GENERAL_STOP_START_button(self,GUI):
        contatore_velocita  = 0
        start = False
        is0   = False
        i=0
        #ciclo che si esegue per ogni locomotiva
        for i in range (len(data.locomotives_data)):

            #se la velocita è 0 si aumenta il contatore, e is0 è settato a True
            if data.locomotives_data[i]['Velocita'] == 0:
                contatore_velocita=contatore_velocita+1
                is0 = True
            #in base al colore del bottone, si attiva
            if self.color == "#f08080":

                #ferma completamente il sistema
                memoria = data.locomotives_data[i]['ID']
                ID      = data.locomotives_data[i]['LocoID']
                #se la locomotiva era gia ferma, il comando non gli viene mandato
                if not is0:

                    #predno in memoria la velocita corrente e poi gli assegno il valore
                    data.locomotives_data[i]['VelocitaM'] = data.locomotives_data[i]['Velocita']
                    data.locomotives_data[i]['Velocita']  = 0
                    comandi.STOP(memoria,ID)
            else:

                #ripristina il sistema come era prima
                memoria     = data.locomotives_data[i]['ID']
                ID          = data.locomotives_data[i]['LocoID']
                velocita    = data.locomotives_data[i]['VelocitaM'] 
                direzione   = data.locomotives_data[i]['Direzione'] 
                start = True

                #se la locomotiva era ferma il comadno non gli viene mandato
                if not is0 or data.locomotives_data[i]['VelocitaM']!=0:

                    #predno in memoria la velocita corrente e poi gli assegno il valore
                    data.locomotives_data[i]['VelocitaM'] = data.locomotives_data[i]['Velocita']
                    data.locomotives_data[i]['Velocita']  = velocita
                    comandi.throttle(memoria,ID,velocita,direzione)
            i=i+1
            is0 = False

        #cambia lo stile del bottone a seconda di come va il sistema, verde se è fermo e rosso se è in movimento
        if contatore_velocita != len(data.locomotives_data) or start:
            new_color = "#8fbc8f" if self.color == "#f08080" else "#f08080"
            new_text = data.Textlines[18] if self.color == "#f08080" else data.Textlines[10]
            GUI.STOP_button.config(background=new_color,text=new_text)
            GUI.check_control_button_state()
