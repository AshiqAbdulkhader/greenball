int data;
void setup() {
  Serial.begin(9600);
  pinMode(12,OUTPUT); //pin for Red LED
  pinMode(8,OUTPUT); //pin for Green LED
  

}

void loop() {
  while (Serial.available())  //checks for serial data
  {
    data = Serial.read();    //read serial data
    if(data=='1')
    {
      digitalWrite(8,HIGH);    //if serial data is 1, green LED glows
      digitalWrite(12,LOW);
    }
    else if(data=='0')
    {
      digitalWrite(12,HIGH);   // //if serial data is 0, red LED glows
      digitalWrite(8,LOW);
    }
    
  }

}
