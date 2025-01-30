import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

def envoie_donnee(mouvement):
    mouvements= {"Stop":"1", "Go_Forward":"2", "Go_Backward":"3","Go_Turnright":"4","Go_Turnleft":"5", "Up_tab":"u","Down_Tab":"d"}
    if mouvement in mouvements: 
       message= str(mouvements[mouvement])
       arduino.write((message+ '\n').encode())
       print(f"Commande:{mouvement}({message})")
       
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

def forward():
    envoie_donnee("Go_Forward")

def backward():
    envoie_donnee("Go_Backward")

def turn_right():
    envoie_donnee("Go_Turnright")

def turn_left():
    envoie_donnee("Go_Turnleft")

def up_screen():
    envoie_donnee("Up_tab")

def down_screen():
    envoie_donnee("Down_Tab")

def stop():
    envoie_donnee("Stop")