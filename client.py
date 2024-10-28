import socket
from cryptography.fernet import Fernet

# Load the encryption key
def load_key(filename="fernet.key"):
    with open(filename, "rb") as key_file:
        return key_file.read()

cipher = Fernet(load_key())

def connect_to_proxy(proxy_host, proxy_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((proxy_host, proxy_port))
            
            # Get message from user input
            message = input("Enter the message to send to the server: ")
            print(f"[Client] Message to send: {message}")
            
            # Encrypt the message
            encrypted_message = cipher.encrypt(message.encode())
            print(f"[Client] Sending encrypted message: {encrypted_message}")

            # Send the encrypted message to the proxy
            s.sendall(encrypted_message)

            # Receive and display response from the proxy
            response = s.recv(1024)
            print(f"[Client] Server response: {response.decode()}")

    except Exception as e:
        print(f"[Client] Connection error: {e}")

if __name__ == "__main__":
    proxy_host = '127.0.0.1'
    proxy_port = 8888
    connect_to_proxy(proxy_host, proxy_port)
