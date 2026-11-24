#Tests informed by Sheldon Barry (2020):
# https://sheldonbarry.com/2020/05/04/blockchain-explained-using-python/
# Full-chain rebuilding and results-table output added for this project.

import copy
import json

from create_chain import calculate_hash
from verify_chain import verify_chain


def main():
    with open("chain.json", "r", encoding="utf-8") as file:
        original = json.load(file)

    # Check the baseline before testing any changes.
    if not verify_chain(original):
        print("Original chain is invalid. Check it before continuing.")
        return

    results = []

    def run_test(name, chain, expected):
        print("\nChecking:", name)

        if verify_chain(chain):
            actual = "Accepted"
        else:
            actual = "Rejected"

        print("Result:", actual)
        results.append((name, expected, actual))

    # Test 1: unchanged chain.
    run_test("Original chain", original, "Accepted")

    # Test 2: change the middle block's message.
    changed = copy.deepcopy(original)
    changed[1]["message"] = "Alice sends Bob 100 tokens"

    run_test("Edited message", changed, "Rejected")

    # Test 3: update only the changed block's stored hash.
    one_hash_updated = copy.deepcopy(changed)
    one_hash_updated[1]["hash"] = calculate_hash(one_hash_updated[1])

    run_test("Updated middle hash", one_hash_updated, "Rejected")

    # Test 4: rebuild the affected links and hashes.
    rebuilt = copy.deepcopy(one_hash_updated)

    for i in range(1, len(rebuilt)):
        rebuilt[i]["previous_hash"] = rebuilt[i - 1]["hash"]
        rebuilt[i]["hash"] = calculate_hash(rebuilt[i])

    run_test("Rebuilt chain", rebuilt, "Accepted")

    print("\n{:<25} {:<12} {:<12}".format(
        "Test", "Expected", "Actual"
    ))

    for name, expected, actual in results:
        print("{:<25} {:<12} {:<12}".format(
            name, expected, actual
        ))


if __name__ == "__main__":
    main()
              