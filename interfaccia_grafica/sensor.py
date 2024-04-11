'''
lettura dei sensori, le risposte
'''
import serial
import time
import queue
import function

# Definisci la coda all'interno del modulo sensor
message_queue = queue.Queue()


def start_sensor():
    porta_seriale = "COM3"
    
    try:
        ser = serial.Serial(porta_seriale, baudrate=115200, timeout=0)

        while not function.Sensors["Terminate"][0]:
            try:
                response = ser.readline().decode('utf-8').strip()
                if response:
                    print(f"Ricevuto dalla porta seriale: {response}")
                    message_queue.put(response)  # Aggiungi il messaggio alla coda

            except UnicodeDecodeError:
                print("Errore di decodifica. Assicurati che il dispositivo stia inviando dati correttamente.")
            time.sleep(0.1)
    except serial.SerialException as e:
        print(f"Errore nell'apertura della porta seriale: {e}")


