import socket

def start_client():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        
        # Gửi URL yêu cầu lên server
        url = "https://dictionary.cambridge.org/vi/dictionary/english-vietnamese/hello"
        client_socket.sendall(url.encode())

        # Nhận phản hồi từ server
        response = client_socket.recv(4096).decode()
        print(f"Server response: {response}")

if __name__ == "__main__":
    start_client()
