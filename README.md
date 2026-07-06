# MailMind — Triagem Automática de E-mails
 
> Sistema de triagem automática de e-mails para a Nexus Consultoria.
> Classifica por categoria e urgência, gera resumo executivo e sugere resposta profissional usando IA.
---
 
## Funcionalidades
 
- Classifica e-mails por categoria (proposta, reunião, financeiro, reclamação...)
- Define urgência (alta, média, baixa) automaticamente
- Gera resumo executivo em 2-3 frases
- Sugere resposta profissional pronta para enviar
- Proteção contra prompt injection via conteúdo de e-mail
- Exporta relatório em JSON para integração com outras ferramentas
- Testes unitários com cobertura completa
 
---
 
## Stack
 
| Camada | Tecnologia |
|--------|-----------|
| LLM | Anthropic Claude Haiku |
| Interface | Rich (CLI) |
| Segurança | bleach + whitelist de valores |
 
---
 
## Como rodar
 
```bash
git clone https://github.com/FernandaAndradedev-hash/Sistema-de-Triagem-Automatizada.git
cd Sistema-de-Triagem-Automatizada
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Preencha ANTHROPIC_API_KEY no .env
 
# Triagem resumida:
python src/cli.py
 
# Com detalhes completos:
python src/cli.py --detail
```
 
---
 
## Testes
 
```bash
pytest tests/ -v
```
 
---
 
## Estrutura
 
````
Sistema-de-Triagem-Automatizada/
├── src/
│   ├── config.py         # Configurações
│   ├── validators.py     # Segurança e sanitização
│   ├── email_data.py     # E-mails fictícios
│   ├── classifier.py     # Classificação
│   ├── summarizer.py     # Resumo executivo
│   ├── responder.py      # Resposta sugerida
│   ├── pipeline.py       # Orquestrador
│   └── cli.py            # Interface CLI
├── data/output/          # Relatórios JSON
└── tests/
````
 
---
 
## Licença
 
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.