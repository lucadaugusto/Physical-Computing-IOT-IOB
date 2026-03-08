# ==============================================================================
# PROJETO: CONTADOR DE DEDOS (MediaPipe + Arduino)
# ==============================================================================
# Como usar: 
# 1. Altere a PORTA_ARDUINO para a sua (ex: 'COM3') ou deixe None para teste.
# 2. Pressione 'q' para sair.
# ==============================================================================

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import serial
import time
import json

# ==============================================================================
# 1. Configuração da Comunicação Serial (Arduino)
# ==============================================================================
# Para testar SEM o Arduino, deixe a variável como: None
# Para testar COM o Arduino, coloque a porta entre aspas. Exemplo: 'COM9'
PORTA_ARDUINO = None

arduino = None # Começamos assumindo que não há Arduino

if PORTA_ARDUINO: # Se o aluno digitou alguma porta, tenta conectar
    try:
        arduino = serial.Serial(PORTA_ARDUINO, 9600, timeout=1)
        time.sleep(2)
        print("Arduino conectado na porta:", PORTA_ARDUINO)
    except:
        print("Erro: Arduino não encontrado na porta", PORTA_ARDUINO)
else:
    print("Modo de teste: Vídeo rodando sem o Arduino.")

# ==============================================================================
# 2. Configuração do MediaPipe Tasks API
# ==============================================================================
model_path = 'hand_landmarker.task'

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)
detector = vision.HandLandmarker.create_from_options(options)

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),  # Polegar
    (0, 5), (5, 6), (6, 7), (7, 8),  # Indicador
    (5, 9), (9, 10), (10, 11), (11, 12),  # Médio
    (9, 13), (13, 14), (14, 15), (15, 16),  # Anelar
    (13, 17), (17, 18), (18, 19), (19, 20),  # Mínimo
    (0, 17)  # Fecha a base da palma da mão
]


# ==============================================================================
# 3. Funções Auxiliares
# ==============================================================================
def count_fingers(hand_landmarks):
    """Conta os dedos indicadores, médio, anelar e mínimo."""
    count = 0
    if hand_landmarks[8].y < hand_landmarks[6].y:
        count += 1
    if hand_landmarks[12].y < hand_landmarks[10].y:
        count += 1
    if hand_landmarks[16].y < hand_landmarks[14].y:
        count += 1
    if hand_landmarks[20].y < hand_landmarks[18].y:
        count += 1
    return count


def desenhar_maos_na_tela(frame, hand_landmarks, connections):
    """Desenha os pontos e linhas no vídeo."""
    h, w, _ = frame.shape
    for connection in connections:
        ponto_inicial = connection[0]
        ponto_final = connection[1]
        x1 = int(hand_landmarks[ponto_inicial].x * w)
        y1 = int(hand_landmarks[ponto_inicial].y * h)
        x2 = int(hand_landmarks[ponto_final].x * w)
        y2 = int(hand_landmarks[ponto_final].y * h)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    for landmark in hand_landmarks:
        cx = int(landmark.x * w)
        cy = int(landmark.y * h)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), cv2.FILLED)


# ==============================================================================
# 4. Loop Principal (Webcam)
# ==============================================================================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Variável para memorizar o último valor que enviámos ao Arduino
ultimo_valor_enviado = -1

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame da webcam.")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    detection_result = detector.detect(mp_image)

    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:

            finger_count = count_fingers(hand_landmarks)
            desenhar_maos_na_tela(frame, hand_landmarks, HAND_CONNECTIONS)

            cv2.putText(frame, f"Fingers: {finger_count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # --- NOVA LÓGICA DE ENVIO ---
            # Determina o valor atual (1, 2 ou 0)
            if finger_count == 1:
                valor_atual = 1
            elif finger_count == 2:
                valor_atual = 2
            else:
                valor_atual = 0

            # Só envia para o Arduino SE o valor mudou desde a última vez
            if valor_atual != ultimo_valor_enviado:
                if arduino and arduino.is_open:
                    data = {"valor": valor_atual}
                    pacote = json.dumps(data) + "\n"
                    arduino.write(pacote.encode('utf-8'))
                    print("Enviado:", pacote.strip())

                    # Atualiza a memória com o novo valor
                    ultimo_valor_enviado = valor_atual

    cv2.imshow("Webcam - Finger Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
