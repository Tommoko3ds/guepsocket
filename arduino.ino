#define TRIG_PIN 11
#define ECHO_PIN 12
#define LED_PIN_RED 8
#define LED_PIN_YELLOW 9
#define LED_PIN_GREEN 10
#define LED_PIN 13

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(LED_PIN_RED, OUTPUT); // Pin para el LED rojo
  pinMode(LED_PIN_YELLOW, OUTPUT); // Pin para el LED amarillo
  pinMode(LED_PIN_GREEN, OUTPUT); // Pin para el LED verde
}

void loop() {
  long duration, distance;
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.034 / 2;
  
  Serial.println(distance); // Enviar la distancia medida a través del puerto serial

  // Lógica para encender los LEDs según la distancia medida
  if (distance >= 1 && distance <= 10) {
    digitalWrite(LED_PIN_RED, HIGH); // Encender el LED rojo
    digitalWrite(LED_PIN_YELLOW, LOW); // Apagar el LED amarillo
    digitalWrite(LED_PIN_GREEN, LOW); // Apagar el LED verde
  } else if (distance > 11 && distance <= 30) {
    digitalWrite(LED_PIN_RED, LOW); // Apagar el LED rojo
    digitalWrite(LED_PIN_YELLOW, HIGH); // Encender el LED amarillo
    digitalWrite(LED_PIN_GREEN, LOW); // Apagar el LED verde
  } else if (distance > 31) {
    digitalWrite(LED_PIN_RED, LOW); // Apagar el LED rojo
    digitalWrite(LED_PIN_YELLOW, LOW); // Apagar el LED amarillo
    digitalWrite(LED_PIN_GREEN, HIGH); // Encender el LED verde
  }

  // Lógica para manejar comandos desde el puerto serial
    if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      digitalWrite(LED_PIN, HIGH);
    } else if (command == '0') {
      digitalWrite(LED_PIN, LOW);
    }
  }

  delay(1500);
}
