int xpin = A0;
int ypin = A1;
int zpin = A2;

float threshold = 6;
float xval[100] = {0};
float yval[100] = {0};
float zval[100] = {0};
float xavg;
float yavg;
float zavg;

int steps = 0;
int state = 0;

void setup() {
  Serial.begin(9600);
  calibrate();
}

void loop() {
  int acc = 0;
  float totvect[100] = {0};
  float totave[100] = {0};
  float xaccl[100] = {0};
  float yaccl[100] = {0};
  float zaccl[100] = {0};

  for (int i=0;i<100;i++) {
    xaccl[i] = float(analogRead(xpin) - 345);
    delay(1);
    yaccl[i] = float(analogRead(ypin) - 346);
    delay(1);
    zaccl[i] = float(analogRead(zpin) - 416);
    delay(1);
    
    totvect[i] = sqrt(((xaccl[i]-xavg)*(xaccl[i]-xavg)) + ((yaccl[i]-yavg)*(yaccl[i]-yavg)) + ((zaccl[i]-zavg)*(zaccl[i]-zavg)));
    totave[i] = (totvect[i] + totvect[i-1]) / 2;
    
    //delay(200);
    delay(100);

    if (totave[i] > threshold && state == 0) {
      steps = steps + 1;
      state = 1;
    }

    if (totave[i] < threshold && state == 1) {
      state = 0;
    }
    Serial.println(steps);
  };
  //delay(200);
  delay(1000);
}

void calibrate() {
  float sum = 0;
  float sum1 = 0;
  float sum2 = 0;
  
  for (int i=0;i<100;i++) {
    xval[i] = float(analogRead(xpin) - 345);
    sum = xval[i] + sum;
  }
  xavg = sum / 100.0;
  delay(100);
  
  for (int i=0;i<100;i++) {
    yval[i] = float(analogRead(ypin) - 346);
    sum1 = yval[i] + sum1;
  }
  yavg = sum1 / 100.0;
  delay(100);
  
  for (int i=0;i<100;i++) {
    zval[i] = float(analogRead(zpin) - 416);
    sum2 = zval[i] + sum2;
  }
  zavg = sum2 / 100.0;
  delay(100);
}
