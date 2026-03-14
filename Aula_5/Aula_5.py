import cv2
import time
import json
import paho.mqtt.client as mqtt
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --- Configurações do MQTT ---
MQTT_BROKER = "IP Broker MQTT"
MQTT_PORT = 1883
MQTT_TOPIC = "user/experience/emotion"


# --- Configuração do Cliente MQTT ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao Broker MQTT com sucesso!")
    else:
        print(f"Falha na conexão: {rc}")


client = mqtt.Client(client_id="emotion_detector_tasks_1")
client.on_connect = on_connect
try:
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()
except Exception as e:
    print(f"Erro MQTT: {e}")

# --- Configuração do MediaPipe Tasks ---
# Certifique-se de que o arquivo 'face_landmarker.task' está no mesmo diretório
model_path = 'face_landmarker.task'

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=True,
    num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

# --- Configuração da Captura ---
cap = cv2.VideoCapture(0)
SMILE_THRESHOLD = 0.005
SAD_THRESHOLD = -0.004
last_emotion = "Neutral"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    # Converter BGR para RGB para o MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Detecção (Síncrona para simplificar o exemplo)
    detection_result = detector.detect(mp_image)

    current_emotion = "Neutral"

    if detection_result.face_landmarks:
        # No Tasks, os landmarks são acessados via lista de listas
        landmarks = detection_result.face_landmarks[0]

        # Índices permanecem os mesmos do Face Mesh original
        # 61, 291: Cantos da boca | 13, 14: Centro dos lábios
        corner_y = (landmarks[61].y + landmarks[291].y) / 2
        lip_center_y = (landmarks[13].y + landmarks[14].y) / 2

        smile_value = lip_center_y - corner_y

        if smile_value > SMILE_THRESHOLD:
            current_emotion = "Happy"
        elif smile_value < SAD_THRESHOLD:
            current_emotion = "Sad"

        # Lógica de publicação MQTT
        if current_emotion != last_emotion:
            last_emotion = current_emotion
            payload = {"timestamp": time.time(), "emotion": last_emotion}
            if client.is_connected():
                client.publish(MQTT_TOPIC, json.dumps(payload))
                print(f"Enviado: {last_emotion}")

    # --- UI ---
    color = (0, 255, 255)  # Amarelo (Neutral)
    if last_emotion == "Happy": color = (0, 255, 0)
    if last_emotion == "Sad": color = (0, 0, 255)

    cv2.putText(frame, f"Emocao: {last_emotion}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow('MediaPipe Tasks - Emotion', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
client.loop_stop()
