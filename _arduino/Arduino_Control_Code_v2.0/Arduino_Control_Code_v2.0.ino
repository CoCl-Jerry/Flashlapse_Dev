#include <Adafruit_NeoPixel.h>

#define COMMANDSIZE 8
#define LED_PIN 6
#define NUMPIXELS 86
#define BRIGHTNESS 50

#define MOTORPIN1 A1
#define MOTORPIN2 A2
#define MOTORPIN3 A4
#define MOTORPIN4 A5
#define IR_PIN 13
#define STEPS 2038

bool inputComplete = false;  // whether the string is complete
int commands[COMMANDSIZE];
char sz[] = "0~00~00~000~000~000~000~000";
String serialResponse = "";

double rpm = 5;
int delayTime = 0;
int currentStep = 0;

Adafruit_NeoPixel strip(NUMPIXELS, LED_PIN, NEO_GRBW + NEO_KHZ800);

void setup() {
  Serial.begin(9600);
  strip.setBrightness(BRIGHTNESS);
  strip.begin(); 
  strip.show();

  pinMode(MOTORPIN1, OUTPUT);
  pinMode(MOTORPIN2, OUTPUT);
  pinMode(MOTORPIN3, OUTPUT);
  pinMode(MOTORPIN4, OUTPUT);
  pinMode(IR_PIN, OUTPUT);
  getdelay();
  startup();

}

void loop() {

}
