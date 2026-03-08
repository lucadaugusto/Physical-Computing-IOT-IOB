# ==============================================================================
# AULA: DETECTOR DE SONOLÊNCIA (MediaPipe Tasks)
# ==============================================================================
# Descrição: Calcula o EAR (Eye Aspect Ratio) para detectar olhos fechados.
# Envia comandos JSON via Serial para o Arduino.
# ==============================================================================

import cv2
import mediapipe as mp
import serial, time, json, os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --- CONFIGURAÇÃO DE HARDWARE ---
PORTA_ARDUINO = None  # Altere para 'COM8' ou similar se usar o Arduino
arduino = None

if PORTA_ARDUINO:
    try:
        arduino = serial.Serial(PORTA_ARDUINO, 9600, timeout=1)
        time.sleep(2)
        print(f"Conectado ao Arduino na porta {PORTA_ARDUINO}")
    except:
        print("Arduino não encontrado. Modo Simulação.")

# --- CONFIGURAÇÃO DA IA (TASKS API) ---
MODEL_PATH = 'face_landmarker.task'
EYE_AR_THRESH = 0.25  # Limiar de olhos fechados
EYE_AR_CONSEC_FRAMES = 15  # Frames necessários para alarme
COUNTER = 0
ALARM_ON = False

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.FaceLandmarkerOptions(base_options=base_options, num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)


# --- FUNÇÕES AUXILIARES ---
def calculate_ear(eye_landmarks):
    # Distâncias verticais
    v1 = abs(eye_landmarks[1].y - eye_landmarks[5].y)
    v2 = abs(eye_landmarks[2].y - eye_landmarks[4].y)
    # Distância horizontal
    h = abs(eye_landmarks[0].x - eye_landmarks[3].x)

    if h == 0: return 0.0
    return (v1 + v2) / (2.0 * h)


# --- LOOP PRINCIPAL ---
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    resultado = detector.detect(mp_image)

    if resultado.face_landmarks:
        for face in resultado.face_landmarks:
            # Índices MediaPipe para EAR (Canto ext, topo1, topo2, canto int, baixo1, baixo2)
            # Olho Direito: [33, 160, 158, 133, 153, 144]
            # Olho Esquerdo: [362, 385, 387, 263, 373, 380]
            right_eye_indices = [33, 160, 158, 133, 153, 144]
            left_eye_indices = [362, 385, 387, 263, 373, 380]

            right_eye_lm = [face[i] for i in right_eye_indices]
            left_eye_lm = [face[i] for i in left_eye_indices]

            ear_right = calculate_ear(right_eye_lm)
            ear_left = calculate_ear(left_eye_lm)
            avg_ear = (ear_left + ear_right) / 2.0

            # --- DESENHO DOS OLHOS (AZUL) ---
            for index in right_eye_indices + left_eye_indices:
                pt = face[index]
                cv2.circle(frame, (int(pt.x * w), int(pt.y * h)), 2, (255, 0, 0), -1)

            # --- LÓGICA DE ALARME ---
            if avg_ear < EYE_AR_THRESH:
                COUNTER += 1
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    if not ALARM_ON:
                        ALARM_ON = True
                        if arduino:
                            arduino.write(json.dumps({"dir": "A"}).encode() + b'\n')

                    cv2.putText(frame, "ALERTA DE SONOLENCIA!", (w // 4, h // 2),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            else:
                COUNTER = 0
                if ALARM_ON:
                    ALARM_ON = False
                    if arduino:
                        arduino.write(json.dumps({"dir": "N"}).encode() + b'\n')

            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (10, 30), 1, 1.5, (255, 0, 0), 2)

    cv2.imshow("Detector de Sonolencia (Tasks)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
if arduino: arduino.close()
cv2.destroyAllWindows()
