import os
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test-fake")

import json
from unittest.mock import MagicMock, patch

import pytest
from email_data import Email

SAMPLE_EMAIL = Email(
    id="001",
    sender_name="João Silva",
    sender_email="joao@empresa.com.br",
    subject="Solicitação de proposta",
    body="Gostaria de receber uma proposta de consultoria.",
    received_at="2024-03-15 09:00:00",
)


class TestClassifier:

    @patch("classifier._client")
    def test_classifica_proposta(self, mock_client):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "category": "proposta",
            "urgency": "alta",
            "reason": "Solicitação de proposta comercial."
        }))]
        mock_client.messages.create.return_value = mock_response

        from classifier import classify_email
        result = classify_email(SAMPLE_EMAIL)

        assert result["category"] == "proposta"
        assert result["urgency"] == "alta"

    @patch("classifier._client")
    def test_json_invalido_usa_padrao(self, mock_client):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="isso não é json")]
        mock_client.messages.create.return_value = mock_response

        from classifier import classify_email
        result = classify_email(SAMPLE_EMAIL)

        assert result["category"] == "informacao"
        assert result["urgency"] == "media"

    @patch("classifier._client")
    def test_categoria_invalida_corrigida(self, mock_client):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "category": "categoria_que_nao_existe",
            "urgency": "alta",
            "reason": "Teste."
        }))]
        mock_client.messages.create.return_value = mock_response

        from classifier import classify_email
        result = classify_email(SAMPLE_EMAIL)

        assert result["category"] == "informacao"