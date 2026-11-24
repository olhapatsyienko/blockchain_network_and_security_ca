# Chain verification is adapted from Barry (2020).
# https://sheldonbarry.com/2020/05/04/blockchain-explained-using-python/
#
# Signature verification is reused from Experiment Two through verify.py.
# Ed25519 and public key loading follow the PyCA documentation.
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/
#
# The combined tests and results table were developed for this project
# with assistance from OpenAI Codex.

import copy
import json

from cryptography.hazmat.primitives import serialization

from create_chain import create_chain, calculate_hash
from verify_chain import verify_chain
from verify import verify_signature


def rebuild_chain(chain):
    previous_hash = "0" * 64

    for block in chain:
        block["previous_hash"] = previous_hash
        block["hash"] = calculate_hash(block)
        previous_hash = block["hash"]


def main():
    # Load the original signed message.
    with open("signed_message.json", "r", encoding="utf-8") as file:
        signed_message = json.load(file)

    # Load the public key once and keep it unchanged.
    with open("public_key.pem", "rb") as file:
        public_key = serialization.load_pem_public_key(file.read())

    message = signed_message["message"]
    signature_hex = signed_message["signature_hex"]

    if message != "Alice sends Bob 10 tokens":
        print("Unexpected starting message.")
        return

    # Confirm that the saved message and signature match the public key.
    starting_signature_valid = verify_signature(
        message.encode("utf-8"),
        bytes.fromhex(signature_hex),
        public_key
    )

    if not starting_signature_valid:
        print("Starting signature is invalid. Check the saved files.")
        return

    # Create the chain and put the signed message in block 2.
    original = create_chain()
    original[1]["message"] = message
    original[1]["signature_hex"] = signature_hex
    rebuild_chain(original)

    # Stage 2 changes only the message.
    edited = copy.deepcopy(original)
    edited[1]["message"] = "Alice sends Bob 100 tokens"

    # Stage 3 repairs the hashes but keeps the original signature.
    rebuilt = copy.deepcopy(edited)
    rebuild_chain(rebuilt)

    tests = [
        ("Original signed chain", original, True, True),
        ("Edited message", edited, False, False),
        ("Rebuilt chain", rebuilt, True, False)
    ]

    results = []

    for name, chain, expected_chain, expected_signature in tests:
        print("\nChecking:", name)

        # Run both checks independently.
        chain_valid = verify_chain(chain)

        signature_valid = verify_signature(
            chain[1]["message"].encode("utf-8"),
            bytes.fromhex(chain[1]["signature_hex"]),
            public_key
        )

        chain_result = "Accepted" if chain_valid else "Rejected"
        signature_result = "Accepted" if signature_valid else "Rejected"

        print("Chain:", chain_result)
        print("Signature:", signature_result)

        matched = (
            chain_valid == expected_chain
            and signature_valid == expected_signature
        )

        results.append(
            (name, chain_result, signature_result, matched)
        )

    print("\n{:<24} {:<12} {:<12} {}".format(
        "Test", "Chain", "Signature", "As expected"
    ))

    for name, chain_result, signature_result, matched in results:
        print("{:<24} {:<12} {:<12} {}".format(
            name, chain_result, signature_result, matched
        ))


if __name__ == "__main__":
    main()
