import socket
import threading

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def find_primes_in_range(a, b):
    return [x for x in range(a, b + 1) if is_prime(x)]

#! TCP - Tuần tự Server
def tcp_sequential_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12346))
    server_socket.listen(5)
    print("TCP Tuần tự Server đang lắng nghe trên cổng 12346...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Kết nối từ {client_address} đã được thiết lập.")
        data = client_socket.recv(1024).decode()
        a, b = map(int, data.split())

        primes = find_primes_in_range(a, b)
        response = " ".join(map(str, primes))

        client_socket.send(response.encode())
        client_socket.close()

#! TCP - Song Song Server
def tcp_parallel_server():
    def handle_client(client_socket, client_address):
        print(f"Kết nối từ {client_address} đã được thiết lập.")
        data = client_socket.recv(1024).decode()
        a, b = map(int, data.split())

        primes = find_primes_in_range(a, b)
        response = " ".join(map(str, primes))

        client_socket.send(response.encode())
        client_socket.close()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12347))
    server_socket.listen(5)
    print("TCP Song Song Server đang lắng nghe trên cổng 12347...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

#! UDP - Tuần tự Server
def udp_sequential_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 12348))
    print("UDP Tuần tự Server đang lắng nghe trên cổng 12348...")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        a, b = map(int, data.decode().split())

        primes = find_primes_in_range(a, b)
        response = " ".join(map(str, primes))

        server_socket.sendto(response.encode(), client_address)

#! UDP - Song Song Server
def udp_parallel_server():
    def handle_client(data, client_address, server_socket):
        print(f"Kết nối từ {client_address} đã được thiết lập.")
        a, b = map(int, data.decode().split())

        primes = find_primes_in_range(a, b)
        response = " ".join(map(str, primes))

        server_socket.sendto(response.encode(), client_address)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 12349))
    print("UDP Song Song Server đang lắng nghe trên cổng 12349...")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        client_handler = threading.Thread(target=handle_client, args=(data, client_address, server_socket))
        client_handler.start()

#! Main function to call different servers
def main():
    choice = input("Chọn chế độ server (1: TCP tuần tự, 2: TCP song song, 3: UDP tuần tự, 4: UDP song song): ")
    if choice == '1':
        tcp_sequential_server()
    elif choice == '2':
        tcp_parallel_server()
    elif choice == '3':
        udp_sequential_server()
    elif choice == '4':
        udp_parallel_server()
    else:
        print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
