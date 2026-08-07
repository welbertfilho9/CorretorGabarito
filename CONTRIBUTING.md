# Contribuindo com o CorretorGabarito

Obrigado pelo interesse em contribuir! Este é um projeto pessoal/acadêmico em
evolução (a parte de backend/web ainda está em desenvolvimento), então
contribuições, sugestões e correções são muito bem-vindas.

## Como contribuir

1. Faça um fork do repositório.
2. Crie uma branch a partir da `main` com um nome descritivo:
   `git checkout -b feature/nome-da-feature` ou `fix/nome-do-bug`.
3. Faça suas alterações, mantendo o estilo do código existente.
4. Teste manualmente o fluxo afetado (o projeto ainda não possui suíte de
   testes automatizados — veja o roadmap em `docs/ROADMAP.md`).
5. Abra um Pull Request descrevendo:
   - O que foi alterado e por quê.
   - Como testar a mudança.
   - Screenshots/GIFs, se a mudança for visual (ex.: layout do formulário).

## Padrão de commits

Recomendamos mensagens de commit curtas e descritivas, seguindo mais ou
menos o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adiciona suporte a formulários com 25 questões
fix: corrige leitura de QR Code em imagens com baixa iluminação
docs: atualiza instruções de instalação no README
refactor: extrai lógica de leitura de alunos para função própria
```

## Organização do código

- `formularios.py` — geração dos formulários (PNG/PDF) com QR Code.
- `comparacao.py` — script de apoio para testar filtros de processamento de imagem.
- `projeto.py` — captura, correção automática e envio de e-mail com o resultado.

Veja `docs/ARQUITETURA.md` para uma visão geral de como os módulos se
relacionam antes de propor mudanças estruturais.

## Abrindo Issues

Ao abrir uma issue, inclua:

- Uma descrição clara do problema ou sugestão.
- Passos para reproduzir (no caso de bugs).
- Sistema operacional, versão do Python e das bibliotecas relevantes.
- Imagens de exemplo, se o problema for relacionado à detecção/leitura de
  formulários (sem incluir dados reais de alunos — use os exemplos em
  `exemplos/` ou dados fictícios).

## Pull Requests

- Mantenha os PRs focados em uma única mudança lógica.
- Não inclua dados sensíveis (nomes reais, e-mails, credenciais) em nenhum
  arquivo, commit ou captura de tela.
- Descreva claramente qualquer mudança de comportamento visível ao usuário.

## Segurança

Se você encontrar uma vulnerabilidade de segurança (por exemplo, uma forma de
vazar credenciais ou dados de alunos), por favor não abra uma issue pública.
Entre em contato diretamente com o mantenedor do repositório.
