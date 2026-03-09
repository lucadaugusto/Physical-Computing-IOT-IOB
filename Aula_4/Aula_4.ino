/* ==============================================================================
 * PROJETO: ALERTA DE SONOLÊNCIA (ESTILO HI-LO)
 * ==============================================================================
 * Descrição: Aciona um alarme de dois tons quando 
 * recebe o comando de sonolência do Python via JSON {"dir": "A"}.
 * * Hardware: 
 * - Buzzer: Pino 9
 * - LED Alerta: Pino 13 (ou externo)
 * ==============================================================================
 */

#include <ArduinoJson.h>

const int pinoBuzzer = 9;
const int pinoLED    = 13;

void setup() {
  Serial.begin(9600);
  
  pinMode(pinoBuzzer, OUTPUT);
  pinMode(pinoLED, OUTPUT);

  // Beep de inicialização
  tone(pinoBuzzer, 1000, 100);
  Serial.println("Sistema Pronto!");
}

void loop() {
  if (Serial.available() > 0) {
    String entrada = Serial.readStringUntil('\n');

    JsonDocument doc;
    DeserializationError erro = deserializeJson(doc, entrada);

    if (!erro) {
      const char* status = doc["dir"];

      // --- ALARME ---
      if (status[0] == 'A') {
        // Tom AGUDO (Hi)
        digitalWrite(pinoLED, HIGH);
        tone(pinoBuzzer, 880); 
        delay(300);

        // Tom GRAVE (Lo)
        digitalWrite(pinoLED, LOW);
        tone(pinoBuzzer, 698); 
        delay(300);
      } 
      else if (status[0] == 'N') {
        // Desliga tudo se estiver normal
        digitalWrite(pinoLED, LOW);
        noTone(pinoBuzzer);
      }
    }
  }
}
