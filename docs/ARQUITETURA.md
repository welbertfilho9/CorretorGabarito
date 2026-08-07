# Arquitetura

> Este documento descreve a arquitetura **atual** do projeto: três scripts
> Python independentes que, juntos, formam o fluxo de geração e correção de
> gabaritos. Não há, hoje, um backend web — essa é a próxima etapa planejada
> (veja `ROADMAP.md`).

## Visão geral

```
┌─────────────────┐      ┌──────────────────┐      ┌───────────────────┐
│  formularios.py  │      │   comparacao.py   │      │    projeto.py      │
│                  │      │                    │      │                    │
│  Gera formulários│      │  Ferramenta de     │      │  Captura, corrige  │
│  em PNG/PDF com  │      │  calibração visual │      │  e envia resultado │
│  QR Code por     │      │  de filtros de     │      │  por e-mail        │
│  aluno           │      │  imagem            │      │                    │
└────────┬─────────┘      └────────────────────┘      └─────────┬──────────┘
         │                                                        │
         │              alunos.txt (id, nome, email, nota)        │
         └───────────────────────┬────────────────────────────────┘
                                  ▼
                         armazenamento em CSV
```

Os três scripts compartilham o mesmo arquivo `alunos.txt` como fonte da
verdade sobre os alunos e como destino da nota final. Não há banco de dados;
a "persistência" é um arquivo texto simples.

## Módulos

### `formularios.py` — Geração de formulários

- Lê `alunos.txt` (CSV com `id,nome,email`).
- Para cada aluno, desenha um formulário de 720x320px contendo:
  - Nome do aluno.
  - QR Code codificando o `id` do aluno (usado depois para identificação
    automática na correção).
  - Colunas de bolhas de resposta (A–E) para até 20 questões.
- Salva um PNG por aluno em `formularios_gerados/` e compila todos em um
  único PDF (`formularios_gerados/formularios_todos.pdf`), pronto para
  impressão.
- As coordenadas de cada bolha são calculadas e devolvidas em memória —
  **mas não são persistidas em disco**, pois `projeto.py` usa um conjunto de
  coordenadas fixas equivalente, calculado para o mesmo layout (ver seção
  "Acoplamento por coordenadas fixas" abaixo).

### `comparacao.py` — Ferramenta de calibração

- Não faz parte do fluxo de produção; é usada durante o desenvolvimento
  para visualizar, lado a lado, o efeito de diferentes filtros (blur,
  binarização adaptativa, operações morfológicas) sobre uma imagem de
  exemplo (`exemplos/ex1.jpg`).
- Serve para decidir os parâmetros (limiares, kernels) usados depois em
  `projeto.py`.

### `projeto.py` — Correção automática

Fluxo principal, executado via terminal:

1. Pergunta o número de questões e o gabarito (resposta correta de cada
   questão).
2. Obtém uma imagem da folha de respostas por um de três meios:
   - Captura via webcam (aguarda o usuário pressionar espaço).
   - Seleção de um arquivo de imagem já existente.
   - Leitura contínua da webcam (modo "3").
3. Aplica pré-processamento: escala de cinza, blur gaussiano, binarização
   adaptativa, abertura morfológica (*opening*) para reduzir ruído.
4. Detecta o maior contorno da imagem (a borda do formulário) e aplica uma
   correção de perspectiva (`cv2.getPerspectiveTransform`) para alinhar o
   formulário, mesmo se fotografado em ângulo.
5. Lê o QR Code para identificar o `id` do aluno.
6. Para cada uma das ~100 posições fixas de bolha, calcula a porcentagem de
   pixels brancos dentro do círculo; acima de 70%, considera a alternativa
   marcada.
7. Compara a alternativa marcada com o gabarito e calcula a nota.
8. Ao pressionar Enter, salva a imagem corrigida em `provas_corrigidas/`,
   atualiza a nota em `alunos.txt` e envia um e-mail ao aluno com o
   resultado e uma imagem do gabarito.

## Acoplamento por coordenadas fixas

Um ponto importante da arquitetura atual: as posições de cada bolha de
resposta **não são detectadas dinamicamente** — são coordenadas fixas,
definidas como constantes tanto em `projeto.py` quanto em `comparacao.py`.
Isso funciona porque `formularios.py` sempre gera formulários no mesmo
layout de 720x320px. Se os parâmetros de layout em `formularios.py` forem
alterados, essas coordenadas precisam ser recalculadas manualmente nos
outros dois scripts — esse é um dos pontos de melhoria mapeados no roadmap.

## Envio de e-mail

O envio é feito via `smtplib` usando uma conta Gmail com **senha de app**
(não a senha normal da conta). As credenciais são lidas de variáveis de
ambiente (`EMAIL_REMETENTE`, `EMAIL_SENHA_APP`), carregadas de um arquivo
`.env` local via `python-dotenv` — veja `.env.example`.

## Persistência de dados

| Arquivo/pasta            | Papel                                                        |
|---------------------------|---------------------------------------------------------------|
| `alunos.txt`               | CSV com `id,nome,email,nota` — lido e escrito por todos os scripts. |
| `gabaritos/gabaritoN.png`  | Imagem em branco do formulário para N questões, usada como referência visual ao corrigir. |
| `formularios_gerados/`     | Saída de `formularios.py` (gerada, não versionada).            |
| `provas_corrigidas/`       | Saída de `projeto.py` (gerada, não versionada).                |
| `exemplos/`                | Imagens de exemplo para calibração em `comparacao.py`.         |

## Por que não há backend ainda?

O projeto nasceu como um trabalho acadêmico de Visão Computacional, focado
em resolver o problema de processamento de imagem (leitura de QR Code,
correção de perspectiva, detecção de marcações). A camada de interação hoje
é o terminal + janelas do OpenCV. Um backend web (API + frontend) permitiria
cadastro de alunos e gabaritos sem editar arquivos manualmente, upload de
imagens pelo navegador e histórico de correções — está descrito em
`ROADMAP.md`.
