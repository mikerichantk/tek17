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
 
int up = 12;
int right = 11;
int down = 10;
int left = 9;
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
  
  //Code is using wasd character keys in order to move 
  //up,left,down, and right in that order
  if(Serial.available() > 0){
    //Reads from the serial input 
    int rxd = Serial.read();
    
    //If "w" is pressed, move up
    if(rxd==119){
      digitalWrite(up,HIGH);
      digitalWrite(down,LOW);
      Serial.println("Moving Up");
    }
    
    //If "a" is pressed, move left
    if(rxd==97){
      digitalWrite(left,HIGH);
      digitalWrite(right,LOW);
      Serial.println("Moving Left");
    }
    
    //If "s" is pressed, move down 
    if(rxd==115){
      digitalWrite(down,HIGH);
      digitalWrite(up,LOW);
      Serial.println("Moving Down");
    }
    
    //If "d" is pressed, move right 
    if(rxd==100){
      digitalWrite(right,HIGH);
      digitalWrite(left,LOW);
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
