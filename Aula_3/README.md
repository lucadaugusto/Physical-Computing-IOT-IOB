# 👤 Monitor de Pose Facial (IA + Arduino)

Este projeto utiliza inteligência artificial para detectar a direção do olhar (**Esquerda, Direita ou Frente**) através do mapeamento de pontos da face (Face Mesh) e envia comandos via Serial para o Arduino.

## 🛠️ Pré-requisitos

### Python
Certifique-se de ter o Python 3.11 instalado. 

Instale as bibliotecas necessárias:
```bash
pip install opencv-python mediapipe pyserial
```

## 🚀 Funcionalidades
* **Detecção Facial:** Mapeamento de 468 pontos da face em tempo real.
* **Interface Visual:** Máscara tecnológica com pontos e traços em azul.
* **Comunicação JSON:** Envio de comandos estruturados para o Arduino (`{"dir": "L"}`).
* **Modo Simulação:** Funciona com ou sem o Arduino conectado (Porta `None`).

## 📂 Estrutura do Projeto
* `Aula_3.py`: Script Python (Processamento de imagem e lógica de direção).
* `Aula_3.ino`: Código Arduino (Recepção do JSON e acionamento dos LEDs).
* `face_landmarker.task`: Modelo de IA do MediaPipe (deve estar na mesma pasta).

## 🔌 Como Configurar

### 1. Hardware
Conecte três LEDs para indicar as direções nos pinos digitais:
* **LED Esquerda:** Pino Digital **6**.
* **LED Frente:** Pino Digital **7**.
* **LED Direita:** Pino Digital **8**.

### 2. Software
1. **Arduino:** Carregue o arquivo `Aula_3.ino` no seu microcontrolador através da Arduino IDE.
2. **Ambiente Python:** Certifique-se de estar com o seu ambiente virtual (`venv`) ativo.
3. **Configuração da Porta:**
    * **Com Arduino:** No arquivo `Aula_3.py`, altere `PORTA_ARDUINO = 'COMx'` (verifique qual porta aparece no Gerenciador de Dispositivos ou na IDE do Arduino).
    * **Sem Arduino:** Mantenha `PORTA_ARDUINO = None`.

## 🎮 Como Operar
* **Olhar para a Esquerda:** Acende o LED da esquerda (Comando `L`).
* **Olhar para a Direita:** Acende o LED da direita (Comando `R`).
* **Olhar para Frente:** Acende o LED central (Comando `F`).
* **Tecla 'q'**: Encerra o programa e fecha a conexão com segurança.

---

### 🔍 Dica (Calibração)
Se a detecção estiver oscilando muito entre os estados, oriente os alunos a ajustarem a variável `THRESHOLD` no código Python:
* **Aumentar (ex: 0.05):** Exige um movimento de cabeça mais acentuado para mudar o LED (mais estabilidade).
* **Diminuir (ex: 0.02):** Torna o sistema extremamente sensível a pequenos movimentos.

---
**Nota:** Certifique-se de que o arquivo `face_landmarker.task` está no mesmo diretório dos scripts para que a IA funcione corretamente.
