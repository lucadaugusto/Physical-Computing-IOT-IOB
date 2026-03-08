/* * ==============================================================================
 * PROJETO: RECEPTOR DE GESTOS (Arduino + JSON)
 * ==============================================================================
 * HARDWARE: 
 * - LED 1: Pino Digital 6
 * - LED 2: Pino Digital 7 (e assim por diante)
 * * BIBLIOTECA: Instalar a "ArduinoJson" no Library Manager.
 * ==============================================================================
 */

// Inclui a biblioteca para ler o formato JSON
#include <ArduinoJson.h>

// ==============================================================================
// 1. Configuração dos Pinos
// ==============================================================================
// Vamos ligar os LEDs aos pinos digitais 6 e 7 do Arduino
const int pinoLED1 = 6; 
const int pinoLED2 = 7; 

void setup() {
  // Inicia a comunicação serial com a mesma velocidade do Python (9600)
  Serial.begin(9600);
  
  // Configura os pinos dos LEDs como SAÍDA de energia
  pinMode(pinoLED1, OUTPUT);
  pinMode(pinoLED2, OUTPUT);
  
  // Garante que os LEDs começam apagados
  digitalWrite(pinoLED1, LOW);
  digitalWrite(pinoLED2, LOW);
}

void loop() {
  // ==============================================================================
  // 2. Leitura da Comunicação Serial
  // ==============================================================================
  // Verifica se existe alguma mensagem na "caixa de correio" (Serial)
  if (Serial.available() > 0) {
    
    // Lê a mensagem toda até encontrar a quebra de linha ('\n')
    String pacoteTexto = Serial.readStringUntil('\n');
    
    // ==============================================================================
    // 3. Processamento do JSON
    // ==============================================================================
    // Cria um documento JSON (usando a sintaxe do ArduinoJson 7)
    JsonDocument doc;
    
    // Tenta converter o texto recebido para o formato JSON
    DeserializationError erro = deserializeJson(doc, pacoteTexto);
    
    // Se não houver erro na leitura do JSON, prosseguimos
    if (!erro) {
      // Extrai o número que está dentro da chave "valor"
      int quantidadeDedos = doc["valor"];
      
      // ==============================================================================
      // 4. Lógica de Acender/Apagar LEDs
      // ==============================================================================
      // Primeiro, apagamos todos os LEDs para garantir um estado limpo
      digitalWrite(pinoLED1, LOW);
      digitalWrite(pinoLED2, LOW);
      
      // Acende os LEDs com base na quantidade de dedos
      if (quantidadeDedos == 1) {
        // Se for 1 dedo, acende apenas o primeiro LED
        digitalWrite(pinoLED1, HIGH);
        
      } else if (quantidadeDedos == 2) {
        // Se forem 2 dedos, acende os dois LEDs
        digitalWrite(pinoLED1, HIGH);
        digitalWrite(pinoLED2, HIGH);
      }
      // Se for 0, os LEDs simplesmente continuam apagados
    }
  }
}
