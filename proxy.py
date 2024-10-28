import socket
from cryptography.fernet import Fernet

# Load the Fernet key
def load_key(filename="fernet.key"):
    with open(filename, "rb") as key_file:
        return key_file.read()

cipher = Fernet(load_key())

def start_proxy_server(proxy_host='127.0.0.1', proxy_port=8888, server_host='127.0.0.1', server_port=12345):
    print(f"Proxy server starting on {proxy_host}:{proxy_port}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy:
        proxy.bind((proxy_host, proxy_port))
        proxy.listen(1)

        while True:
            conn, addr = proxy.accept()
            print(f"[Proxy] Connected by {addr}")
            with conn:
                encrypted_data = conn.recv(1024)
                try:
                    # Decrypt and display the message
                    decrypted_message = cipher.decrypt(encrypted_data).decode()
                    print(f"[Proxy] Decrypted message from client: {decrypted_message}")

                    # Forward the message to the server and get the response
                    server_response = forward_to_server(decrypted_message, server_host, server_port)
                    conn.sendall(server_response)
                except Exception as e:
                    print(f"[Proxy] Decryption error: {e}")
                    conn.sendall(b"Decryption failed.")

def forward_to_server(message, server_host, server_port):
    print(f"[Proxy] Forwarding message to server: {message}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((server_host, server_port))
        server.sendall(message.encode())
        response = server.recv(1024)  # Receive response from server
    print(f"[Proxy] Received response from server: {response.decode()}")
    return response

if __name__ == "__main__":
    start_proxy_server()
