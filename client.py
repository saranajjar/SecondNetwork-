import socket
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))  # Replace 'localhost' with the server's IP if running remotely
    # Login
    account_number = input("Enter your account number: ")
    password = input("Enter your password: ")
    login_request = f"LOGIN {account_number} {password}"
    client.send(login_request.encode())
    response = client.recv(1024).decode()
    print(response)
    # If authenticated, allow banking operations
    if response == "Authenticated":
        while True:
            print("\nChoose operation:")
            print("1. Check balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Exit")
            choice = input("Enter choice: ")
            if choice == '1':
                client.send(f"BALANCE {account_number}".encode())
                balance_response = client.recv(1024).decode()
                print(balance_response)
            elif choice == '2':
                amount = input("Enter amount to deposit: ")
                client.send(f"DEPOSIT {account_number} {amount}".encode())
                deposit_response = client.recv(1024).decode()
                print(deposit_response)
            elif choice == '3':
                amount = input("Enter amount to withdraw: ")
                client.send(f"WITHDRAW {account_number} {amount}".encode())
                withdraw_response = client.recv(1024).decode()
                print(withdraw_response)
            elif choice == '4':
                client.send("EXIT".encode())
                final_balance_response = client.recv(1024).decode()
                print(final_balance_response)
                break
            else:
                print("Invalid choice")
    else:
        print("Authentication failed")
    client.close()
if __name__ == "__main__":
    main()
