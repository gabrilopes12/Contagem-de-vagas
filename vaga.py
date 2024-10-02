import cv2
import pickle

# Carregar e redimensionar a imagem de seleção
img = cv2.imread('foto.png')
img = cv2.resize(img, (1473, 828))  # Redimensionar a imagem para 1473x828

vagas = []
for x in range(3):  # número de vagas
    vaga = cv2.selectROI('vagas', img, False)
    cv2.destroyWindow('vagas')
    vagas.append((vaga))

    for x, y, w, h in vagas:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

with open('vagas.pkl', 'wb') as arquivo:
    pickle.dump(vagas, arquivo)