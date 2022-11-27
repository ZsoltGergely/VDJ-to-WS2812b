#include "Adafruit_NeoPixel.h"

#define PIN      2
#define NUMPIXELS 75


Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

int speed=1, mode=1, palette=1, max_brightness=255, brightness=0;
char input[30];

// Get next command from Serial (add 1 for final 0)


void setup() {
Serial.begin(115200);
pinMode(LED_BUILTIN, OUTPUT);

pixels.begin();

// for(int i=0; i<100; i++) {
//   pixels.clear();
//   pixels.setBrightness(i);
//   pixels.fill(pixels.Color(255, 0, 255), 0, NUMPIXELS);
//   pixels.show();
// }
}

void loop() {
  while (Serial.available () == 0)
  {
    digitalWrite(LED_BUILTIN, HIGH); 
  }digitalWrite(LED_BUILTIN, LOW);
  int availableBytes = Serial.readBytesUntil('&', input, 30);
  // while(Serial.available() > 0) {
  //   char t = Serial.read();
  // }

  char* command = NULL;
  char *strings[6];

  // Read each command pair 
  command = strtok(input, ";");
  byte index = 0;
  while (command != NULL)
  {
      strings[index] = command;
      index++;
      command = strtok(NULL, ";");
  }


  brightness = atoi(strings[0]);
  palette = atoi(strings[1]);
  max_brightness = atoi(strings[2]);
  mode = atoi(strings[3]);
  speed = atoi(strings[4]);


  if (brightness == 0)
  {
    pixels.clear();
    pixels.fill(pixels.Color(0, 0, 0), 0, NUMPIXELS);
    pixels.show();
  }else{
    pixels.clear();
    pixels.setBrightness(brightness*max_brightness/100);
    pixels.fill(set_color(palette, speed), 0, NUMPIXELS);
    pixels.show();

  }


}


uint32_t set_color(int palette, int speed){
   switch (palette) {
    case 0: 
    return Rainbow(millis()/(100-speed+1));
    
    case 1: 
    return Sunset(millis()/(100-speed+1));
    
    case 2: 
    return Ocean(millis()/(100-speed+1));
    
    case 3: 
    return PinaColada(millis()/(100-speed+1));
    
    case 4: 
    return Sulfur(millis()/(100-speed+1));
    
    case 5: 
    return NoGreen(millis()/(100-speed+1));
    
    case 6: 
    return USA(millis()/(100-speed+1));
    
   }
}
uint32_t Rainbow(unsigned int i) {
  if (i > 1529) return Rainbow(i % 1530);
  if (i > 1274) return pixels.Color(255, 0, 255 - (i % 255));   //violet -> red
  if (i > 1019) return pixels.Color((i % 255), 0, 255);         //blue -> violet
  if (i > 764) return pixels.Color(0, 255 - (i % 255), 255);    //aqua -> blue
  if (i > 509) return pixels.Color(0, 255, (i % 255));          //green -> aqua
  if (i > 255) return pixels.Color(255 - (i % 255), 255, 0);    //yellow -> green
  return pixels.Color(255, i, 0);                               //red -> yellow
}
uint32_t Sunset(unsigned int i) {
  if (i > 1019) return Sunset(i % 1020);
  if (i > 764) return pixels.Color((i % 255), 0, 255 - (i % 255));          //blue -> red
  if (i > 509) return pixels.Color(255 - (i % 255), 0, 255);                //purple -> blue
  if (i > 255) return pixels.Color(255, 128 - (i % 255) / 2, (i % 255));    //orange -> purple
  return pixels.Color(255, i / 2, 0);                                       //red -> orange
}

uint32_t Ocean(unsigned int i) {
  if (i > 764) return Ocean(i % 765);
  if (i > 509) return pixels.Color(0, i % 255, 255 - (i % 255));  //blue -> green
  if (i > 255) return pixels.Color(0, 255 - (i % 255), 255);      //aqua -> blue
  return pixels.Color(0, 255, i);                                 //green -> aqua
}

uint32_t PinaColada(unsigned int i) {
  if (i > 764) return PinaColada(i % 765);
  if (i > 509) return pixels.Color(255 - (i % 255) / 2, (i % 255) / 2, (i % 255) / 2);  //red -> half white
  if (i > 255) return pixels.Color(255, 255 - (i % 255), 0);                            //yellow -> red
  return pixels.Color(128 + (i / 2), 128 + (i / 2), 128 - i / 2);                       //half white -> yellow
}

uint32_t Sulfur(unsigned int i) {
  if (i > 764) return Sulfur(i % 765);
  if (i > 509) return pixels.Color(i % 255, 255, 255 - (i % 255));   //aqua -> yellow
  if (i > 255) return pixels.Color(0, 255, i % 255);                 //green -> aqua
  return pixels.Color(255 - i, 255, 0);                              //yellow -> green
}

uint32_t NoGreen(unsigned int i) {
  if (i > 1274) return NoGreen(i % 1275);
  if (i > 1019) return pixels.Color(255, 0, 255 - (i % 255));         //violet -> red
  if (i > 764) return pixels.Color((i % 255), 0, 255);                //blue -> violet
  if (i > 509) return pixels.Color(0, 255 - (i % 255), 255);          //aqua -> blue
  if (i > 255) return pixels.Color(255 - (i % 255), 255, i % 255);    //yellow -> aqua
  return pixels.Color(255, i, 0);                                     //red -> yellow
}

//NOTE: This is an example of a non-gradient palette: you will get straight red, white, or blue
//      This works fine, but there is no gradient effect, this was merely included as an example.
//      If you wish to include it, put it in the switch-case in ColorPalette() and add its
//      threshold (764) to thresholds[] at the top.
uint32_t USA(unsigned int i) {
  if (i > 764) return USA(i % 765);
  if (i > 509) return pixels.Color(0, 0, 255);      //blue
  if (i > 255) return pixels.Color(128, 128, 128);  //white
  return pixels.Color(255, 0, 0);                   //red
}
