'''
The purpose of this file is to comunicate with arduino directly by the serial port.
With these command you could be able to control both the system and all the locomotives.
'''
import app.data as data
import time
import subprocess

#                   ___                                       _      _    
#           o O O  / __|    ___    _ __    __ _    _ _     __| |    (_)   
#          o      | (__    / _ \  | '  \  / _` |  | ' \   / _` |    | |   
#         TS__[O]  \___|   \___/  |_|_|_| \__,_|  |_||_|  \__,_|   _|_|_  
#        {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
#       ./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 

#Funzione che aggiorna il nome della seriale
def name_serial_port():
    """- This function update the serial port's name that deal with the dcc control unit"""
    port = data.serial_ports[0]
        # Per sistemi Windows                   Per sistemi Unix-like (Linux, macOS)
    return f"COM{port}" if data.SO == 'Windows' else f"/dev/{port}"  

 
#funzione che accende o spegne la corrente al sistema
#<1> o <0>
def open_current(on):
    """
    - This function allow you to open the **current** o shut down it. It takes as argument 0 or 1 and then passes the command <0> or <1> to the arduino
     
    -- **<1>** enables power from the motor shield to the main operations and programming tracks\n
    -- **<0>** disables power from the motor shield to the main operations and programming tracks\n
    """
    comando = ('echo "<{}>" > {}'.format(on,name_serial_port()))
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)

#funzione per dare il comando di velocita alla locomotiva
#<t REGISTER CAB SPEED DIRECTION>

# 	REGISTER: Numero di registrazione interno.
# 	CAB: Indirizzo breve (1-127) o lungo (128-10293) del decoder del treno.
# 	SPEED: Velocità del regolatore da 0 a 126, o -1 per l'arresto di emergenza.
# 	DIRECTION: 1 per la direzione in avanti, 0 per la direzione inversa.

def throttle(memoria,ID, SPEED, DIR):
    """
    - This function allow you to set the **speed of a specific locomotive**. It takes as arguments: memoryRegister, LocomotiveID, speeed and Direction.\n
    # <t REGISTER CAB SPEED DIRECTION>
 
    Sets the throttle for a given register/cab combination \n\n
     
    -- REGISTER: an internal register number, from 1 through MAX_MAIN_REGISTERS (inclusive), to store the DCC packet used to control this throttle setting\n
    -- CAB:  the short (1-127) or long (128-10293) address of the engine decoder\n
    -- SPEED: throttle speed from 0-126, or -1 for emergency stop (resets SPEED to 0)\n
    -- DIRECTION: 1=forward, 0=reverse.  Setting direction when speed=0 or speed=-1 only effects directionality of cab lighting for a stopped train
     
    """
    print(memoria, ID, SPEED, DIR)
    comando =('echo "<t {} {} {} {}>" > {}'.format(memoria, ID, SPEED, DIR,name_serial_port())) 
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)

#funzione per lo stop di una singola locomotiva dato l'ID

def STOP(memoria,ID):
    """
    - This function allow you to **stop a specific locomotive**. It takes as arguments: memoryRegister and LocomotiveID.\n
    It uses the same command of throttle but direction and speed are fixed to stop the locomotive.

    """
    comando = ('echo "<t {} {} 0 1>" > {}'.format(memoria,ID,name_serial_port()))
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)


#funzione per cambiare indirizzo al controller della locomotiva
#<w [CAB] 1 5> -->

# - [CAB] è l'indirizzo attuale della locomotiva 
# - 5 è il nuovo indirizzo desiderato 
# - 1 è il CV dove è localizzato l'ID della locomotiva

def change_id(current_ID,new_ID):
    """
    - This function allow you to modify the **LocomotiveID of a specific locomotive**. It takes as arguments: current LocomotiveID and the new LocomotiveID.\n
    # <w [CAB] CV VALUE>
 
    writes, without any verification, a Configuration Variable to the decoder of an engine on the main operations track.\n\n
     
    -- CAB:  the short (1-127) or long (128-10293) address of the engine decoder \n
    -- CV: the number of the Configuration Variable memory location in the decoder to write to (1-1024), The number 1 is related to the locomotiveID.\n
    -- VALUE: the value to be written to the Configuration Variable memory location (0-255)
     
    """
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
    """
    - This function allow you to save the **TurnoutID**. It takes as arguments: TurnouID and the pin related to it.\n
    # <Z ID PIN IFLAG>:          
    
    creates a new output ID, with specified PIN and IFLAG values. if output ID already exists, it is updated with specificed PIN and IFLAG.\n
    note: output state will be immediately set to ACTIVE/INACTIVE and pin will be set to HIGH/LOW according to IFLAG value specifcied (see below).\n\n
    
    -- ID: the numeric ID (0-32767) of the output to control\n
    -- PIN: the arduino pin number to use for the output\n
    -- IFLAG: defines the operational behavior of the output based on bits 0, 1, and 2 as follows:\n\n
    
    ---\n

    - 1) -IFLAG, bit 0:\n
    0 = forward operation (ACTIVE=HIGH / INACTIVE=LOW)\n
    1 = inverted operation (ACTIVE=LOW / INACTIVE=HIGH)\n

    ---\n

    - 2) -IFLAG, bit 1:\n 
    0 = state of pin restored on power-up to either ACTIVE or INACTIVE depending on state before power-down; state of pin set to INACTIVE when first created\n
    1 = state of pin set on power-up, or when first created, to either ACTIVE of INACTIVE depending on IFLAG, bit 2\n\n

    ---\n

    - 3) -IFLAG, bit 2:\n
    0 = state of pin set to INACTIVE uponm power-up or when first created\n
    1 = state of pin set to ACTIVE uponm power-up or when first created 

    """
    #1 poiche deve essere attivo purche i rele stiano fermi
    comando = ('echo "<Z {} {} 1>" > {}'.format(Turnout_ID,pin,name_serial_port()))
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
    print(Turnout_ID,pin)

def cambia_deviatoio(Turnout_ID):
    """
    - This function allow you to modify the **Turnout's state**. It takes as argument the TurnoutID.\n
    # <Z ID ACTIVATE>:          
    
    sets output ID to either the "active" or "inactive" state\n\n
    
    ID: the numeric ID (0-32767) of the output to control\n
    ACTIVATE: 0 (active) or 1 (inactive)\n

    """

    #1 significa low, per attivare i rele
    comando = ('echo "<Z {} 1>" > {}'.format(Turnout_ID,name_serial_port()))
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
    time.sleep(0.2)

    #0 significa high, per disattivare i rele
    comando = ('echo "<Z {} 0>" > {}'.format(Turnout_ID,name_serial_port()))
    subprocess.call(comando, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
    #print(Turnout_ID)
