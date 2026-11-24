# Verification function reproduced from Experiment Two.
# The verify call and InvalidSignature behaviour are documented at
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/

from cryptography.exceptions import InvalidSignature


def verify_signature(message: bytes, signature: bytes, public_key) -> bool:
    try:
        public_key.verify(signature, message)
        return True
    except InvalidSignature:
        return False
