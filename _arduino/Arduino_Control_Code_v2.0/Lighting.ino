void colorWipeMotors(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    moveCWStep();
    delay(wait);
  }
}

void stripUpdate() {
  strip.setBrightness(int(commands[7] * 2));
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    if (i >= commands[1] && i < commands[2]) {
      strip.setPixelColor(i, int(commands[3] * 2.55), int(commands[4] * 2.55), int(commands[5] * 2.55), int(commands[6] * 2.55));
    }
  }
}

void lightshow() {
  strip.show();
}

void stripReset() {
  strip.setBrightness(int(20 * 2));
  strip.clear();
  strip.show();
}

void colorWipe(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

void disco(int wait) {
  while (!Serial.available())
  {
    int firstPixelHue = 0;     // First pixel starts at red (hue 0)
    for (int a = 0; a < 30; a++) { // Repeat 30 times...
      for (int b = 0; b < 3; b++) { //  'b' counts from 0 to 2...
        strip.clear();         //   Set all pixels in RAM to 0 (off)
        // 'c' counts up from 'b' to end of strip in increments of 3...
        for (int c = b; c < strip.numPixels(); c += 3) {
          // hue of pixel 'c' is offset by an amount to make one full
          // revolution of the color wheel (range 65536) along the length
          // of the strip (strip.numPixels() steps):
          int      hue   = firstPixelHue + c * 65536L / strip.numPixels();
          uint32_t color = strip.gamma32(strip.ColorHSV(hue)); // hue -> RGB
          strip.setPixelColor(c, color); // Set pixel 'c' to value 'color'
        }
        strip.show();                // Update strip with new contents
        aciveDelay(wait);                 // Pause for a moment
        firstPixelHue += 65536 / 90; // One cycle of color wheel over 90 frames
      }
    }
  }

}

// Rainbow cycle along whole strip. Pass delay time (in ms) between frames.
void rainbow(int wait) {
  // Hue of first pixel runs 5 complete loops through the color wheel.
  // Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to 5*65536. Adding 256 to firstPixelHue each time
  // means we'll make 5*65536/256 = 1280 passes through this outer loop:
  while (!Serial.available())
  { for (long firstPixelHue = 0; firstPixelHue < 5 * 65536 && !Serial.available(); firstPixelHue += 256) {
      for (int i = 0; i < strip.numPixels(); i++) { // For each pixel in strip...
        // Offset pixel hue by an amount to make one full revolution of the
        // color wheel (range of 65536) along the length of the strip
        // (strip.numPixels() steps):
        int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
        // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
        // optionally add saturation and value (brightness) (each 0 to 255).
        // Here we're using just the single-argument hue variant. The result
        // is passed through strip.gamma32() to provide 'truer' colors
        // before assigning to each pixel:
        strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
      }
      strip.show(); // Update strip with new contents
      aciveDelay(wait);  // Pause for a moment
    }
  }

}

void sunCycle(int wait,int pix) {

  int      head          = pix;
  int      tail          = 0;
  long     lastTime      = millis();
  uint32_t firstPixelHue = 0;

  while (!Serial.available()) { // Repeat forever (or until a 'break' or 'return')
    for (int i = 0; i < strip.numPixels(); i++) { // For each pixel in strip...
      if (((i >= tail) && (i <= head)) ||     //  If between head & tail...
          ((tail > head) && ((i >= tail) || (i <= head)))) {
        strip.setPixelColor(i, strip.Color(0, 0, 0, 255)); // Set white
      } else {                                             // else set rainbow
        strip.setPixelColor(i, 0, 255, 0,0 );
      }
    }

    strip.show(); // Update strip with new contents
    // There's no delay here, it just runs full-tilt until the timer and
    // counter combination below runs out.

    firstPixelHue += 40; // Advance just a little along the color wheel

    long temp = millis() - lastTime;
    
    if (temp > wait*1000L) { // Time to update head/tail?
      if (++head >= strip.numPixels()) {     // Advance head, wrap around
        head = 0;
      }
      if (++tail >= strip.numPixels()) {     // Advance tail, wrap around
        tail = 0;
      }
      lastTime = millis();                   // Save time of last movement
    }
  }
}

void pulse(uint8_t wait) {
  while (!Serial.available()) {
    for (int j = 0; j < 256; j++) { // Ramp up from 0 to 255
      // Fill entire strip with white at gamma-corrected brightness level 'j':
      strip.fill(strip.Color(0, 0, 0, strip.gamma8(j)));
      strip.show();
      aciveDelay(wait);
    }

    for (int j = 255; j >= 0; j--) { // Ramp down from 255 to 0
      strip.fill(strip.Color(0, 0, 0, strip.gamma8(j)));
      strip.show();
      aciveDelay(wait);
    }
  }

}

void aciveDelay(int wait)
{
  for (int i = 0; i < wait && !Serial.available(); i++)
  {
    delay(1);
  }
}
