# ==============================================================================
# PROJETO: MONITOR DE POSE FACIAL (IA + ARDUINO)
# ==============================================================================
# Descrição: Detecta a direção do olhar (Esquerda, Direita, Frente) usando 
# FaceMesh e envia comandos JSON via Serial para o Arduino.
#
# Componentes: Webcam + Arduino (Opcional)
# Bibliotecas: OpenCV, MediaPipe, PySerial
# ==============================================================================

import cv2
import mediapipe as mp
import serial
import time
import json
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --- CONFIGURAÇÃO DE HARDWARE ---
PORTA_ARDUINO = None  # Altere para 'COM3', 'COM10', etc., ou None para teste
BAUD_RATE = 9600
arduino = None

# Inicia a conexão Serial se uma porta for definida
if PORTA_ARDUINO:
    try:
        arduino = serial.Serial(PORTA_ARDUINO, BAUD_RATE, timeout=1)
        time.sleep(2)  # Aguarda o boot do Arduino
        print(f" Conectado ao Arduino na porta {PORTA_ARDUINO}")
    except Exception as e:
        print(f" Erro ao conectar: {e}. Rodando em modo simulação.")
else:
    print(" Modo Simulação: Nenhuma porta serial definida.")

# --- CONFIGURAÇÃO DA IA (FACE MESH) ---
MODEL_PATH = 'face_landmarker.task'
THRESHOLD = 0.03  # Sensibilidade do movimento (ajuste conforme necessário)

# Tenta carregar as conexões da malha facial (compatível com venv)
try:
    import mediapipe.python.solutions.face_mesh_connections as fmc

    CONEXOES_MALHA = fmc.FACEMESH_TESSELATION
except:
    try:
        from mediapipe.python.solutions import face_mesh as mp_face_mesh

        CONEXOES_MALHA = mp_face_mesh.FACEMESH_TESSELATION
    except:
        print(" Não foi possível carregar os traços da malha.")
        CONEXOES_MALHA = []

# Inicializa o Detector de Face
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.FaceLandmarkerOptions(base_options=base_options, num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

# --- LOOP PRINCIPAL ---
cap = cv2.VideoCapture(0)
ultimo_comando = ""

print(" Iniciando detecção... Pressione 'q' para sair.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)  # Espelhar para visualização natural
    h, w, _ = frame.shape

    # Processamento da imagem
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    resultado = detector.detect(mp_image)

    if resultado.face_landmarks:
        for face in resultado.face_landmarks:

            # 1. DESENHAR MALHA FACIAL (Traços e Pontos em AZUL)
            # Desenha as linhas de conexão
            if CONEXOES_MALHA:
                for connection in CONEXOES_MALHA:
                    p1, p2 = face[connection[0]], face[connection[1]]
                    pt1 = (int(p1.x * w), int(p1.y * h))
                    pt2 = (int(p2.x * w), int(p2.y * h))
                    cv2.line(frame, pt1, pt2, (255, 0, 0), 1)  # Azul (BGR)

            # Desenha os pontos (Landmarks)
            for landmark in face:
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 1, (255, 0, 0), -1)

            # 2. LÓGICA DE DIREÇÃO (Pontos: 1-Nariz, 33-Olho Esq, 263-Olho Dir)
            nariz = face[1]
            centro_olhos_x = (face[33].x + face[263].x) / 2.0
            diff = nariz.x - centro_olhos_x

            if diff < -THRESHOLD:
                direcao, cmd = "ESQUERDA", "L"
            elif diff > THRESHOLD:
                direcao, cmd = "DIREITA", "R"
            else:
                direcao, cmd = "FRENTE", "F"

            # 3. ENVIO SERIAL JSON
            if cmd != ultimo_comando:
                pacote_dict = {"dir": cmd}
                pacote_json = json.dumps(pacote_dict) + "\n"

                if arduino and arduino.is_open:
                    arduino.write(pacote_json.encode())
                    print(f" Enviado: {pacote_json.strip()}")
                else:
                    print(f" Simulação: {direcao} ({cmd})")

                ultimo_comando = cmd

            # Exibe o status na tela
            cv2.putText(frame, f"Olhar: {direcao}", (10, 40), 1, 2, (0, 255, 255), 2)

    cv2.imshow("Monitoramento de Pose Facial", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- FINALIZAÇÃO ---
cap.release()
if arduino: arduino.close()
cv2.destroyAllWindows()
print(" Programa encerrado.")
