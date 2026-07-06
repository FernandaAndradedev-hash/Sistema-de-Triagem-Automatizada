"""
Orquestrador do pipeline de triagem de e-mails.

Coordena as três etapas: classificar → resumir → sugerir resposta.
Processa e-mails em lote e gera relatório final em JSON.
"""
import json
import logging
from datetime import datetime
from pathlib import Path

import config
from classifier import classify_email
from email_data import Email, TriagedEmail, get_all_emails
from responder import suggest_reply
from summarizer import summarize_email
from validators import validate_email

logger = logging.getLogger(__name__)


def process_email(email: Email) -> TriagedEmail:
    """
    Processa um único e-mail pelas três etapas.

    Args:
        email: E-mail bruto.

    Returns:
        TriagedEmail com classificação, resumo e resposta sugerida.
    """
    try:
        # Etapa 0: Validação e sanitização
        clean_email = validate_email(email)

        # Etapa 1: Classificação
        classification = classify_email(clean_email)

        # Etapa 2: Resumo
        summary = summarize_email(clean_email)

        # Etapa 3: Resposta sugerida
        reply = suggest_reply(
            clean_email,
            category=classification["category"],
            summary=summary,
        )

        return TriagedEmail(
            email=email,
            category=classification["category"],
            urgency=classification["urgency"],
            summary=summary,
            suggested_reply=reply,
        )

    except Exception as exc:
        logger.error("Erro ao processar e-mail %s: %s", email.id, exc)
        return TriagedEmail(
            email=email,
            error=str(exc),
        )


def run_triage(emails: list[Email] | None = None) -> list[TriagedEmail]:
    """
    Executa o pipeline de triagem em uma lista de e-mails.

    Args:
        emails: Lista de e-mails. Se None, usa os e-mails fictícios.

    Returns:
        Lista de TriagedEmail com resultados completos.
    """
    if emails is None:
        emails = get_all_emails()

    logger.info("Iniciando triagem de %d e-mails...", len(emails))
    results = []

    for i, email in enumerate(emails, 1):
        logger.info("Processando e-mail %d/%d: %s", i, len(emails), email.id)
        result = process_email(email)
        results.append(result)

    # Estatísticas
    total = len(results)
    errors = sum(1 for r in results if r.error)
    by_urgency = {}
    by_category = {}

    for r in results:
        if not r.error:
            by_urgency[r.urgency] = by_urgency.get(r.urgency, 0) + 1
            by_category[r.category] = by_category.get(r.category, 0) + 1

    logger.info(
        "Triagem concluída: %d e-mails, %d erros | urgência: %s | categoria: %s",
        total, errors, by_urgency, by_category,
    )

    return results


def save_report(results: list[TriagedEmail], output_dir: str = "data/output") -> str:
    """
    Salva o relatório de triagem em JSON.

    Args:
        results: Lista de resultados da triagem.
        output_dir: Diretório de saída.

    Returns:
        Caminho do arquivo gerado.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = output_path / f"triage_{timestamp}.json"

    report = []
    for r in results:
        report.append({
            "id": r.email.id,
            "sender": r.email.sender_name,
            "subject": r.email.subject,
            "received_at": r.email.received_at,
            "category": r.category,
            "urgency": r.urgency,
            "summary": r.summary,
            "suggested_reply": r.suggested_reply,
            "error": r.error,
        })

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    logger.info("Relatório salvo: %s", filepath)
    return str(filepath)