import cv2
import pickle 
import numpy as np

# Carregar as vagas
with open('vagas.pkl', 'rb') as arquivo:
    vagas = pickle.load(arquivo)

# Carregar o vídeo e redimensioná-lo para 1473x828
video = cv2.VideoCapture('video.mp4')

while True:
    check, img = video.read()

    # Redimensionar o frame do vídeo para o mesmo tamanho da imagem de seleção
    if img is not None:
        img = cv2.resize(img, (1473, 828))  # Redimensionar o vídeo

        imgCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgTh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgTh, 5)
        kernel = np.ones((3, 3), np.int8)
        imgDil = cv2.dilate(imgMedian, kernel)

        vagasAbertas = 0

        for x, y, w, h in vagas:
            vaga = imgDil[y:y+h, x:x+w]
            count = cv2.countNonZero(vaga)
            cv2.putText(img, str(count), (x, y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            if count < 3700:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                vagasAbertas += 1
            else:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

        cv2.rectangle(img, (90, 0), (415, 60), (0, 255, 0), -1)
        cv2.putText(img, f'VAGAS LIVRES: {vagasAbertas}/3', (95, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 5)

        cv2.imshow('video', img)
        cv2.imshow('video Th', imgDil)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break