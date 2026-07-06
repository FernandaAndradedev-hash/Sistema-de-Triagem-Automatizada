import os
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test-fake")

from unittest.mock import MagicMock, patch
from email_data import Email, TriagedEmail


SAMPLE_EMAIL = Email(
    id="001",
    sender_name="Test User",
    sender_email="test@test.com",
    subject="Test subject",
    body="Test body content.",
    received_at="2024-03-15 09:00:00",
)


class TestPipeline:

    @patch("pipeline.suggest_reply")
    @patch("pipeline.summarize_email")
    @patch("pipeline.classify_email")
    def test_processo_completo(self, mock_classify, mock_summarize, mock_reply):
        mock_classify.return_value = {"category": "proposta", "urgency": "alta", "reason": ""}
        mock_summarize.return_value = "Resumo do e-mail."
        mock_reply.return_value = "Resposta sugerida."

        from pipeline import process_email
        result = process_email(SAMPLE_EMAIL)

        assert result.category == "proposta"
        assert result.urgency == "alta"
        assert result.summary == "Resumo do e-mail."
        assert result.suggested_reply == "Resposta sugerida."
        assert result.error == ""

    @patch("pipeline.classify_email")
    def test_erro_retorna_triage_com_erro(self, mock_classify):
        mock_classify.side_effect = Exception("API error")

        from pipeline import process_email
        result = process_email(SAMPLE_EMAIL)

        assert result.error != ""
        assert result.category == ""

    @patch("pipeline.suggest_reply")
    @patch("pipeline.summarize_email")
    @patch("pipeline.classify_email")
    def test_run_triage_processa_lista(self, mock_classify, mock_summarize, mock_reply):
        mock_classify.return_value = {"category": "informacao", "urgency": "media", "reason": ""}
        mock_summarize.return_value = "Resumo."
        mock_reply.return_value = "Resposta."

        from pipeline import run_triage
        results = run_triage([SAMPLE_EMAIL, SAMPLE_EMAIL])

        assert len(results) == 2