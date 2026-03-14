#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// --- Configurações de Rede ---
const char* ssid = "NOME_DO_SEU_WIFI";
const char* password = "SENHA_DO_SEU_WIFI";

// --- Configurações MQTT ---
const char* mqtt_server = "IP_DO_SEU_BROKER"; 
const char* mqtt_topic = "user/experience/emotion";

// --- Definição dos Pinos dos LEDs ---
#define LED_VERDE    12 // Happy
#define LED_AMARELO  14 // Neutral
#define LED_VERMELHO 27 // Sad

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() 
{
  delay(10);
  Serial.println();
  Serial.print("Conectando em ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado!");
}

// Função que apaga todos os LEDs
void apagarLEDs() 
{
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_AMARELO, LOW);
  digitalWrite(LED_VERMELHO, LOW);
}

// Callback executado quando uma mensagem chega via MQTT
void callback(char* topic, byte* payload, unsigned int length) 
{
  Serial.print("Mensagem recebida no tópico [");
  Serial.print(topic);
  Serial.print("] ");

  // Converter o payload para String para processar o JSON
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  // Decodificar o JSON
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, message);

  if (error) {
    Serial.print("Falha no parse do JSON: ");
    Serial.println(error.f_str());
    return;
  }

  const char* emotion = doc["emotion"];
  Serial.print("Sentimento detectado: ");
  Serial.println(emotion);

  apagarLEDs();

  // Lógica dos LEDs e Mensagens
  if (strcmp(emotion, "Happy") == 0) {
    digitalWrite(LED_VERDE, HIGH);
    Serial.println(">>> LED VERDE ACESO (FELIZ)");
  } 
  else if (strcmp(emotion, "Neutral") == 0) {
    digitalWrite(LED_AMARELO, HIGH);
    Serial.println(">>> LED AMARELO ACESO (NEUTRO)");
  } 
  else if (strcmp(emotion, "Sad") == 0) {
    digitalWrite(LED_VERMELHO, HIGH);
    Serial.println(">>> LED VERMELHO ACESO (TRISTE)");
  }
}

void reconnect() 
{
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    // ID do cliente aleatório para evitar conflitos
    if (client.connect("ESP32_Emotion_Receiver")) {
      Serial.println("conectado!");
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

void setup() 
{
  Serial.begin(115200);
  
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARELO, OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);
  
  apagarLEDs();
  setup_wifi();
  
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() 
{
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
