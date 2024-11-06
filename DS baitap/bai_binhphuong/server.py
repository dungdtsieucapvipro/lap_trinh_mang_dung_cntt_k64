import socket
import threading

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode()
        n = int(data)
        # Tính bình phương
        result = n ** 2
        client_socket.send(str(result).encode())
    except ValueError:
        client_socket.send("Loi: Dau vao khong hop le".encode())
    finally:
        client_socket.close()

def start_server(mode="sequential"):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12347))  # Đổi sang cổng 12346
    server_socket.listen(5)
    print("Server dang lang nghe o port 12347...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"chap nhan ket noi tu {addr}")

        if mode == "sequential":
            handle_client(client_socket)
        elif mode == "parallel":
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    mode = input("nhap kieu (sequential/parallel): ").strip().lower()
    start_server(mode=mode)
