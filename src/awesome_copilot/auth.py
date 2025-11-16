from typing import Optional
import hmac


# Exemplo simples de validação de api key; em produção, use Vault/Secrets Manager


def check_api_key(received: Optional[str], expected: Optional[str]) -> bool:
    if not expected:
        return True
    if not received:
        return False
    # uso de hmac.compare_digest para evitar timing attacks
    return hmac.compare_digest(received, expected)
