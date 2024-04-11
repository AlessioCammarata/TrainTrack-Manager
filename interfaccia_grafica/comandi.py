'''
The purpose of this file is to comunicate with arduino directly by the serial port.
With these command you could be able to control both the system and all the locomotives.
'''

import os
import serial

port = 3
serial_port = f"COM{port}"
inizialized = [False]

def is_serial_port_available(function_port):
    if function_port == "":
        function_port = port
    # Costruisci il percorso del dispositivo della porta seriale
    #port_path = f"/dev/{port}"  # Per sistemi Unix-like (Linux, macOS)
    port_path = f"COM{function_port}"  # Per sistemi Windows
    exist = os.path.exists(port_path)
    if exist and not inizialized[0]:
        inizialized[0] = True
        serial.Serial(port_path,baudrate=115200,timeout=1)
    # Verifica l'esistenza del percorso della porta seriale
    exist_inizialized = exist and inizialized[0]
    return exist_inizialized
  


#funzione che accende o spegne la corrente al sistema
#<1> o <0>

def open_current(on):
    os.system('echo "<{}>" > {}'.format(on,serial_port))


#funzione per dare il comando di velocita alla locomotiva
#<t REGISTER CAB SPEED DIRECTION>

# 	REGISTER: Numero di registrazione interno.
# 	CAB: Indirizzo breve (1-127) o lungo (128-10293) del decoder del treno.
# 	SPEED: Velocità del regolatore da 0 a 126, o -1 per l'arresto di emergenza.
# 	DIRECTION: 1 per la direzione in avanti, 0 per la direzione inversa.

def throttle(memoria,ID, SPEED, DIR):
    print(memoria, ID, SPEED, DIR)
    os.system('echo "<t {} {} {} {}>" > {}'.format(memoria, ID, SPEED, DIR,serial_port)) 

#funzione per lo stop di una singola locomotiva dato l'ID

def STOP(memoria,ID):
    os.system('echo "<t {} {} 0 1>" > {}'.format(memoria,ID,serial_port))

#funzione per cambiare indirizzo al controller della locomotiva
#<w [CAB] 1 5> -->

# - [CAB] è l'indirizzo attuale della locomotiva 
# - 5 è il nuovo indirizzo desiderato 
# - 1 è il CV dove è localizzato l'ID della locomotiva

def change_id(current_ID,new_ID):
    os.system('echo "<w {} 1 {}>" > {}'.format(current_ID,new_ID,serial_port))

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
    os.system('echo "<Z {} {} 1>" > {}'.format(Turnout_ID,pin,serial_port))
    print(Turnout_ID,pin)

def cambia_deviatoio(Turnout_ID):
    os.system('echo "<Z {} 1>" > {}'.format(Turnout_ID,serial_port))
    #poiche deve essere solo un impulso
    os.system('echo "<Z {} 0>" > {}'.format(Turnout_ID,serial_port))

    #print(Turnout_ID)

'''

import subprocess

# Esegui un comando e cattura l'output
comando = 'echo "<T {} {}>" > COM3'.format(3,7)
comando = "dir"  # Sostituisci "dir" con il comando che desideri eseguire
output = subprocess.check_output(comando, shell=True, text=True)

# Stampa l'output
print(output)

'''

'''
import os
import time

porta_seriale = "COM3"  # Sostituisci con la tua porta seriale

try:
    # Invia dati ad Arduino
    os.system(f'type "Hello, Arduino!" > {porta_seriale}')

    # Attendi un po' prima di leggere la risposta
    time.sleep(2)

    # Leggi la risposta da Arduino
    response = os.popen(f'type {porta_seriale}').read().strip()
    print("Arduino dice:", response)

except KeyboardInterrupt:
    pass
    
'''

# Controllo Uscite - <Z>:
# Esempio: <Z ID ACTIVATE>
# 	ID: ID numerico (0-32767) dell'uscita.
# 	ACTIVATE: 0 per attivare, 1 per disattivare.


# Lettura della corrente - <c>:
# Esempio: <c>
# 	Nessun parametro richiesto.
