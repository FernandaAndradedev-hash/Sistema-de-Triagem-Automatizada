"""
Base de e-mails fictícios da Nexus Consultoria.

Cobre os principais tipos de e-mail que uma consultoria recebe:
propostas, reuniões, financeiro, reclamações, feedback, spam e internos.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Email:
    """Representa um e-mail recebido."""
    id: str
    sender_name: str
    sender_email: str
    subject: str
    body: str
    received_at: str


@dataclass
class TriagedEmail:
    """E-mail após triagem completa."""
    email: Email
    category: str = ""
    urgency: str = ""
    summary: str = ""
    suggested_reply: str = ""
    error: str = ""


SAMPLE_EMAILS = [
    Email(
        id="001",
        sender_name="Ricardo Almeida",
        sender_email="ricardo.almeida@distribuidoramax.com.br",
        subject="Solicitação de Proposta — Consultoria de Processos",
        body="""
Boa tarde,

Meu nome é Ricardo Almeida, sou Diretor de Operações da Distribuidora Max Ltda.
Estamos passando por um momento de crescimento acelerado e identificamos que nossos
processos internos precisam de reestruturação.

Gostaríamos de receber uma proposta de consultoria para mapeamento e otimização
de processos nas áreas de logística, compras e financeiro. Nossa empresa tem
aproximadamente 200 colaboradores e faturamento anual de R$ 45 milhões.

Podemos agendar uma reunião de alinhamento para a próxima semana?

Att,
Ricardo Almeida
(11) 99999-5678
        """,
        received_at="2024-03-15 09:30:00",
    ),
    Email(
        id="002",
        sender_name="Carla Mendonça",
        sender_email="carla.mendonca@techsolutions.com.br",
        subject="URGENTE — Problema grave com entrega do projeto",
        body="""
Prezados,

Estou extremamente insatisfeita com a condução do projeto de reestruturação
organizacional que contratamos com vocês há 3 meses.

Os prazos acordados não foram cumpridos, os relatórios entregues estão incompletos
e nossa equipe não recebeu o treinamento prometido. Investimos R$ 80.000 neste
projeto e o retorno está muito aquém do esperado.

Solicito reunião URGENTE com o responsável pelo projeto até amanhã. Caso não
haja resposta satisfatória, tomaremos medidas legais.

Carla Mendonça
Diretora Executiva — TechSolutions
        """,
        received_at="2024-03-15 10:15:00",
    ),
    Email(
        id="003",
        sender_name="Paulo Henrique",
        sender_email="paulo.henrique@grupoalfa.com.br",
        subject="Confirmação de reunião — Quinta-feira 14h",
        body="""
Olá,

Confirmo minha presença na reunião de apresentação de resultados do diagnóstico
organizacional marcada para quinta-feira, dia 18/03, às 14h00, na sede de vocês.

Participarão da minha parte: eu, o CFO Marcos Ribeiro e a gerente de RH Ana Paula.

Precisam de alguma documentação ou material da nossa parte para a reunião?

Abraços,
Paulo Henrique
CEO — Grupo Alfa
        """,
        received_at="2024-03-15 11:00:00",
    ),
    Email(
        id="004",
        sender_name="Financeiro Indústrias Beta",
        sender_email="financeiro@industriasbeta.com.br",
        subject="NF 4521 — Pagamento em atraso",
        body="""
Prezados,

Identificamos que a Nota Fiscal nº 4521, emitida em 15/02/2024, no valor de
R$ 28.500,00, com vencimento em 15/03/2024, ainda não foi liquidada em nosso sistema.

Solicitamos a regularização do pagamento ou confirmação de comprovante até
esta sexta-feira para evitar incidência de juros e multa contratual.

Departamento Financeiro
Indústrias Beta S.A.
        """,
        received_at="2024-03-15 11:30:00",
    ),
    Email(
        id="005",
        sender_name="Juliana Ferreira",
        sender_email="juliana.ferreira@construtoranova.com.br",
        subject="Feedback sobre consultoria — Muito satisfeita!",
        body="""
Boa tarde,

Gostaria de registrar meu agradecimento pelo excelente trabalho realizado pela
equipe da Nexus na reestruturação do nosso departamento de RH.

Os resultados superaram nossas expectativas: reduzimos o turnover em 35% e
o tempo de onboarding caiu de 30 para 12 dias. A equipe foi extremamente
profissional e comprometida durante todo o projeto.

Com certeza indicaremos a Nexus para nossos parceiros de negócio.

Parabéns a toda a equipe!

Juliana Ferreira
Diretora de RH — Construtora Nova
        """,
        received_at="2024-03-15 13:00:00",
    ),
    Email(
        id="006",
        sender_name="Newsletter Empresarial",
        sender_email="noreply@newsletterempresarial.com.br",
        subject=" As 10 tendências de gestão para 2024 — Edição especial",
        body="""
Olá gestor(a)!

Não perca nossa edição especial com as 10 principais tendências de gestão
empresarial para 2024! ESG, IA nos negócios, gestão ágil e muito mais.

➡️ ACESSE AGORA: www.newsletterempresarial.com.br/edicao-especial

Aproveite também nossa oferta exclusiva: 50% OFF no curso de Gestão Estratégica!
Use o cupom: GESTAO2024

Para cancelar o recebimento deste e-mail, clique aqui.
        """,
        received_at="2024-03-15 14:00:00",
    ),
    Email(
        id="007",
        sender_name="Marcos Silva",
        sender_email="marcos.silva@nexusconsultoria.com.br",
        subject="Reunião de equipe — Pauta semana 12",
        body="""
Pessoal,

Segue a pauta da nossa reunião semanal de segunda-feira às 9h:

1. Status dos projetos em andamento (15 min)
2. Pipeline de novos clientes (10 min)
3. Férias do time em abril — alinhamento de cobertura (10 min)
4. Atualização do template de proposta comercial (15 min)

Por favor, atualizem o status dos seus projetos no sistema até domingo à noite.

Abs,
Marcos Silva
Sócio-Diretor — Nexus Consultoria
        """,
        received_at="2024-03-15 15:00:00",
    ),
    Email(
        id="008",
        sender_name="Ana Carolina Ramos",
        sender_email="ana.ramos@grupomercantil.com.br",
        subject="Dúvida sobre metodologia de consultoria de vendas",
        body="""
Boa tarde,

Encontrei a Nexus Consultoria através de uma indicação e tenho interesse
nos serviços de consultoria de vendas para nossa rede de 15 lojas.

Gostaria de entender melhor como funciona a metodologia de vocês:
- Qual é o prazo médio de um projeto de consultoria de vendas?
- Vocês trabalham com metas e KPIs definidos?
- É possível fazer um diagnóstico inicial sem compromisso?

Aguardo retorno.

Ana Carolina Ramos
Gestora Comercial — Grupo Mercantil
        """,
        received_at="2024-03-15 16:00:00",
    ),
]


def get_all_emails() -> list[Email]:
    """Retorna todos os e-mails fictícios."""
    return SAMPLE_EMAILS


def get_email_by_id(email_id: str) -> Email | None:
    """Retorna um e-mail específico pelo ID."""
    return next((e for e in SAMPLE_EMAILS if e.id == email_id), None)