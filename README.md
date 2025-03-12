<p align="center">
  <img src="Train Track Manager/interfaccia_grafica/assets/Preview.png" width="50%">
</p>

## Descrizione
TrainTrack Manager è un'applicazione che permette di controllare un plastico ferroviario utilizzando Arduino e un'interfaccia grafica sviluppata in Python. Il progetto consente la gestione delle locomotive, il controllo dei deviatoi e l'automazione del sistema tramite sensori RFID.

## Caratteristiche Principali
- **Controllo di un plastico ferroviario** con Arduino Mega 2560 e Arduino Uno Rev 3.
- **Interfaccia grafica user-friendly** sviluppata in Python con Tkinter.
- **Sistema di automazione** per la gestione intelligente delle locomotive e degli scambi.
- **Integrazione di sensori RFID** per il monitoraggio della posizione delle locomotive.
- **Supporto multilingua** (Italiano, Inglese, Francese, Spagnolo).

## Componenti del Progetto
### 1. **Arduino**
- Arduino Mega 2560 per il controllo delle locomotive e dei deviatoi.
- Arduino Uno Rev 3 per la gestione dei sensori RFID.
- Motor Shield Rev 3 per la modulazione della corrente.

### 2. **Interfaccia Grafica**
- Implementata in Python utilizzando Tkinter.
- Controllo delle locomotive (velocità, direzione, gestione database locomotive).
- Monitoraggio in tempo reale del circuito e degli scambi.
- Modalità automatica per la gestione autonoma dei treni.

### 3. **Sistema di Automazione**
- Lettori RFID per il rilevamento della posizione delle locomotive.
- Algoritmo di controllo per prevenire collisioni e gestire gli scambi.
- Ottimizzazione dei percorsi basata sulla situazione attuale del circuito.

## Installazione
### Prerequisiti
- **Hardware:**
  - Arduino Mega 2560
  - Arduino Uno Rev 3
  - Motor Shield Rev 3
  - Sensori RFID MFRC522
  - Relè per il controllo degli scambi
- **Software:**
  - Python 3.x
  - Librerie Python necessarie: `pyserial`, `tkinter`, `opencv`, `queue`, `threading`, `pillow`, `subprocess`
  - Librerie Arduino: `DCCpp`, `MFRC522`

### Passaggi
1. **Installare Python e le librerie richieste:**
   ```bash
   pip install pyserial opencv-python pillow
   ```
2. **Caricare gli sketch su Arduino** utilizzando l'IDE Arduino.
3. **Avviare l'applicazione Python** con:
   ```bash
   python main.py
   ```

## Modalità di Utilizzo
- **Gestione manuale:** Controllo delle locomotive e dei deviatoi tramite GUI.
- **Monitoraggio in tempo reale:** Visualizzazione dello stato delle locomotive e degli scambi.
- **Modalità automatica:** Algoritmo di gestione autonoma del traffico ferroviario.

## Sviluppi Futuri
- Implementazione di videocamere su ogni locomotiva per il monitoraggio.
- Controllo da remoto tramite Arduino Wi-Fi.
- Scalabilità della GUI per supportare circuiti personalizzati.

## Documentazione
- **Documentazione tecnica:** [TrainTrack Manager Docs](https://www.traintrackdocs.altervista.org/)
- **Repository GitHub:** [TrainTrack Manager Repo](https://github.com/alexein1001/translating)

## Autore
**Alessio Cammarata** - Progetto realizzato come parte del corso di Informatica e Telecomunicazioni, 5^A Info, Anno Scolastico 2023/2024.

## Licenza
Questo progetto è rilasciato sotto licenza **MIT**.

---

# TrainTrack Manager (English Version)

## Description
TrainTrack Manager is an application that allows you to control a railway model using Arduino and a graphical interface developed in Python. The project enables locomotive management, switch control, and system automation via RFID sensors.

## Main Features
- **Railway model control** with Arduino Mega 2560 and Arduino Uno Rev 3.
- **User-friendly graphical interface** developed in Python with Tkinter.
- **Automation system** for intelligent locomotive and switch management.
- **Integration of RFID sensors** for locomotive position monitoring.
- **Multilingual support** (Italian, English, French, Spanish).

## Project Components
### 1. **Arduino**
- Arduino Mega 2560 for locomotive and switch control.
- Arduino Uno Rev 3 for RFID sensor management.
- Motor Shield Rev 3 for current modulation.

### 2. **Graphical Interface**
- Implemented in Python using Tkinter.
- Locomotive control (speed, direction, locomotive database management).
- Real-time monitoring of the circuit and switches.
- Automatic mode for autonomous train management.

### 3. **Automation System**
- RFID readers for detecting locomotive positions.
- Control algorithm to prevent collisions and manage switches.
- Route optimization based on the current circuit status.

## Installation
### Prerequisites
- **Hardware:**
  - Arduino Mega 2560
  - Arduino Uno Rev 3
  - Motor Shield Rev 3
  - RFID Sensors MFRC522
  - Relays for switch control
- **Software:**
  - Python 3.x
  - Required Python libraries: `pyserial`, `tkinter`, `opencv`, `queue`, `threading`, `pillow`, `subprocess`
  - Arduino Libraries: `DCCpp`, `MFRC522`

### Steps
1. **Install Python and required libraries:**
   ```bash
   pip install pyserial opencv-python pillow
   ```
2. **Upload the sketches to Arduino** using the Arduino IDE.
3. **Start the Python application** with:
   ```bash
   python main.py
   ```

## Usage Modes
- **Manual management:** Control locomotives and switches via GUI.
- **Real-time monitoring:** View the status of locomotives and switches.
- **Automatic mode:** Autonomous railway traffic management algorithm.

## Future Developments
- Implementation of cameras on each locomotive for monitoring.
- Remote control via Arduino Wi-Fi.
- GUI scalability to support custom circuits.

## Documentation
- **Technical documentation:** [TrainTrack Manager Docs](https://www.traintrackdocs.altervista.org/)
- **GitHub Repository:** [TrainTrack Manager Repo](https://github.com/alexein1001/translating)

## Author
**Alessio Cammarata** - Project created as part of the Computer Science and Telecommunications course, 5^A Info, Academic Year 2023/2024.

## License
This project is released under the **MIT** license.

