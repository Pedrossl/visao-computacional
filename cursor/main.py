import cv2
import mediapipe as mp
import pyautogui

# Inicializando o MediaPipe Hands e Face Mesh
try:
    mp_hands = mp.solutions.hands
    mp_face_mesh = mp.solutions.face_mesh
    hands = mp_hands.Hands(max_num_hands=1)
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
    mp_drawing = mp.solutions.drawing_utils
    print("MediaPipe Hands e Face Mesh inicializados com sucesso.")
except Exception as e:
    print(f"Erro ao inicializar o MediaPipe Hands e Face Mesh: {e}")

# Captura de vídeo
cap = cv2.VideoCapture(0)