/*
 * Tektronix Remotely Aimed Video and RF Monitor
 * Language: Arduino
 * 
 * The purpose of this program is to control the Bescor MP-101 Motorized Pan and
 * Tilt Head with an Arduino Micro. The Micro receives control signals via USB 
 * from the field PC, which are being received from a remote PC.
 * 
 * The signals are being sent through a python GUI application made with pyQT.
 * 
 * This application can be found at github.com/mikerichantk/tek17/
 * 
 ******************************************************
 * @version  1.0
 * @date     20 Feb 2021
 * 
 * @author   Addison Raak, Ka'ulu Ng,
 *           Michael Antkiewicz, Nicholas Baldwin
 * 
 ******************************************************
 */

// Value of resistor on back of remote: 3.9k
// Value of potentiometer ranges from 0.25k-18.8k
int speed_pin = 13;
int up = 12;
int right = 9;
int down = 6;
int left = 4;
int count = 0;
void setup() {
  // Setting up the pins for up, right, down, left
  pinMode(up,OUTPUT);
  pinMode(right,OUTPUT);
  pinMode(down,OUTPUT);
  pinMode(left,OUTPUT);
  Serial.begin(9600);
}

void loop() {

  // sets the speed of the motors. Range is from 0-255.
  // When the level is set to 255, it takes about 10 seconds to turn 90 deg.
  analogWrite(speed_pin, 255);
  //Code is using wasd character keys in order to move 
  //up,left,down, and right in that order
  if(Serial.available() > 0){
    //Reads from the serial input 
    int rxd = Serial.read();
    
    //If "w" is pressed, move up
    if(rxd==119){
      digitalWrite(up,HIGH);
      digitalWrite(down,LOW);
      delay(100);
      Serial.println("Moving Up");
    }
    
    //If "a" is pressed, move left
    if(rxd==97){
      digitalWrite(left,HIGH);
      digitalWrite(right,LOW);
      delay(100);
      Serial.println("Moving Left");
    }
    
    //If "s" is pressed, move down 
    if(rxd==115){
      digitalWrite(down,HIGH);
      digitalWrite(up,LOW);
      delay(100);
      Serial.println("Moving Down");
    }
    
    //If "d" is pressed, move right 
    if(rxd==100){
      digitalWrite(right,HIGH);
      digitalWrite(left,LOW);
      delay(100);
      Serial.println("Moving Right");
    }
  }
  else{
    if(count <= 1000){
        count++;
    }
    else{
      count = 0;
      digitalWrite(up,LOW);
      digitalWrite(right,LOW);
      digitalWrite(down,LOW);
      digitalWrite(left,LOW);
    }
  }



}
