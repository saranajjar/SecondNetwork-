import socket
import threading
# Bank account details
accounts = {
    '123456': {'balance': 1000, 'password': 'pass123'},
    '789012': {'balance': 500, 'password': 'pass456'}
}
# Function to handle client requests
def handle_client(client_socket):
    while True:
        # Receive client request
        request = client_socket.recv(1024).decode()
        
        # Parse request
        req_parts = request.split()
        command = req_parts[0]
        
        # Authenticate client
        if command == 'LOGIN':
            account_number = req_parts[1]
            password = req_parts[2]
            if account_number in accounts and accounts[account_number]['password'] == password:
                client_socket.send("Authenticated".encode())
            else:
                client_socket.send("Invalid credentials".encode())
        # Check balance
        elif command == 'BALANCE':
            account_number = req_parts[1]
            balance = accounts[account_number]['balance']
            client_socket.send(f"Balance: {balance}".encode())
        # Deposit
        elif command == 'DEPOSIT':
            account_number = req_parts[1]
            amount = int(req_parts[2])
            accounts[account_number]['balance'] += amount
            client_socket.send("Deposit successful".encode())
        # Withdraw
        elif command == 'WITHDRAW':
            account_number = req_parts[1]
            amount = int(req_parts[2])
            if accounts[account_number]['balance'] >= amount:
                accounts[account_number]['balance'] -= amount
                client_socket.send("Withdrawal successful".encode())
            else:
                client_socket.send("Insufficient funds".encode())
        # Close connection
        elif command == 'EXIT':
            break
    # Send final balance and close connection
    client_socket.send(f"Final balance: {accounts[account_number]['balance']}".encode())
    client_socket.close()
# Main function to start the server
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server started")
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
if __name__ == "__main__":
    main()
