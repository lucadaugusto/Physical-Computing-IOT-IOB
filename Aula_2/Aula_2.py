# ==============================================================================
# 🤏 PROJETO: CONTROLE DE INTENSIDADE POR PINÇA (MediaPipe + Arduino)
# ==============================================================================
# Como usar:
# 1. Altere a PORTA_ARDUINO ou deixe None para testes.
# 2. Aproxime ou afaste o polegar do indicador para diminuir ou aumentar a intensidade.
# 3. AVariação de 0% a 100%.
# ==============================================================================

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import serial, time, json, math

# --- CONFIGURAÇÃO SIMPLES ---
PORTA_ARDUINO = 'COM9'  # Coloque a sua porta aqui ou None
arduino = None

if PORTA_ARDUINO:
    try:
        arduino = serial.Serial(PORTA_ARDUINO, 9600, timeout=1)
        time.sleep(2)
        print(f" Conectado na porta {PORTA_ARDUINO}")
    except:
        print(" Erro ao conectar no Arduino.")

# --- CONFIGURAÇÃO DA IA ---
model_path = 'hand_landmarker.task'
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

# Variáveis de controlo
ultimo_valor_enviado = -1

while cap := cv2.VideoCapture(0):
    if not cap.isOpened(): break

    while True:
        ret, frame = cap.read()
        if not ret: break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        resultado = detector.detect(mp_image)

        if resultado.hand_landmarks:
            for mao in resultado.hand_landmarks:
                # PONTOS: 4 (Polegar) e 8 (Indicador)
                p4 = mao[4]
                p8 = mao[8]

                # Cálculo da Distância Euclidiana
                distancia = math.sqrt((p8.x - p4.x) ** 2 + (p8.y - p4.y) ** 2)

                # MAPEAMENTO (Ajuste 0.05 e 0.25 conforme a distância da sua mão)
                intensidade = int((distancia - 0.05) * (100 / (0.25 - 0.05)))
                valor_atual = max(0, min(100, intensidade))  # Garante 0-100%

                # Desenho visual (Círculos nos dedos e linha entre eles)
                h, w, _ = frame.shape
                cx4, cy4 = int(p4.x * w), int(p4.y * h)
                cx8, cy8 = int(p8.x * w), int(p8.y * h)
                cv2.circle(frame, (cx4, cy4), 8, (255, 0, 0), -1)
                cv2.circle(frame, (cx8, cy8), 8, (255, 0, 0), -1)
                cv2.line(frame, (cx4, cy4), (cx8, cy8), (0, 255, 0), 2)

                cv2.putText(frame, f"Brilho: {valor_atual}%", (10, 50), 1, 2, (255, 255, 255), 2)

                # Enviar para Arduino apenas se mudar mais de 2% (evita ruído)
                if abs(valor_atual - ultimo_valor_enviado) > 2 and arduino:
                    pacote = json.dumps({"brilho": valor_atual}) + "\n"
                    arduino.write(pacote.encode())
                    ultimo_valor_enviado = valor_atual

        cv2.imshow("Controlo por Pinca", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    break

cap.release()
cv2.destroyAllWindows()
if arduino: arduino.close()
