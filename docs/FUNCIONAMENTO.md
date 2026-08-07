# Como funciona o corretor

Este documento detalha, passo a passo, como `projeto.py` transforma uma foto
de uma folha de respostas em uma nota, com base nas técnicas de visão
computacional usadas.

## 1. Aquisição da imagem

Três modos disponíveis:

- **Captura (modo 1):** abre a webcam em modo de pré-visualização contínua;
  o usuário posiciona o formulário e pressiona espaço para capturar assim
  que o QR Code é detectado.
- **Arquivo (modo 2):** abre um seletor de arquivos (`tkinter.filedialog`)
  para escolher uma imagem já existente.
- **Webcam contínua (modo 3):** processa cada frame da webcam em tempo real,
  sem etapa de captura separada.

## 2. Pré-processamento

1. Conversão para escala de cinza.
2. Redimensionamento para 720x320px (tamanho padrão do formulário).
3. Blur gaussiano (5x5) para reduzir ruído de alta frequência.
4. Binarização adaptativa (`cv2.adaptiveThreshold`, método gaussiano,
   invertida) — necessária porque a iluminação costuma variar de forma
   desigual sobre a folha física.
5. Abertura morfológica (*opening* = erosão seguida de dilatação) para
   remover pequenos ruídos que sobram da binarização.

## 3. Correção de perspectiva

Fotos tiradas em ângulo distorcem a posição das bolhas de resposta em
relação às coordenadas fixas esperadas. Para resolver isso:

1. Encontra-se o maior contorno externo na imagem binarizada — assumido
   como a borda do formulário.
2. Aproxima-se esse contorno a um polígono (`cv2.approxPolyDP`); se o
   resultado tiver 4 vértices, assume-se que é um retângulo (o formulário).
3. Os 4 pontos são ordenados (topo-esquerda, topo-direita, baixo-direita,
   baixo-esquerda) e usados em `cv2.getPerspectiveTransform` para calcular
   uma matriz de transformação que "endireita" a imagem para um retângulo
   de 688x301px.

Se o contorno não tiver exatamente 4 vértices, a imagem original é usada sem
correção (fallback).

## 4. Identificação do aluno via QR Code

O QR Code impresso no formulário (gerado por `formularios.py`) contém apenas
o `id` do aluno. Ele é lido com `cv2.QRCodeDetector` sobre a imagem já
corrigida.

## 5. Detecção das marcações

As posições de cada bolha (A–E, para até 20 questões) são coordenadas fixas
pré-calculadas — não são detectadas dinamicamente a cada execução. Para cada
posição:

1. Recorta-se uma região de interesse (ROI) do tamanho da bolha.
2. Aplica-se uma máscara circular (`cv2.circle` preenchido) para considerar
   apenas os pixels dentro do círculo, ignorando o que estiver nos cantos
   do ROI retangular.
3. Calcula-se a porcentagem de pixels brancos (marcados) dentro da máscara.
4. Se essa porcentagem for **≥ 70%**, a bolha é considerada preenchida.

Esse limiar de 70% foi ajustado empiricamente (com apoio do script
`comparacao.py`) para tolerar marcações parciais ou levemente borradas sem
gerar falsos positivos por ruído.

## 6. Cálculo da nota

Para cada questão, verifica-se qual alternativa (se houver) foi marcada e
compara-se com o gabarito informado no início da execução. Acertos são
contados e desenhados em verde sobre a imagem; erros, em vermelho.

## 7. Registro e envio do resultado

Ao confirmar (tecla Enter):

1. A imagem anotada (com os círculos verde/vermelho e a nota) é salva em
   `provas_corrigidas/<nome_do_aluno>.jpg`.
2. A nota é gravada de volta em `alunos.txt`, na linha correspondente ao
   `id` do aluno.
3. Um e-mail é enviado ao aluno com a nota, a imagem corrigida e uma imagem
   do gabarito, usando uma conta Gmail configurada via variáveis de
   ambiente (veja `.env.example`).

## Limitações conhecidas

- As coordenadas das bolhas são fixas para o layout gerado por
  `formularios.py`; formulários com layout diferente (ex.: gerados
  manualmente, mudança nas constantes de layout) não funcionarão sem
  recalcular essas coordenadas.
- A leitura via webcam depende do índice de dispositivo `1`
  (`cv2.VideoCapture(1)`), que pode não corresponder à câmera correta em
  todos os computadores — em alguns sistemas pode ser necessário trocar
  para `0`.
- Não há tratamento de erro para QR Codes ilegíveis além de mensagens no
  console — a interação principal ainda é via janelas do OpenCV e o
  terminal.
