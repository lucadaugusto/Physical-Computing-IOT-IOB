# 😴 Detector de Sonolência (VC + IA + Arduino)

Este projeto utiliza visão computacional e IA para monitorar o nível de abertura dos olhos (**Eye Aspect Ratio - EAR**) em tempo real. Caso o sistema detecte que o usuário está com os olhos fechados por muito tempo, um alarme é disparado no Arduino.

## 🛠️ Pré-requisitos

### Python
Certifique-se de ter o Python 3.11 instalado. 

Instale as bibliotecas necessárias:
```bash
pip install opencv-python mediapipe pyserial
```

## 🚀 Funcionalidades
* **Cálculo de EAR:** Monitoramento da abertura ocular para detectar fadiga.
* **Alarme:** Alerta sonoro de dois tons para despertar o condutor.
* **Comunicação JSON:** Envio de status de segurança (`{"dir": "A"}` para Alarme e `{"dir": "N"}` para Normal).
* **Interface Visual:** Destaque dos pontos dos olhos em azul na tela.

## 📂 Estrutura do Projeto
* `Aula_4.py`: Script Python (Cálculo do EAR e lógica de tempo de fechamento).
* `Aula_4.ino`: Código Arduino (Recepção do JSON e controle do Buzzer Hi-Lo).
* `face_landmarker.task`: Modelo de IA do MediaPipe (deve estar na mesma pasta).

## 🔌 Como Configurar

### 1. Hardware
Conecte os componentes de alerta nos pinos digitais:
* **Buzzer (Positivo):** Pino Digital **9**.
* **LED Alerta (Opcional):** Pino Digital **13** (ou LED interno da placa).

### 2. Software
1. **Arduino:** Carregue o arquivo `Aula_4.ino` através da Arduino IDE.
2. **Ambiente Python:** Certifique-se de estar com o seu ambiente virtual (`venv`) ativo.
3. **Configuração da Porta:**
    * **Com Arduino:** No arquivo `Aula_4.py`, altere `PORTA_ARDUINO = 'COMx'`.
    * **Sem Arduino:** Mantenha `PORTA_ARDUINO = None`.

## 🎮 Como Operar
* **Olhos Abertos:** O sistema exibe o valor do EAR em azul. O LED e Buzzer ficam desligados.
* **Olhos Fechados:** Se permanecerem fechados por mais de **15 frames**, o Arduino inicia o toque e exibe "ALERTA" na tela.
* **Tecla 'q'**: Encerra o programa com segurança.

---

### 🔍 Dica (Calibração de Segurança)
Cada pessoa possui uma abertura de olho diferente. Oriente os alunos a ajustarem:
* **EYE_AR_THRESH (ex: 0.25):** Se o alarme tocar com o olho aberto, diminua este valor. Se não tocar com o olho fechado, aumente.
* **EYE_AR_CONSEC_FRAMES (ex: 15):** Aumente para tornar o alarme menos "sensível" a piscadas rápidas.

---
**Nota:** O arquivo `face_landmarker.task` é indispensável para que o Python consiga mapear os olhos corretamente.
