# Network and System Security CA

Demonstration code for three experiments on hash-linked chains and Ed25519 signatures, run on Kali Linux. Experiments 2 and 3 use cryptography 49.0.0. Kali blocks system-wide pip, so that library was installed with `python3-cryptography` from apt or in a virtual environment.

## Experiment 1: Changing a Hash-Linked Chain

Tests whether editing a transaction in a chain of three blocks makes verification fail, and whether the chain is accepted again after the changed block’s hash and the later links are rebuilt.

- `create_chain.py` builds three blocks: “Genesis block”, “Alice sends Bob 10 tokens”, “End of demonstration”
- Each block stores its number, message, previous hash and its own SHA-256 hash. The first previous hash is 64 zeros. The hash is SHA-256 of the block number, message and previous hash as JSON (sorted keys, UTF-8). The stored hash is left out of that input
- The chain is saved to `chain.json`
- `verify_chain.py` recalculates each hash and checks that each previous-hash field matches the block before it. Adapted from Barry’s (2020) `checkChainValid()`, using dictionaries, with checks for an empty chain and the genesis block
- `run_tests.py` checks the saved chain, then edits copies. Deep copies leave `chain.json` unchanged
- Run: `python3 create_chain.py`, `python3 verify_chain.py`, `python3 run_tests.py`

**Results**

- Original chain: accepted
- Amount in block 2 changed from 10 to 100, hashes left as stored: rejected (content hash mismatch)
- Only block 2’s hash recalculated: rejected (block 3 still holds the old previous hash)
- Links and hashes rebuilt from block 2: accepted

The rebuilt chain matches the edited message. Acceptance shows the links are consistent. It does not show that the original record was kept.

## Experiment 2: Verifying Digital Signatures

Code is in `Two Verifying Digital Signatures`. Python 3.13. Tests whether an Ed25519 signature is accepted only when the message, the signature and the public key are the ones used at signing time.

- `sign_message.py` signs “Alice sends Bob 10 tokens” (25 UTF-8 bytes, no newline) and writes `private_key.pem` (PKCS8), `public_key.pem` (SubjectPublicKeyInfo) and `signed_message.json` (64-byte signature as hex)
- `verify.py` returns true only if verification does not raise `InvalidSignature`. It does not generate keys
- `run_tests.py` reloads the saved files and changes one input at a time
- Run from that folder: `python3 sign_message.py`, then `python3 run_tests.py`
- The private key stays in the signing folder. Experiment 3 reuses `verify.py` with a new key pair and a new signed message

**Results**

- Original message, signature and key: accepted
- “10” changed to “100”, not signed again: rejected
- Second, unrelated public key: rejected
- First signature byte flipped from 87 to 86 (still 64 bytes): rejected

A pass shows those bytes were signed by the matching private key. The public key file is not tied to a real Alice and the check does not cover token ownership or replay.

## Experiment 3: Combining Signatures and Hash Links

Code is in `combined_ex`, so the first two experiments stay unchanged. Python 3.14.8. Tests whether rebuilding the hashes after an edit also makes the original signature valid again.

- `sign_message.py` creates a new Ed25519 key pair, signs the same 25-byte message, and saves `public_key.pem` and `signed_message.json`. The private key is kept in memory and is not written to disk
- `verify.py` is the check from Experiment 2
- Copies of `create_chain.py` and `verify_chain.py` include `signature_hex` in each block hash. Blocks with no signature use an empty string
- `run_combined.py` checks the saved signature, places the signed transaction in block 2, then runs three stages on deep copies. The edited message is not signed again
- Chain and signature checks run separately, so a signature result is still recorded when the chain fails
- Run: `python3 run_combined.py`

**Results**

- Original signed chain: chain accepted, signature accepted
- Message changed from 10 to 100, signature and hashes left as stored: chain rejected, signature rejected
- Hashes and links rebuilt, original signature kept: chain accepted, signature rejected

Rebuilding makes the chain consistent with the edited data. It does not create a valid signature for the new message. A chain pass on its own does not show that the transaction still matches what was signed.
