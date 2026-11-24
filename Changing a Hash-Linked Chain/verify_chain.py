# Verification logic adapted from Sheldon Barry (2020):
# https://sheldonbarry.com/2020/05/04/blockchain-explained-using-python/
# Adapted for dictionary blocks and our calculate_hash function.
# Empty-chain and genesis-block checks added.

import json
from create_chain import calculate_hash


def verify_chain(chain):
    if not chain:
        print("The chain is empty.")
        return False

    first_block = chain[0]

    if first_block["previous_hash"] != "0" * 64:
        print("Genesis block has an incorrect previous hash.")
        return False

    if first_block["hash"] != calculate_hash(first_block):
        print("Genesis block hash does not match its contents.")
        return False

    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i - 1]

        if current_block["hash"] != calculate_hash(current_block):
            print("Block", current_block["number"],
                  "- content hash mismatch")
            return False

        if current_block["previous_hash"] != previous_block["hash"]:
            print("Block", current_block["number"],
                  "- previous hash mismatch")
            return False

    return True


def main():
    with open("chain.json", "r", encoding="utf-8") as file:
        chain = json.load(file)

    if verify_chain(chain):
        print("Chain verification: Accepted")
    else:
        print("Chain verification: Rejected")


if __name__ == "__main__":
    main()
