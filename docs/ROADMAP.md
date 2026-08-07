# Roadmap técnico

Este roadmap reflete o estado de "trabalho em progresso" do projeto. A parte
de visão computacional (geração e correção de gabaritos) está funcional; a
camada de backend/frontend web ainda não existe.

## Curto prazo

- [ ] Adicionar testes automatizados para as funções puras (ex.:
      `ordenar_pontos`, `aplicar_transformacao_perspectiva`,
      `carregar_dados_alunos`), usando imagens de exemplo fixas.
- [ ] Tornar o índice da webcam (`cv2.VideoCapture(1)`) configurável via
      variável de ambiente ou argumento de linha de comando, em vez de
      hardcoded.
- [ ] Tratar o caso de QR Code não detectado de forma mais robusta (retry
      configurável, mensagem mais clara para o usuário).
- [ ] Validar o formato do e-mail em `alunos.txt` ao carregar os dados.

## Médio prazo

- [ ] **Backend web** (API) para:
  - Cadastro de turmas/alunos sem editar `alunos.txt` manualmente.
  - Upload de imagem da folha de respostas pelo navegador.
  - Histórico de correções por prova/turma.
- [ ] **Frontend web** consumindo essa API (o frontend mencionado como
      "bastante completo" no projeto original ainda precisa ser integrado
      a este repositório/backend).
- [ ] Substituir o armazenamento em `alunos.txt` (CSV) por um banco de
      dados leve (ex.: SQLite) para suportar múltiplas turmas e provas.
- [ ] Detecção dinâmica da posição das bolhas (em vez de coordenadas fixas
      acopladas ao layout de `formularios.py`), permitindo layouts de
      formulário mais flexíveis.

## Longo prazo

- [ ] Suporte a folhas de resposta com layouts diferentes (ex.: mais de 20
      questões, colunas adicionais).
- [ ] Modo de correção em lote (processar várias imagens de uma vez, sem
      interação manual por prova).
- [ ] Painel de estatísticas por turma (distribuição de notas, questões com
      mais erros).

---

Sugestões e contribuições para este roadmap são bem-vindas — veja
`CONTRIBUTING.md`.
