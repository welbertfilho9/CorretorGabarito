"""
Script de apoio ao desenvolvimento: exibe lado a lado diferentes etapas
de processamento de imagem (recorte, binarização, filtros morfológicos)
para ajudar a escolher os parâmetros ideais usados em projeto.py.
Não faz parte do fluxo de correção em si — é uma ferramenta de
depuração/calibração visual.
"""
import numpy as np
import cv2
import os

# --- Funções de Correção de Perspectiva (do código original) ---
def ordenar_pontos(pontos):
    pontos = pontos.reshape((4, 2))
    soma = pontos.sum(axis=1)
    diff = np.diff(pontos, axis=1)

    topo_esq = pontos[np.argmin(soma)]
    baixo_dir = pontos[np.argmax(soma)]
    topo_dir = pontos[np.argmin(diff)]
    baixo_esq = pontos[np.argmax(diff)]

    return np.array([topo_esq, topo_dir, baixo_dir, baixo_esq], dtype="float32")

def aplicar_transformacao_perspectiva(img, contorno, largura=688, altura=301):
    epsilon = 0.02 * cv2.arcLength(contorno, True)
    aproximado = cv2.approxPolyDP(contorno, epsilon, True)

    if len(aproximado) == 4:
        pontos_ordenados = ordenar_pontos(aproximado)

        destino = np.array([
            [0, 0],
            [largura - 1, 0],
            [largura - 1, altura - 1],
            [0, altura - 1]
        ], dtype="float32")

        matriz = cv2.getPerspectiveTransform(pontos_ordenados, destino)
        corrigido = cv2.warpPerspective(img, matriz, (largura, altura))
        return corrigido
    else:
        return img

coordenadas = [
    (198, 14, 20, 20), (238, 14, 20, 20), (278, 14, 20, 20), (318, 14, 20, 20), (358, 14, 20, 20),
    (198, 42, 20, 20), (238, 42, 20, 20), (278, 42, 20, 20), (318, 42, 20, 20), (358, 42, 20, 20),
    (198, 70, 20, 20), (238, 70, 20, 20), (278, 70, 20, 20), (318, 70, 20, 20), (358, 70, 20, 20),
    (198, 98, 20, 20), (238, 98, 20, 20), (278, 98, 20, 20), (318, 98, 20, 20), (358, 98, 20, 20),
    (198, 126, 20, 20), (238, 126, 20, 20), (278, 126, 20, 20), (318, 126, 20, 20), (358, 126, 20, 20),
    (198, 154, 20, 20), (238, 154, 20, 20), (278, 154, 20, 20), (318, 154, 20, 20), (358, 154, 20, 20),
    (198, 182, 20, 20), (238, 182, 20, 20), (278, 182, 20, 20), (318, 182, 20, 20), (358, 182, 20, 20),
    (198, 210, 20, 20), (238, 210, 20, 20), (278, 210, 20, 20), (318, 210, 20, 20), (358, 210, 20, 20),
    (198, 238, 20, 20), (238, 238, 20, 20), (278, 238, 20, 20), (318, 238, 20, 20), (358, 238, 20, 20),
    (198, 266, 20, 20), (238, 266, 20, 20), (278, 266, 20, 20), (318, 266, 20, 20), (358, 266, 20, 20),
    (479, 14, 20, 20), (519, 14, 20, 20), (559, 14, 20, 20), (599, 14, 20, 20), (639, 14, 20, 20),
    (479, 42, 20, 20), (519, 42, 20, 20), (559, 42, 20, 20), (599, 42, 20, 20), (639, 42, 20, 20),
    (479, 70, 20, 20), (519, 70, 20, 20), (559, 70, 20, 20), (599, 70, 20, 20), (639, 70, 20, 20),
    (479, 98, 20, 20), (519, 98, 20, 20), (559, 98, 20, 20), (599, 98, 20, 20), (639, 98, 20, 20),
    (479, 126, 20, 20), (519, 126, 20, 20), (559, 126, 20, 20), (599, 126, 20, 20), (639, 126, 20, 20),
    (479, 154, 20, 20), (519, 154, 20, 20), (559, 154, 20, 20), (599, 154, 20, 20), (639, 154, 20, 20),
    (479, 182, 20, 20), (519, 182, 20, 20), (559, 182, 20, 20), (599, 182, 20, 20), (639, 182, 20, 20),
    (479, 210, 20, 20), (519, 210, 20, 20), (559, 210, 20, 20), (599, 210, 20, 20), (639, 210, 20, 20),
    (479, 238, 20, 20), (519, 238, 20, 20), (559, 238, 20, 20), (599, 238, 20, 20), (639, 238, 20, 20),
    (479, 266, 20, 20), (519, 266, 20, 20), (559, 266, 20, 20), (599, 266, 20, 20), (639, 266, 20, 20)
]

