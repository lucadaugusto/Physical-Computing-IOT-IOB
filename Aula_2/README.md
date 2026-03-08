# 🤏 Controle de Intensidade por Pinça (IA + Arduino)

Este projeto utiliza inteligência artificial para medir a distância entre os dedos e controlar o brilho de um LED (dimmer) via comunicação Serial.

## 🛠️ Pré-requisitos

### Python
Certifique-se de ter o Python 3.11 instalado. 

Instale as bibliotecas necessárias:
```bash
pip install opencv-python mediapipe pyserial
```

## 🚀 Funcionalidades
* Detecção de mão e cálculo de **distância** em tempo real.
* Controle de **intensidade (0% a 100%)** pela abertura da pinça.
* Saída de sinal **PWM** no Arduino para variação de brilho.
* Feedback visual no vídeo com linha guia entre o polegar e o indicador.

## 📂 Estrutura do Projeto
* `Aula_2.py`: Script Python (processamento da imagem e cálculo).
* `Aula_2.ino`: Código Arduino (recepção do dado e controle do LED).
* `hand_landmarker.task`: Arquivo de inteligência artificial (essencial na mesma pasta).

## 🔌 Como Configurar

### 1. Hardware
Conecte o LED a um pino **PWM** (marcado com `~`):
* **LED (Pólo Positivo):** Conectar ao pino digital escolhido **.

### 2. Software
1. Carregue o arquivo `Aula_2.ino` no seu Arduino.
2. No PyCharm, abra o arquivo `Aula_2.py`.
3. **Configuração da Porta Serial:**
    * **Com Arduino:** Altere `PORTA_ARDUINO` para a sua porta (ex: `'COM3'`).
    * **Sem Arduino (Teste):** Defina `PORTA_ARDUINO = None`.
4. Execute o script Python.

## 🎮 Como Operar
* **Unir dedos (Polegar e Indicador):** Apaga o LED (0%).
* **Afastar dedos:** Aumenta o brilho do LED até o máximo (100%).
* **Tecla 'q'**: Sai do programa com segurança.

---
**Nota:** Se o LED não apagar totalmente ou não atingir o brilho máximo, ajuste os valores de calibração `0.05` e `0.25` no código Python.
