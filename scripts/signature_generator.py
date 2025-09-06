import hashlib

SECRET_KEY = "super_secret_key_for_signatures"  # .env


def get_input(prompt, type_func=str):
    while True:
        try:
            return type_func(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please try again.")


def main():
    print("=== Transaction Signature Generator ===\n")
    account_id = get_input("Enter account ID (integer): ", int)
    user_id = get_input("Enter user ID (integer): ", int)
    amount = get_input("Enter amount (number): ", int)
    transaction_id = input("Enter transaction ID (UUID): ").strip()
    data_string = f"{account_id}{amount}{transaction_id}{user_id}{SECRET_KEY}"
    signature = hashlib.sha256(data_string.encode()).hexdigest()
    print("\n=== Signature Generated ===")
    print(f"Account ID     : {account_id}")
    print(f"User ID        : {user_id}")
    print(f"Amount         : {amount}")
    print(f"Transaction ID : {transaction_id}")
    print(f"Signature      : {signature}")
    print("============================")


if __name__ == "__main__":
    main()
