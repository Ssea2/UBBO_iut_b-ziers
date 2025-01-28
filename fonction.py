import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

def envoie_donnee(message):
    arduino.write((message+ '\n').encode())
    """reponse= arduino.readline().decode().strip()
    if reponse:
        print("Reponse de l'arduino:",reponse)"""
    
envoie_donnee('2')
time.sleep(2)
envoie_donnee('1')