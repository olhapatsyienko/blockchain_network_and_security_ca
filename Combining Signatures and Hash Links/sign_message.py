# Key generation and signing adapted from the PyCA documentation.
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/
# JSON export and printed output added for this experiment.

import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey
)


def main():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    message = "Alice sends Bob 10 tokens"
    message_bytes = message.encode("utf-8")
    signature = private_key.sign(message_bytes)

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open("public_key.pem", "wb") as file:
        file.write(public_key_pem)

    signed_message = {
        "message": message,
        "signature_hex": signature.hex()
    }

    with open("signed_message.json", "w", encoding="utf-8") as file:
        json.dump(signed_message, file, indent=4)

    print("Message:", message)
    print("Message bytes:", len(message_bytes))
    print("Signature bytes:", len(signature))
    print("Signature hex:", signature.hex())
    print("\nSaved public_key.pem and signed_message.json")


if __name__ == "__main__":
    main()
