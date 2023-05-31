#include <Arduino.h>                                            
#include <WiFi.h>                                               //Enables WiFi connectivity
#include <WiFiClient.h>                                         //Enables TCP
#include <driver/ledc.h>                                        //PWM library
#include <Adafruit_NeoPixel.h>                                  //NeoPixel LED library

const char* ssid = "momodumm";                                  //SSID of network
const char* password = "moinmoin";                              //Password of network

const char* server_address = " 192.168.214.36";                  //IP address of computer running Python script
const int server_port = 8080;                                   //Server Port

const int Motor1FWDchannel = 0;                                 //Channels of the PWM pins of the Feather V2
const int Motor1BWDchannel = 1;
const int Motor2FWDchannel = 2;
const int Motor2BWDchannel = 3;
const int Motor3FWDchannel = 4;
const int Motor3BWDchannel = 5;

const int Motor1FWD = 12;                                       //Pins of the Feather V2
const int Motor1BWD = 13;
const int Motor2FWD = 27;
const int Motor2BWD = 33;
const int Motor3FWD = 15;
const int Motor3BWD = 32;

int PWMvalue1;                                                  //PWM values for each motor
int PWMvalue2;
int PWMvalue3;

int PWMsign1;                                                   //PWM signs for each motor
int PWMsign2;
int PWMsign3;

uint8_t PWMsignals[6];                                          //Array of 6 bytes received from server

const int PWMfrequency = 5000;                                  //PWM frequency of 5000Hz

const int PWMresolution = 8;                                    //PWM resolution of 8 bit

WiFiClient client;                                              //Declares WifiClient object

Adafruit_NeoPixel StatusLED(1, 0, NEO_GRB + NEO_KHZ800);        //Declares NeoPixel object

void ConnectToWifi() {                                          // Sets up connection to the specified network
  WiFi.mode(WIFI_MODE_STA); 
  WiFi.begin(ssid, password);                                  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
    StatusLED.setBrightness(128);                               //Status LED brightness at 50%
    StatusLED.setPixelColor(0, StatusLED.Color(255, 0, 0));     //Status LED color, Red if looking for Wifi
    StatusLED.show();                                           //Updates Status LED
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());                               //Prints out device IPv4 address
  StatusLED.setBrightness(128);                                 //Status LED brightness at 50%
  StatusLED.setPixelColor(0, StatusLED.Color(0, 0, 255));       //Status LED color, Blue if connected to Wifi
  StatusLED.show();                                             //Updates Status LED
}

void SetupPWMPins() {                                           //Maps each of the six PWM channels and pins

  ledcSetup(Motor1FWDchannel, PWMfrequency, PWMresolution);
  ledcSetup(Motor1BWDchannel, PWMfrequency, PWMresolution);
  ledcSetup(Motor2FWDchannel, PWMfrequency, PWMresolution);
  ledcSetup(Motor2BWDchannel, PWMfrequency, PWMresolution);
  ledcSetup(Motor3FWDchannel, PWMfrequency, PWMresolution);
  ledcSetup(Motor3BWDchannel, PWMfrequency, PWMresolution);

  ledcAttachPin(Motor1FWD, Motor1FWDchannel);
  ledcAttachPin(Motor1BWD, Motor1BWDchannel);
  ledcAttachPin(Motor2FWD, Motor2FWDchannel);
  ledcAttachPin(Motor2BWD, Motor2BWDchannel);
  ledcAttachPin(Motor3FWD, Motor3FWDchannel);
  ledcAttachPin(Motor3BWD, Motor3BWDchannel);

}

void ConnectToTCP() {                                           //Connects to server via TCP

  if (!client.connected()) {
      Serial.print("Connecting to server...");
      if (client.connect(server_address, server_port)) {
        Serial.println("Connected to server!");
        StatusLED.setBrightness(128);                          //Status LED brightness at 50%
        StatusLED.setPixelColor(0, StatusLED.Color(0, 255, 0));//Status LED color, Green if connected to Wifi
        StatusLED.show();                                      //Updates Status LED
      } else {
        Serial.println("Connection failed");
        return;
      }
    }

}

void ReceiveDatafromServer() {                                  //Receives data from server via TCP

  if (client.connected()) {                                  
      if (client.available()) {
        client.read(PWMsignals, 6);                             //Reads out a 6 byte value called PWMsignals containing PWM values and signs, PWM values from 0-255 and 0 for - 1 for +
        
        PWMvalue1 = PWMsignals[0];                              //Maps each value to the specific motor
        PWMvalue2 = PWMsignals[1];
        PWMvalue3 = PWMsignals[2];
        PWMsign1 = PWMsignals[3];
        PWMsign2 = PWMsignals[4];
        PWMsign3 = PWMsignals[5];
      }
  }

}

void SetMotorSpeed() {                                          // Motor speed and direction is assigned to each PWM pin
 Serial.println(String(PWMvalue1) + " " + String(PWMvalue2) + " " + String(PWMvalue3) + " " + String(PWMsign1) + " " + String(PWMsign2) + " " + String(PWMsign3));
  if(PWMsign1 == 1) {                                           //Motor 1
      ledcWrite(Motor1FWDchannel, PWMvalue1);
      ledcWrite(Motor1BWDchannel, 0);
  }
  else{
      ledcWrite(Motor1BWDchannel, PWMvalue1);
      ledcWrite(Motor1FWDchannel, 0);
  }

  if(PWMsign2 == 1) {                                           //Motor 2
      ledcWrite(Motor2FWDchannel, PWMvalue2);
      ledcWrite(Motor2BWDchannel, 0);
  }
  else{
      ledcWrite(Motor2BWDchannel, PWMvalue2);
      ledcWrite(Motor2FWDchannel, 0);
  }

  if(PWMsign3 == 1) {                                           //Motor 3
      ledcWrite(Motor3FWDchannel, PWMvalue3);
      ledcWrite(Motor3BWDchannel, 0);
  }
  else{
      ledcWrite(Motor3BWDchannel, PWMvalue3);
      ledcWrite(Motor3FWDchannel, 0);
  }
}

void setup() {
  Serial.begin(115200);                                         //Sets baud rate for serial monitor
  StatusLED.begin();                                            //Sets up status LED
  ConnectToWifi();                                          
  SetupPWMPins();
}

void loop() {
  ConnectToTCP();
  ReceiveDatafromServer();     
  SetMotorSpeed();                                                
}
