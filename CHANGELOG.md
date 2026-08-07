# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

## [Unreleased]

### Planejado
- Backend web para substituir o fluxo via terminal/desktop.
- Interface para cadastro de alunos e gabaritos sem editar arquivos manualmente.
- Suíte de testes automatizados.

Veja `docs/ROADMAP.md` para mais detalhes.

## [0.1.0] - Publicação inicial como projeto open source

### Adicionado
- Estrutura de repositório público (README, LICENSE, CONTRIBUTING,
  CODE_OF_CONDUCT, documentação em `docs/`).
- Suporte a configuração de credenciais de e-mail via variáveis de ambiente
  (`.env` / `.env.example`) usando `python-dotenv`.

### Alterado
- Credenciais de e-mail que estavam hardcoded em `projeto.py` agora são lidas
  de variáveis de ambiente.
- Arquivo `alunos.txt` de exemplo passou a conter dados fictícios em vez de
  dados reais de alunos.

### Segurança
- Removidas credenciais de e-mail (usuário e senha de app do Gmail)
  hardcoded no código-fonte.
- Removidos dados pessoais reais de alunos (nomes, e-mails, notas) do
  arquivo `alunos.txt` versionado.

## [0.0.0] - Versão acadêmica original

- Versão desenvolvida como projeto da disciplina de Visão Computacional
  (UFABC): geração de formulários com QR Code, correção automática via
  visão computacional e envio de resultados por e-mail.
