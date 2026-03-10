// --- Configurações ---
// LED_BUILTIN já é uma constante padrão do Arduino (geralmente pino 13 no Arduino Uno)
const int LED_PIN = LED_BUILTIN; 

void setup() 
{
  // Inicia a comunicação serial na mesma velocidade definida no Python (9600)
  Serial.begin(9600);
  
  // Configura o pino do LED como saída
  pinMode(LED_PIN, OUTPUT);
  
  // Opcional: Avisar ao Python que o Arduino está pronto
  Serial.println("Arduino Pronto!");
}

void loop() 
{
  // Verifica se há dados chegando na porta serial
  if (Serial.available() > 0) {
    
    // Lê o caractere recebido
    char comando = Serial.read();
    
    // Lógica de Processamento dos Comandos
    switch (comando) {
      case 'L':
        digitalWrite(LED_PIN, HIGH);
        Serial.println("LED Ligado");
        break;
        
      case 'D':
        digitalWrite(LED_PIN, LOW);
        Serial.println("LED Desligado");
        break;
        
      // Ignora caracteres invisíveis como \n (New Line) ou \r (Carriage Return)
      case '\n':
      case '\r':
        break;

      default:
        Serial.print("Comando desconhecido: ");
        Serial.println(comando);
        break;
    }
  }
}
