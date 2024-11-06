import socket

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12347))

    n = input("nhap so nguyen n: ").strip()
    client_socket.send(n.encode())

    result = client_socket.recv(1024).decode()
    print(f"Binh phuong cua {n} la: {result}")

    client_socket.close()

if __name__ == "__main__":
    client_program()
