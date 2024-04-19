#include <LiquidCrystal_I2C.h>
#include "pitches.h"


// Constants
const int LED1 = 11;
const int LED2 = 10;
const int ROCKER_SWITCH = 4;
const int BEEFCAKE_RELAY = 12;
const int RAISE_BUTTON = 2;
const int LOWER_BUTTON = 5;
const int MAX_TEMP = 42;
const int MIN_TEMP = 20;
const int SPEAKER_PIN = 8;


// Global variables
int temp = 25;
bool WIRE_POWER = true;
bool GOAL_TEMP_REACHED = false;
LiquidCrystal_I2C lcd(0x27, 16, 20);


// Custom character
byte Celsius[8] = {
 B11000, B11000, B00011, B00100, B00100, B00100, B00011
};


// Melodies
int good_melody[] = {NOTE_G5, NOTE_A5, NOTE_B5, NOTE_C6};
int bad_melody[] = {NOTE_GS4, NOTE_GS4, 0, NOTE_GS4, NOTE_GS4, 0, NOTE_GS4, NOTE_GS4};


void setup() {
 Serial.begin(9600);
 setupLCD(); //initializing LCD Screen
 setupPins(); //initializing Pins
}


void loop() {
 if (digitalRead(ROCKER_SWITCH) == LOW) {
   activateSystem();
 } else {
   deactivateSystem();
 }
}


/*
* Initializing LCD Screen
*/
void setupLCD() {
 lcd.init();
 lcd.createChar(0, Celsius);
 lcd.backlight();
 displaySetTemp(); //displaying set temperature
}


/*
* Initializing all pins
*/
void setupPins() {
 pinMode(ROCKER_SWITCH, INPUT_PULLUP);
 pinMode(RAISE_BUTTON, INPUT_PULLUP);
 pinMode(LOWER_BUTTON, INPUT_PULLUP);
 pinMode(BEEFCAKE_RELAY, OUTPUT);
 pinMode(LED1, OUTPUT);
 pinMode(LED2, OUTPUT);
 pinMode(A2, INPUT);
 pinMode(A3, INPUT)
}


/*
* System is turned on
*/
void activateSystem() {
 digitalWrite(BEEFCAKE_RELAY, WIRE_POWER); //turning on or off the beefcake
 digitalWrite(LED1, HIGH);
 digitalWrite(LED2, HIGH);


 handleTemperatureControl(); //doing all temperature calculations


 int prevTemp = temp;
 adjustTemperature(); //checking for temperature button adjustments
 if (prevTemp != temp) {
   displaySetTemp(); //displaying new set temperature
 }
}


/*
* System is turned off
*/
void deactivateSystem() {
 lcd.noBacklight();
 lcd.noDisplay();
 digitalWrite(BEEFCAKE_RELAY, LOW);
 digitalWrite(LED1, LOW);
 digitalWrite(LED2, LOW);
}


/*
* Check the temperature button for adjustments
*/
void adjustTemperature() {
 if (digitalRead(RAISE_BUTTON) == LOW) {
   temp = min(temp + 1, MAX_TEMP); //Ensuring the range is not violated
 } else if (digitalRead(LOWER_BUTTON) == LOW) {
   temp = max(temp - 1, MIN_TEMP); //Ensuring the range is not violated
 }
 GOAL_TEMP_REACHED = false;
}


/*
* Displaying set temperature on LCD Screen
*/
void displaySetTemp() {
 lcd.clear();
 lcd.setCursor(0, 0);
 lcd.print("Set Temp: ");
 lcd.print(temp);
 lcd.setCursor(11,0);
 lcd.write(0);
}


/*
* Checking validity of temperature and displaying it
*/
void handleTemperatureControl() {
 float currentTemp = measureTemperature(); //getting current measured temperature
 lcd.setCursor(0, 1);
 lcd.print("Meas. Temp: ");
 lcd.setCursor(11,1);
 lcd.print(currentTemp);
 lcd.setCursor(15,1);
 lcd.write(0);


 //if the max temperature bound is being violated
 if (currentTemp > MAX_TEMP) {
   WIRE_POWER = false;
   playMelody(bad_melody, sizeof(bad_melody) / sizeof(bad_melody[0])); //play sound
 }else if (currentTemp == temp && GOAL_TEMP_REACHED == false){
   WIRE_POWER = false;
   GOAL_TEMP_REACHED = true;
   playMelody(good_melody, sizeof(good_melody) / sizeof(good_melody[0])); //play sound
 }else{
   WIRE_POWER = true;
 }


}


float measureTemperature() {
 float voltage = (analogRead(A2) + analogRead(A3)) / 2.0 * (5.0 / 1024.0);
 float resistance = ((voltage/(5.0*2.0)*10000.0)/(1.0-(voltage/(5.0*2.0)));
 float temperature = log(resistance/27316.0)/(-0.04);
 float adjusted_temperature = temperature-2.5;
 return adjusted_temperature;
}


void playMelody(int melody[], int size) {
 for (int i = 0; i < size; i++) {
   tone(SPEAKER_PIN, melody[i], 125);
   delay(125);
 }
}
