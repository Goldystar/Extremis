#include<EEPROM.h>
#include <SoftwareSerial.h> // Library for using serial communication
SoftwareSerial SIM(9, 8); // Pins 7, 8 are used as used as software serial pins

String incomingData;   // for storing incoming serial data
String message = "";   // A String for storing the message
int Motor_pin = 4 ;    // Initialized a pin for relay module
int send_ON = 0 ;

int sendoff = 0 ;
int power_count = 0 ;

void setup()
{
  Serial.begin(9600); // baudrate for serial monitor
  SIM.begin(9600); // baudrate for GSM shield

  pinMode(Motor_pin, OUTPUT);   // Setting erlay pin as output pin
  delay(12000);
  
  // set SMS mode to text mode
  SIM.print("AT+CMGF=1\r");  
  delay(100);

}

void loop()
{
  //Function for receiving sms
  receive_message();

  // if received command is to turn on motor
  if(incomingData.indexOf("Motor on")>=0)//sends message if motor is turned on
  {
    digitalWrite(Motor_pin, HIGH);
    message = "Motor is turned ON";

    if( send_ON == 0){
    send_message(message);
  //  E0 = EEPROM.write(0,1);
    send_ON = 1 ;
    }
  }
  
  // if received command is to turn off motor
  if(incomingData.indexOf("Motor off")>=0)//sends message if motor is turned on
  {
    digitalWrite(Motor_pin, LOW);
    message = "Motor is turned OFF";
    
    if(sendoff = 0){
   // E0 = EEPROM.write(0,0);
    send_message(message);
    sendoff = 1 ;
    }
    
  }



int Main = digitalRead(6);

  if(Main==0){ // if power is off
     if(power_count==0){
       message = "Power OFF";
       send_message(message);
       power_count = 1;
     //  EEPROM.write(1,0);
      }
     }
     
  if ((Main==0) && (power_count == 1) ){
    digitalWrite(Motor_pin, LOW);
    
  }
  
}

void receive_message()
{
  if (SIM.available() > 0)
  {
    incomingData = SIM.readString(); // Get the data from the serial port.
    Serial.print(incomingData); 
    delay(1000); 
  }
}

void send_message(String message)
{
  SIM.println("AT+CMGF=1");    //Set the GSM Module in Text Mode
  delay(100);  
  SIM.println("AT+CMGS=\"+918490809159\""); // Replace it with your mobile number
  delay(100);
  SIM.println(message);   // The SMS text you want to send
  delay(100);
  SIM.println((char)26);  // ASCII code of CTRL+Z
  delay(100);
  SIM.println();
  delay(1000);  
}
