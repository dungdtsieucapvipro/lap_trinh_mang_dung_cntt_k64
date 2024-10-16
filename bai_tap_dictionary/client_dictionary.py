import socket

def start_client():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        
        # Gửi từ tiếng Anh yêu cầu lên server
        word = input("Enter an English word: ")
        client_socket.sendall(word.encode())

        # Nhận phản hồi từ server
        response = client_socket.recv(4096).decode()
        print(f"Server response:\n{response}")

if __name__ == "__main__":
    start_client()
