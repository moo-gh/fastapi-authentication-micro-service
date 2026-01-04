import hmac
import hashlib
import json
import time
from app.core.config import settings

class VerificationSigner:
    @staticmethod
    def sign_payload(payload: dict) -> str:
        """
        Signs a payload dictionary using HMAC SHA256.
        """
        # Ensure payload is sorted for consistent signing
        message = json.dumps(payload, sort_keys=True).encode("utf-8")
        signature = hmac.new(
            settings.SECRET_KEY.encode("utf-8"),
            message,
            hashlib.sha256
        ).hexdigest()
        return signature

    @staticmethod
    def verify_signature(payload: dict, signature: str) -> bool:
        """
        Verifies if the signature matches the payload.
        """
        expected_signature = VerificationSigner.sign_payload(payload)
        return hmac.compare_digest(expected_signature, signature)


