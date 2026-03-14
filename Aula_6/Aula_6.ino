#include <SPI.h>
#include <MFRC522.h>

// Definicao dos pinos para o RC522
#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN); // Instancia o leitor

void setup() 
{
  Serial.begin(9600); // Velocidade deve ser a mesma do script Python
  SPI.begin();        // Inicia o barramento SPI
  rfid.PCD_Init();    // Inicia o leitor RFID
  
  // Mensagem inicial opcional (ajuda no debug)
  // Nota: O Python vai ignorar se o ID nao bater com o dicionario
  // Serial.println("Sistema Pronto"); 
}

void loop()
{
  // Verifica se ha um novo cartao presente
  if (!rfid.PICC_IsNewCardPresent()) 
  {
    return;
  }

  // Seleciona o cartao
  if (!rfid.PICC_ReadCardSerial()) {
    return;
  }

  // Variavel para armazenar o ID formatado
  String strID = "";

  // Converte os bytes do UID para uma String hexadecimal formatada
  for (byte i = 0; i < rfid.uid.size; i++) 
  {
    strID += String(rfid.uid.uidByte[i] < 0x10 ? "0" : "");
    strID += String(rfid.uid.uidByte[i], HEX);
    if (i < rfid.uid.size - 1) strID += " ";
  }

  strID.toUpperCase(); // Garante letras maiusculas

  // Envia o ID para o Python via Serial
  Serial.println(strID);

  // Pequeno atraso para evitar leituras duplicadas rapidas
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
  delay(1500);
}