# 1. Carregar a imagem
caminho_imagem = "exemplos/ex1.jpg" # Certifique-se que este caminho está correto
img = cv2.imread(caminho_imagem)

print("1-exemplo do recorte\n2-exemplo dos filtros\n")
exemplo = int(input('Escolha um exemplo: '))

nada = img.copy()
# Redimensionar a imagem original para um tamanho base (opcional, mas ajuda na consistência)
# Usando as dimensões do código original como referência, mas pode ajustar
img = cv2.resize(img, (720, 320))
nada = img.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


borrada = cv2.GaussianBlur(img_gray, (5, 5), 0)
binario = cv2.adaptiveThreshold(borrada, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
binario1 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
kernel = np.ones((3, 3), np.uint8)
dilate = cv2.dilate(binario, kernel, iterations=1)
opening = cv2.morphologyEx(binario, cv2.MORPH_OPEN, kernel)
contornos, _ = cv2.findContours(binario, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
maior_contorno = max(contornos, key=cv2.contourArea)
x, y, w, h = cv2.boundingRect(maior_contorno)
recorte = img[y:y + h, x:x + w]
recorte = cv2.resize(recorte, (688, 301))
recorte1 = recorte.copy()

print("Aplicando correção de perspectiva...")


recorte_corrigido = aplicar_transformacao_perspectiva(img, maior_contorno)
recorte_corrigido1 = recorte_corrigido.copy()
recorte85 = recorte_corrigido.copy()
recorte90 = recorte_corrigido.copy()
recorte87 = recorte_corrigido.copy()
recorte70 = recorte_corrigido.copy()
recorte55 = recorte_corrigido.copy()

# Aplicar ao Grayscale Original (antes do blur)
corrigido_gray = aplicar_transformacao_perspectiva(img_gray, maior_contorno)

# Aplicar ao Blurred
corrigido_blur = aplicar_transformacao_perspectiva(borrada, maior_contorno)

# Aplicar ao Binarizado
corrigido_binary = aplicar_transformacao_perspectiva(binario, maior_contorno)

corrigido_binary1 = aplicar_transformacao_perspectiva(binario1, maior_contorno)

corrigido_dilate = aplicar_transformacao_perspectiva(dilate, maior_contorno)

# Aplicar ao Opened
corrigido_opened = aplicar_transformacao_perspectiva(opening, maior_contorno)

# --- Exibir Resultados ---
respostas_marcadas0 = []
respostas_marcadas = []
respostas_marcadas1 = []
respostas_marcadas2 = []
respostas_marcadas3 = []


if exemplo == 1:
    for i, (x, y, w, h) in enumerate(coordenadas):
        interesse = corrigido_opened[y:y + h, x:x + w]
        mascara = np.zeros((h, w), dtype=np.uint8)
        centro_x = w // 2
        centro_y = h // 2
        raio = min(w, h) // 2
        cv2.circle(mascara, (centro_x, centro_y), raio, 255, -1)
        interesse_mascarado = cv2.bitwise_and(interesse, interesse, mask=mascara)
        total_pixels = cv2.countNonZero(mascara)
        pixels_brancos = cv2.countNonZero(interesse_mascarado)
        porcentagem_branco = (pixels_brancos / total_pixels) * 100

        if porcentagem_branco >= 70:
            respostas_marcadas.append(i)

    for i in range(20):
        alternativas_questao = [(i * 5) + j for j in range(5)]

        for j in alternativas_questao:
            if j in respostas_marcadas:
                marcada = j
                resposta_marcada = j % 5
                x, y, w, h = coordenadas[marcada]
                cor = (0, 255, 0)
                centro_x = x + w // 2
                centro_y = y + h // 2
                raio = min(w, h) // 2
                cv2.circle(recorte, (centro_x, centro_y), raio, cor, 2)
                cv2.circle(recorte_corrigido, (centro_x, centro_y), raio, cor, 2)
                cv2.circle(corrigido_gray, (centro_x, centro_y), raio, cor, 2)
                cv2.circle(corrigido_blur, (centro_x, centro_y), raio, cor, 2)
                cv2.circle(corrigido_binary, (centro_x, centro_y), raio, cor, 2)
                cv2.circle(corrigido_opened, (centro_x, centro_y), raio, cor, 2)
                break

    cv2.imshow("Sem recorte", nada)
    cv2.imshow("Original", recorte1)
    cv2.imshow("Original Redimensionada", recorte_corrigido1)
    cv2.imshow("Original Marcada", recorte)
    cv2.imshow("Original Redimensionada Marcada", recorte_corrigido)


print("Exibindo imagens...")

# Exibe as versões corrigidas
if exemplo == 2:
    for i, (x, y, w, h) in enumerate(coordenadas):
        interesse = corrigido_opened[y:y + h, x:x + w]
        interesse1 = corrigido_binary[y:y + h, x:x + w]
        mascara = np.zeros((h, w), dtype=np.uint8)
        centro_x = w // 2
        centro_y = h // 2
        raio = min(w, h) // 2
        cv2.circle(mascara, (centro_x, centro_y), raio, 255, -1)
        interesse_mascarado = cv2.bitwise_and(interesse, interesse, mask=mascara)
        interesse_mascarado1 = cv2.bitwise_and(interesse1, interesse1, mask=mascara)
        total_pixels = cv2.countNonZero(mascara)
        pixels_brancos = cv2.countNonZero(interesse_mascarado)
        pixels_brancos1 = cv2.countNonZero(interesse_mascarado1)
        porcentagem_branco = (pixels_brancos / total_pixels) * 100
        porcentagem_branco1 = (pixels_brancos1 / total_pixels) * 100

        if porcentagem_branco1 >= 90:
            respostas_marcadas3.append(i)
        if porcentagem_branco1 >= 85:
            respostas_marcadas2.append(i)
        if porcentagem_branco1 >= 80:
            respostas_marcadas1.append(i)
        if porcentagem_branco >= 70:
            respostas_marcadas.append(i)
        if porcentagem_branco >= 55:
            respostas_marcadas0.append(i)


    for i in range(20):
        alternativas_questao = [(i * 5) + k for k in range(5)]
        for j in alternativas_questao:
            if j in respostas_marcadas:
                x, y, w, h = coordenadas[j]
                cor = (0, 255, 0)
                centro_x = x + w // 2
                centro_y = y + h // 2
                raio = min(w, h) // 2
                cv2.circle(recorte70, (centro_x, centro_y), raio, cor, 2)
                break

    for i in range(20):
        alternativas_questao = [(i * 5) + k for k in range(5)]
        for j in alternativas_questao:
            if j in respostas_marcadas1:
                x, y, w, h = coordenadas[j]
                cor = (0, 0, 255)
                centro_x = x + w // 2
                centro_y = y + h // 2
                raio = min(w, h) // 2
                cv2.circle(recorte85, (centro_x, centro_y), raio, cor, 2)
                break

    for i in range(20):
        alternativas_questao = [(i * 5) + k for k in range(5)]
        for j in alternativas_questao:
            if j in respostas_marcadas2:
                x, y, w, h = coordenadas[j]
                cor = (255, 255, 0)
                centro_x = x + w // 2
                centro_y = y + h // 2
                raio = min(w, h) // 2
                cv2.circle(recorte87, (centro_x, centro_y), raio, cor, 2)
                break

    for i in range(20):
        alternativas_questao = [(i * 5) + k for k in range(5)]
        for j in alternativas_questao:
            if j in respostas_marcadas3:
                x, y, w, h = coordenadas[j]
                cor = (0, 255, 255)
                centro_x = x + w // 2
                centro_y = y + h // 2
                raio = min(w, h) // 2
                cv2.circle(recorte90, (centro_x, centro_y), raio, cor, 2)
                break
    for i in range(20):
        alternativas_questao = [(i * 5) + k for k in range(5)]
        for j in alternativas_questao:
            if j in respostas_marcadas0:
                x, y, w, h = coordenadas[j]
                cor = (0, 255, 255)
                centro_x = x + w // 2
                centro_y = y + h // 2
                raio = min(w, h) // 2
                cv2.circle(recorte55, (centro_x, centro_y), raio, cor, 2)
                break

    cv2.imshow("Original Redimensionada (Color)", recorte_corrigido)
    cv2.imshow("Corrigido - Grayscale", corrigido_gray)
    cv2.imshow("Corrigido - Blur", corrigido_blur)
    cv2.imshow("Corrigido - Binarizado (Adaptive)", corrigido_binary)
    cv2.imshow("Corrigido - Binarizado Sem Blur", corrigido_binary1)
    cv2.imshow("90%", recorte90)
    cv2.imshow("85%", recorte87)
    cv2.imshow("80%", recorte85)
    cv2.imshow("Corrigido - Dilatado", corrigido_dilate)
    cv2.imshow("Corrigido - Opened", corrigido_opened)
    cv2.imshow("Corrigido 85%", recorte70)
    cv2.imshow("Corrigido 55%", recorte55)


print("Pressione qualquer tecla para fechar todas as janelas.")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Janelas fechadas.")