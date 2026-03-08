/* * ==============================================================================
 * PROJETO: DIMMER POR GESTO DE PINÇA
 * ==============================================================================
 * Descrição: Recebe um valor JSON {"brilho": X} e ajusta a intensidade do LED.
 * Hardware: Conecte o LED no Pino 3 (ou qualquer pino com o símbolo ~).
 * ==============================================================================
 */

#include <ArduinoJson.h>

// O pino deve ser PWM (3, 5, 6, 9, 10 ou 11 no Arduino Uno)
const int pinoLED = 3; 

void setup() {
  // Inicia a serial na mesma velocidade do Python
  Serial.begin(9600);
  
  // Configura o pino do LED como saída
  pinMode(pinoLED, OUTPUT);
  
  // Inicia com o LED apagado
  analogWrite(pinoLED, 0);
}

void loop() {
  // Verifica se chegaram dados na porta serial
  if (Serial.available() > 0) {
    
    // Lê a linha enviada pelo Python
    String json = Serial.readStringUntil('\n');
    
    // Cria o documento para traduzir o JSON
    JsonDocument doc;
    DeserializationError erro = deserializeJson(doc, json);

    // Se a leitura do JSON deu certo...
    if (!erro) {
      // Pega o valor de 0 a 100 que o Python calculou
      int brilhoPorcento = doc["brilho"]; 
      
      // Converte a escala:
      // 0%   -> 0   (totalmente apagado)
      // 100% -> 255 (brilho máximo)
      int valorPWM = map(brilhoPorcento, 0, 100, 0, 255);
      
      // Aplica a intensidade no pino do LED
      analogWrite(pinoLED, valorPWM);
    }
  }
}
