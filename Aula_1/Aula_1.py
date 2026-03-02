# Aula sobre identificação de gestos usando o MediaPipe para contar dedos e enviar os dados para um Arduino via comunicação serial. 
# O código captura o vídeo da webcam, processa as mãos para contar os dedos indicadores, médio, anelar e mínimo, e envia essa contagem para o Arduino em formato JSON. 
# O programa exibe a contagem de dedos na tela e pode ser encerrado pressionando a tecla 'q'.

import cv2
import mediapipe as mp
import serial
import time
import json

# Configurar a porta serial (ajuste para a porta correta do seu Arduino)
arduino = serial.Serial('COM9', 9600, timeout=1)
time.sleep(2)  # Aguarda a inicialização da conexão serial

# Inicializa o MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

def count_fingers(hand_landmarks):
    """Conta apenas dedos indicadores, médio, anelar e mínimo"""
    count = 0
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
        count += 1
    if hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y:
        count += 1
    if hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y:
        count += 1
    if hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y:
        count += 1
    return count

# Webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame da webcam.")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            finger_count = count_fingers(hand_landmarks)
            cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Só envia 1, 2 ou 0
            if finger_count == 1:
                data = {"valor": 1}
            elif finger_count == 2:
                data = {"valor": 2}
            else:
                data = {"valor": 0}
            
            pacote = json.dumps(data) + "\n"
            arduino.write(pacote.encode('utf-8'))
            print("Enviado:", pacote.strip())
            time.sleep(0.05)  # pequeno delay para não sobrecarregar

    cv2.imshow("Webcam - Finger Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
