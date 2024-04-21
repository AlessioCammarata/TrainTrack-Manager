'''
The purpose of this file is to comunicate with arduino directly by the serial port.
With these command you could be able to control both the system and all the locomotives.
'''

import data
import os
import time
import subprocess

'''

                ___                                       _      _    
        o O O  / __|    ___    _ __    __ _    _ _     __| |    (_)   
       o      | (__    / _ \  | '  \  / _` |  | ' \   / _` |    | |   
      TS__[O]  \___|   \___/  |_|_|_| \__,_|  |_||_|  \__,_|   _|_|_  
     {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
    ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 

'''
#Funzione che aggiorna il nome della seriale
def name_serial_port():
    port = data.serial_ports[0]
    return f"COM{port}"  

#funzione che accende o spegne la corrente al sistema
#<1> o <0>

def open_current(on):
    comando = ('echo "<{}>" > {}'.format(on,name_serial_port()))
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)

#funzione per dare il comando di velocita alla locomotiva
#<t REGISTER CAB SPEED DIRECTION>

# 	REGISTER: Numero di registrazione interno.
# 	CAB: Indirizzo breve (1-127) o lungo (128-10293) del decoder del treno.
# 	SPEED: Velocità del regolatore da 0 a 126, o -1 per l'arresto di emergenza.
# 	DIRECTION: 1 per la direzione in avanti, 0 per la direzione inversa.

def throttle(memoria,ID, SPEED, DIR):
    print(memoria, ID, SPEED, DIR)
    comando =('echo "<t {} {} {} {}>" > {}'.format(memoria, ID, SPEED, DIR,name_serial_port())) 
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)

#funzione per lo stop di una singola locomotiva dato l'ID

def STOP(memoria,ID):
    comando = os.system('echo "<t {} {} 0 1>" > {}'.format(memoria,ID,name_serial_port()))
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)

#funzione per cambiare indirizzo al controller della locomotiva
#<w [CAB] 1 5> -->

# - [CAB] è l'indirizzo attuale della locomotiva 
# - 5 è il nuovo indirizzo desiderato 
# - 1 è il CV dove è localizzato l'ID della locomotiva

def change_id(current_ID,new_ID):
    comando = ('echo "<w {} 1 {}>" > {}'.format(current_ID,new_ID,name_serial_port()))
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)

# Controllo Uscite - <Z>:
# Esempio: <Z ID ACTIVATE>
# 	ID: ID numerico (0-32767) dell'uscita.
# 	ACTIVATE: 0 per attivare, 1 per disattivare.

# 	<Z ID PIN IFLAG>: Crea o aggiorna un output personalizzato con un ID specifico, un numero di pin Arduino (PIN), e un flag (IFLAG) che definisce il comportamento operativo (vedi sotto).
# 	<Z ID>: Elimina la definizione dell'output con l'ID specificato.
# 	<Z>: Mostra tutti gli output personalizzati definiti, restituendo <Y ID PIN IFLAG STATE> per ciascuno.

# 		Bit 0 (Operazione Diretta o Invertita):
# 			IFLAG, bit 0: 0 indica un funzionamento diretto (ACTIVE=HIGH / INACTIVE=LOW).
# 			IFLAG, bit 0: 1 indica un funzionamento invertito (ACTIVE=LOW / INACTIVE=HIGH).
    
#id = numero casuale della memoria -- address porta a cui abbinare il deviatoio
def crea_deviatoio(Turnout_ID,pin):
    #1 poiche deve essere attivo purche i rele stiano fermi
    comando = ('echo "<Z {} {} 1>" > {}'.format(Turnout_ID,pin,name_serial_port()))
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
    print(Turnout_ID,pin)

def cambia_deviatoio(Turnout_ID):
    #1 significa low, per attivare i rele
    comando = ('echo "<Z {} 1>" > {}'.format(Turnout_ID,name_serial_port()))
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
    time.sleep(0.2)

    #0 significa high, per disattivare i rele
    comando = ('echo "<Z {} 0>" > {}'.format(Turnout_ID,name_serial_port()))
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
    #print(Turnout_ID)
