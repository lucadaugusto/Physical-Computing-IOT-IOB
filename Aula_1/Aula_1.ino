#include <ArduinoJson.h>

const int pin1 = 6; // Saída acionada quando valor == 1
const int pin2 = 7; // Saída acionada quando valor == 2

int ultimoValor = -1; // Para evitar reescritas desnecessárias


void setup() {

  Serial.begin(9600);   // Comunicação serial
  Serial.setTimeout(100); // Timeout de 100 ms para leitura da serial

  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);

  digitalWrite(pin1, LOW);
  digitalWrite(pin2, LOW);

  Serial.println("Arduino pronto para receber comandos JSON...");
}

void loop() {
  if (Serial.available() > 0) {
    String jsonString = Serial.readStringUntil('\n');
    jsonString.trim();

    if (jsonString.length() > 0) {
      StaticJsonDocument<200> doc;
      DeserializationError error = deserializeJson(doc, jsonString);

      if (error) {
        Serial.print("Erro JSON: ");
        Serial.println(error.f_str());
        return;
      }

      // Lê o valor do JSON
      if (!doc["valor"].isNull()) {
        int valor = doc["valor"];

        // Só atualiza se for diferente do último recebido
        if (valor != ultimoValor) {
          ultimoValor = valor;
          Serial.print("Valor recebido: ");
          Serial.println(valor);

          if (valor == 1) {
            digitalWrite(pin1, HIGH);
            digitalWrite(pin2, LOW);
            Serial.println("Pin1 ON | Pin2 OFF");
          } 
          else if (valor == 2) {
            digitalWrite(pin1, LOW);
            digitalWrite(pin2, HIGH);
            Serial.println("Pin1 OFF | Pin2 ON");
          } 
          else {
            digitalWrite(pin1, LOW);
            digitalWrite(pin2, LOW);
            Serial.println("Pin1 OFF | Pin2 OFF");
          }
        }
      }
    }
  }
}

