import socket

def run_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Server listening on {host}:{port}...")

    conn, addr = s.accept()
    print(f"Connection from {addr}")

    try:
        data = conn.recv(1024)
        print(f"Received data: {data.decode()}")
        conn.sendall(b"Message received!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345
    run_server(host, port)
