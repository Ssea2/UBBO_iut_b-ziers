/*
Pin 0: NC
Pin 1: NC
Pin 2: (E1 ASM 1) PWM wheel Front Right
Pin 3: (M1 ASM 1) DIR wheel Front Right
Pin 4: NC
Pin 5: (E2 ASM 1) PWM wheel Back Right
Pin 6: (M2 ASM 1) DIR wheel Back Right
Pin 7: NC
Pin 8: (E1 ASM 2) PWM wheel Back Left
Pin 9: (M1 ASM 2) DIR wheel Back Left
Pin 10: NC
Pin 11: (E2 ASM 2) PWM wheel Front Left
Pin 12: (M2 ASM 2) DIR wheel Front Left
Pin 13: NC
Pin 14: Serial 3 for Arduino Servo controller
Pin 15: NC
Pin 16 : (Internal) RX Carte bluetooth (Serial 2)
Pin 17 : (Internal) TX Carte bluetooth 
Pin 18 : (4 motor 1)Encoder signal B wheel Front Right
Pin 19 : (4 motor 2)Encoder signal B wheel Back Left
Pin 20 : (3 motor 3) Encoder signal A wheel Back Right
Pin 21 : (3 motor 4) Encoder signal A wheel Front Left
Pin 22 : NC
Pin 23 : NC
Pin 24 : NC 
Pin 25 : NC 
Pin 26 : NC
Pin 27 : NC
Pin 28 : Dock station IR detection front left
Pin 29 : Dock station IR detection front center
Pin 30 : Dock station IR detection front right
Pin 31 : (3 motor 1) Encoder signal A wheel Front Right
Pin 32 : (3 motor 2) Encoder signal A wheel Back Left
Pin 33 : (4 motor 3) Encoder signal B wheel Back Right
Pin 34 : (4 motor 4) Encoder signal B wheel Front Left
Pin 39 : Dock relay Pin
Pin 40 : Docked Digital Pin
Pin A0 : Battery Voltage Pin
Pin A6 : Proximity sensor Front
Pin A7 : Proximity sensor Left
Pin A8 : Proximity sensor Back
Pin A9 : Proximity sensor Right


M1 Red Wire: ((+)1 ASM 1) 
M1 black Wire: ((-)1 ASM 1) 
M2 Red Wire: ((+)2 ASM 1) 
M2 black Wire: ((-)2 ASM 1) 
M3 Red Wire: ((-)1 ASM 2) 
M3 black Wire: ((+)1 ASM 2) 
M4 Red Wire: ((-)2 ASM 2) 
M4 black Wire: ((+)2 ASM 2) 

*/

#include <Arduino.h>
#include <Servo.h>

//moteur
const int pwmFrontRight = 2;  // PWM pour roue avant droite
const int dirFrontRight = 3;  // Direction pour roue avant droite
const int pwmBackRight = 5;   // PWM pour roue arrière droite
const int dirBackRight = 6;   // Direction pour roue arrière droite
const int pwmBackLeft = 8;    // PWM pour roue arrière gauche
const int dirBackLeft = 9;    // Direction pour roue arrière gauche
const int pwmFrontLeft = 11;  // PWM pour roue avant gauche
const int dirFrontLeft = 12;  // Direction pour roue avant gauche

//servo
Servo myServo;
int servoPin = 26;  // Pin sur lequel est connecté le servo
// Position fixe du servo, remplace par la valeur souhaitée
int pos = 28;
//const char STX = 0x02;  // Start of text
//const char ETX = 0x03;  // End of text


//ultrason 
const int proximityFront = A6;  // Capteur avant

//variable distance
const int detectionDistance = 20;
int distance = 100;

int vm1 = 40;
int vm2 = 40;
int vm4 = 40;
int vm3=20;

int byCmd=49;

const int STOP= 49; // serial terminal = 1
const int GO_FORWARD= 50; // serial terminal = 2
const int GO_BACKWARD= 51; // serial terminal = 3
const int GO_TURNRIGHT= 52; // serial terminal = 4
const int GO_TURNLEFT= 53; // serial terminal = 5
const int UP_TAB = 117; //serial terminal = u
const int DOWN_TAB = 100; //serial terminal = d

unsigned long previousMillis = 0;  // Stocke le dernier temps d'impression
const long interval = 3000;        // Intervalle de 3 secondes (en millisecondes)


//variable bluetooth
char c = 0;

