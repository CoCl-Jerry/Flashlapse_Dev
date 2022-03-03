void serialEvent() {
  int current = 0;
  clearCMD();
  serialResponse = Serial.readStringUntil('\r\n');
  // Convert from String Object to String.
  char buf[sizeof(sz)];
  serialResponse.toCharArray(buf, sizeof(buf));
  char *p = buf;
  char *str;
  while ((str = strtok_r(p, "~", &p)) != NULL)
  {
    int temp;
    temp = atoi(str);
    commands[current] = temp;
    current++;
  }
  exeCMD();
}

void clearCMD() {
  for (int i = 0; i < COMMANDSIZE; i++)
  {
    commands[i] = 0;
  }
}

void exeCMD() {

  switch (commands[0]) {
    case 0:
      stripReset();
      break;

    case 1:
      stripUpdate();
      break;

    case 2:
      switch (commands[1]) {
        case 0:
          disco(commands[2]);
          break;

        case 1:
          rainbow(commands[2]);
          break;

        case 2:
          sunCycle(commands[2], commands[3]);
          break;

        case 3:
          pulse(commands[2]);
          break;
      }
      break;

    case 3:
      startup();
      break;

    case 4:
      lightshow();
      break;

    case 6:
      delayTime = commands[1];
      break;

    case 7:
      clino();
      break;

    case 8:
      rotate_to(int((commands[1] * 20.38) / 3.6));
      break;

    case 9:
      resetMotors();
      break;

    case 10:
      switch (commands[1]) {
        case 0:
          digitalWrite(IR_PIN, HIGH);
          break;

        case 1:
          digitalWrite(IR_PIN, LOW);
          break;
      }
      break;



  }
}
