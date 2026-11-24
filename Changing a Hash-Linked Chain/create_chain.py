import hashlib
import json


def calculate_hash(block):
    # Leave out the stored hash when calculating a new one.
    block_data = {
        "number": block["number"],
        "message": block["message"],
        "previous_hash": block["previous_hash"]
    }

    # Always use the same field order and spacing.
    block_text = json.dumps(
        block_data,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(block_text.encode("utf-8")).hexdigest()


def create_chain():
    chain = []

    messages = [
        "Genesis block",
        "Alice sends Bob 10 tokens",
        "End of demonstration"
    ]

    previous_hash = "0" * 64

    for i in range(len(messages)):
        block = {
            "number": i + 1,
            "message": messages[i],
            "previous_hash": previous_hash
        }

        block["hash"] = calculate_hash(block)
        chain.append(block)

        # The next block will refer to this block's hash.
        previous_hash = block["hash"]

    return chain


def main():
    chain = create_chain()

    with open("chain.json", "w", encoding="utf-8") as file:
        json.dump(chain, file, indent=4)

    for block in chain:
        print("\nBlock:", block["number"])
        print("Message:", block["message"])
        print("Previous hash:", block["previous_hash"])
        print("Current hash:", block["hash"])

    print("\nChain saved to chain.json")


if __name__ == "__main__":
    main()
                         