void moveForeward(){

  digitalWrite(dirFrontRight, LOW); // Avant droite en marche avant (M1)
  analogWrite(pwmFrontRight, vm1);   // Vitesse maximale pour avant droite
  digitalWrite(dirBackRight, LOW);  //(M2)
  analogWrite(pwmBackRight, vm2);   
  digitalWrite(dirBackLeft, LOW);   // (M3)
  analogWrite(pwmBackLeft, vm3);     
  digitalWrite(dirFrontLeft, LOW);  // (M4)
  analogWrite(pwmFrontLeft, vm4);    
}

void moveBackward(){

  digitalWrite(dirFrontRight, HIGH); // Avant droite en marche avant (M1)
  analogWrite(pwmFrontRight, vm1);   // Vitesse maximale pour avant droite
  digitalWrite(dirBackRight, HIGH);  //(M2)
  analogWrite(pwmBackRight, vm2);   
  digitalWrite(dirBackLeft, HIGH);   // (M3)
  analogWrite(pwmBackLeft, vm3);     
  digitalWrite(dirFrontLeft, HIGH);  // (M4)
  analogWrite(pwmFrontLeft, vm4);     
}

void turnLeft(){

  digitalWrite(dirFrontRight, LOW); 
  analogWrite(pwmFrontRight, vm1);
  digitalWrite(dirBackRight, LOW);  
  analogWrite(pwmBackRight, vm2);    
  digitalWrite(dirBackLeft, HIGH);   
  analogWrite(pwmBackLeft, vm3);     
  digitalWrite(dirFrontLeft, HIGH);  
  analogWrite(pwmFrontLeft, vm4);   
}

void turnRight() {

  digitalWrite(dirFrontRight, HIGH); 
  analogWrite(pwmFrontRight, vm1);
  digitalWrite(dirBackRight, HIGH);  
  analogWrite(pwmBackRight, vm2);    
  digitalWrite(dirBackLeft, LOW);   
  analogWrite(pwmBackLeft, vm3);     
  digitalWrite(dirFrontLeft, LOW);  
  analogWrite(pwmFrontLeft, vm4);   
}

void stopMotors() {
  analogWrite(pwmFrontRight, 0); 
  analogWrite(pwmBackRight, 0);   
  analogWrite(pwmBackLeft, 0);    
  analogWrite(pwmFrontLeft, 0);   
}

void servoUp() {
  if (pos <= 90) {
    pos++;
    Serial.print("Position: ");
    Serial.println(pos);
    myServo.write(pos);
    delay(15);
  }
}

void servoDown() {
  if (pos >= 0) {
    pos--;
    Serial.print("Position: ");
    Serial.println(pos);
    myServo.write(pos);
    delay(15);
  }

}

void setup() {
  // Configuration
  pinMode(pwmFrontRight, OUTPUT);
  pinMode(dirFrontRight, OUTPUT);
  pinMode(pwmBackRight, OUTPUT);
  pinMode(dirBackRight, OUTPUT);
  pinMode(pwmBackLeft, OUTPUT);
  pinMode(dirBackLeft, OUTPUT);
  pinMode(pwmFrontLeft, OUTPUT);
  pinMode(dirFrontLeft, OUTPUT);

  pinMode(proximityFront, INPUT);  
  myServo.attach(servoPin);
  myServo.write(pos); // Set the servo to the starting position
  delay(500);  
  // Initialisation de la communication série avec le module Bluetooth (via Serial1 sur pins RX1 et TX1)
  //Serial1.begin(9600);
  Serial.begin(9600);

  // Message d'initialisation
  //Serial.println("Module Bluetooth prêt")

}

void loop() {

  byCmd = Serial.read();
  if (byCmd != -1) {
    Serial.println(byCmd);
  }

  // Mesurer la distance avec le capteur de proximité avant
  distance = analogRead(proximityFront);
  distance = map(distance, 0, 1023, 0, 100);

  // Obtenir le temps actuel
  unsigned long currentMillis = millis();

  // Exécuter les commandes et mouvements en fonction de la distance et des commandes reçues
  switch(byCmd) {
    case STOP:
      stopMotors();
      break;
    case GO_FORWARD:
      moveForeward();
      break;
    case GO_BACKWARD:
      moveBackward();
      break;
    case GO_TURNLEFT:
      turnLeft();
      break;
    case GO_TURNRIGHT:
      turnRight();
      break;
    case UP_TAB:
      servoUp();
      break;
    case DOWN_TAB:
      servoDown();
      break;
    }

    // Increment position and print value
  
  
  // Decrement position and print value
  

  delay(100);
  byCmd = STOP;  // Remet la commande par défaut à STOP
}






