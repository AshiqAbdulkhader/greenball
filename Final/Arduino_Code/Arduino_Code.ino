char state;
void setup() {
  Serial.begin(9600);
  pinMode(12,OUTPUT); //pin for Red LED
  pinMode(13,OUTPUT); //pin for Green LED
  

}

void loop() {
  while (Serial.available())  //checks for serial data
  {
    state = Serial.read();    //read serial data
    if(state=='H')
    {
      digitalWrite(13,HIGH);    //if serial data is 1, green LED glows
      digitalWrite(12,LOW);
    }
    else if(state=='L')
    {
      digitalWrite(12,HIGH);   // //if serial data is 0, red LED glows
      digitalWrite(13,LOW);
    }
    
  }

}
