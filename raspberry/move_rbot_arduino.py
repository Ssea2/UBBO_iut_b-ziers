import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

def envoie_donnee(message):
    arduino.write((message+ '\n').encode())
    reponse= arduino.readline().decode().strip()
    if reponse:
        print("Reponse de l'arduino:",reponse)
    
def robot_dance():
    Up=["Up_tab" for i in range(20)]
    Down=["Down_Tab" for i in range(20)]
    mouvement=["Go_Turnright","Stop","Go_Turnleft","Stop","Stop","Stop"]
    mouvement[4:4]= Up
    mouvement[25:25]=Down
    #print(mouvement)

    Time=[0.005 for i in range(20)]
    Time2=[0.005 for i in range(20)]
    temps_move=[1,1,1,1,1,1,0]
    temps_move[4:4]= Time
    temps_move[25:25]= Time2
    #print(temps_move)

    for i in range(len(mouvement)):
        envoie_donnee(mouvement[i])
        time.sleep(temps_move[i])