
# Hand and Face Tracking with Mouse Control

Este projeto utiliza as bibliotecas OpenCV, MediaPipe e PyAutoGUI para rastrear a posição das mãos e da cabeça utilizando a webcam. Com base no movimento da mão e da cabeça, o cursor do mouse é movido e cliques são realizados.

## Pré-requisitos

Certifique-se de ter Python 3.x instalado. As seguintes bibliotecas Python são necessárias:

- OpenCV
- MediaPipe
- PyAutoGUI

Você pode instalar essas dependências usando:

```bash
pip install opencv-python mediapipe pyautogui
```

## Como Executar

1. Clone o repositório ou copie o código para um arquivo local.
2. Execute o script Python.

```bash
python main.py
```

## Explicação do Código

### Inicialização

O código começa importando as bibliotecas necessárias e inicializando as soluções MediaPipe para detecção de mãos e Face Mesh para rastreamento facial.

```python
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
```

### Captura de Vídeo

Captura o vídeo da webcam.

```python
cap = cv2.VideoCapture(0)
```

### Processamento de Frames

Processa cada frame do vídeo para detectar mãos e rosto, e utiliza as landmarks detectadas para mover o cursor do mouse e realizar cliques com base no movimento da cabeça.

```python
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convertendo a imagem para RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Processando a imagem para detectar as mãos e o rosto
    hand_results = hands.process(image)
    face_results = face_mesh.process(image)
    
    # Convertendo a imagem de volta para BGR para exibição
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Detectando e desenhando landmarks da mão
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Pegando a posição do ponto 8 (ponta do dedo indicador)
            x = hand_landmarks.landmark[8].x
            y = hand_landmarks.landmark[8].y
            # Convertendo a posição normalizada para coordenadas de tela
            screen_width, screen_height = pyautogui.size()
            x = int(x * screen_width)
            y = int(y * screen_height)
            # Movendo o cursor do mouse
            pyautogui.moveTo(x, y)
    
    # Detectando e desenhando landmarks do rosto
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            mp_drawing.draw_landmarks(image, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)
            nose_tip = face_landmarks.landmark[1]  # Landmark 1 é a ponta do nariz
            nose_x = nose_tip.x
            
            # Inicializando a posição inicial do nariz
            if initial_nose_x is None:
                initial_nose_x = nose_x
            
            # Detectando movimento da cabeça
            x_diff = nose_x - initial_nose_x
            
            # Movendo a cabeça para esquerda para clique esquerdo
            if x_diff < -0.05:
                pyautogui.click(button='left')
                initial_nose_x = nose_x  # Reset posição inicial para evitar cliques repetidos
            
            # Movendo a cabeça para direita para clique direito
            if x_diff > 0.05:
                pyautogui.click(button='right')
                initial_nose_x = nose_x  # Reset posição inicial para evitar cliques repetidos
    
    # Mostrando a imagem com as landmarks
    cv2.imshow('Hand and Face Tracking', image)
    
    # Saindo do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberando a captura e destruindo todas as janelas
cap.release()
cv2.destroyAllWindows()
```

### Video usando o sistema
https://www.youtube.com/watch?v=mB_5HASX5zQ

### Nota

A sensibilidade do movimento da cabeça pode ser ajustada alterando os valores de `x_diff`.
