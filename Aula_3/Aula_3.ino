/* ==============================================================================
 * PROJETO: RECEPTOR DE POSE FACIAL (ARDUINO)
 * ==============================================================================
 * Descrição: Recebe comandos JSON via Serial e aciona LEDs conforme a 
 * direção do olhar detectada pela IA (Esquerda, Direita, Frente).
 * * Hardware: 
 * - LED Esquerda: Pino 6
 * - LED Frente:   Pino 7
 * - LED Direita:  Pino 8
 * ==============================================================================
 */

#include <ArduinoJson.h>

// Definição dos pinos dos LEDs
const int pinoEsq     = 6;
const int pinoFrente  = 7;
const int pinoDir     = 8;

void setup() {
  // Inicia a comunicação Serial (mesmo Baud Rate do Python)
  Serial.begin(9600);

  // Configura os pinos como saída
  pinMode(pinoEsq, OUTPUT);
  pinMode(pinoFrente, OUTPUT);
  pinMode(pinoDir, OUTPUT);

  // Teste inicial: Pisca todos os LEDs ao ligar
  digitalWrite(pinoEsq, HIGH);
  digitalWrite(pinoFrente, HIGH);
  digitalWrite(pinoDir, HIGH);
  delay(500);
  digitalWrite(pinoEsq, LOW);
  digitalWrite(pinoFrente, LOW);
  digitalWrite(pinoDir, LOW);

  Serial.println("Arduino pronto para receber comandos!");
}

void loop() {
  // Verifica se há dados chegando na porta Serial
  if (Serial.available() > 0) {
    
    // Lê a mensagem até encontrar a quebra de linha (\n)
    String entrada = Serial.readStringUntil('\n');

    // Cria o documento JSON (estático para economizar memória)
    JsonDocument doc;
    DeserializationError erro = deserializeJson(doc, entrada);

    // Se a tradução do JSON deu certo...
    if (!erro) {
      // Extrai o caractere da direção: 'L', 'R' ou 'F'
      const char* direcao = doc["dir"];

      // Apaga todos os LEDs antes de ligar o novo (reset visual)
      digitalWrite(pinoEsq, LOW);
      digitalWrite(pinoFrente, LOW);
      digitalWrite(pinoDir, LOW);

      // Lógica de acionamento baseada no comando
      if (direcao[0] == 'L') {
        digitalWrite(pinoEsq, HIGH);
        Serial.println("Movimento: Esquerda");
      } 
      else if (direcao[0] == 'R') {
        digitalWrite(pinoDir, HIGH);
        Serial.println("Movimento: Direita");
      } 
      else if (direcao[0] == 'F') {
        digitalWrite(pinoFrente, HIGH);
        Serial.println("Movimento: Frente");
      }
    }
  }
}
