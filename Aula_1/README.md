# 🖐️ Contador de Dedos com IA e Arduino

Este projeto faz parte da **Aula 1** de Computação Física e IoT. Utilizamos a biblioteca **MediaPipe** para reconhecer gestos manuais via webcam e enviar os comandos para um **Arduino** controlar LEDs via comunicação Serial.

## 🚀 Funcionalidades
* Detecção de mão em tempo real.
* Contagem de dedos (0 a 4).
* Envio de dados formatados em **JSON** para o Arduino.
* Interface visual com marcações das articulações da mão.

## 🛠️ Pré-requisitos

### Python
Certifique-se de ter o Python 3.11 instalado. 

Instale as bibliotecas necessárias:
```bash
pip install opencv-python mediapipe pyserial
```

### Arduino

   Instale a biblioteca ArduinoJson (v7.x) através do Gestor de Bibliotecas da IDE do Arduino.

## 📂 Estrutura do Repositório

  Aula_1.py: Script principal em Python (Cérebro do projeto).

  Aula_1.ino: Código C++ para o Arduino (Atuador).

  hand_landmarker.task: Modelo de IA do MediaPipe (Deve estar na mesma pasta do script).

##🔌 Como Configurar
1. Hardware

Ligue os LEDs aos pinos digitais do Arduino conforme a tabela:
*Dedo 1: Pino 6
*Dedo 2: Pino 7

2. Software
*Carregue o arquivo Aula_1.ino no seu Arduino usando a IDE do Arduino.
*No PyCharm, abra o Aula_1.py.
  Nota importante sobre a conexão:
*Com Arduino: No arquivo Aula_1.py, altere a variável PORTA_ARDUINO para a porta onde sua placa está conectada (ex: 'COM3' ou 'COM9').
*Sem Arduino (Teste): Caso queira testar apenas a detecção da câmera, defina PORTA_ARDUINO = None.

    Execute o script Python.

## 🎮 Controles

  Tecla 'q': Encerra o programa e fecha a conexão serial com segurança.
