import socket
import threading


def calculate_golden_ratio_sequence(a):
    # Golden ratio constant
    golden_ratio = 1.61803398875
    sequence = [0] * 20

    # Determine the scaling factor based on the 10th number being A
    sequence[9] = a
    scaling_factor = a / (golden_ratio ** 9)

    # Generate the rest of the sequence
    for i in range(9):
        sequence[i] = scaling_factor * (golden_ratio ** i)
    for i in range(10, 20):
        sequence[i] = scaling_factor * (golden_ratio ** i)

    return sequence


def handle_client(client_socket):
    try:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            a = float(data)  # Convert received data to float
            result = calculate_golden_ratio_sequence(a)
            result_str = ','.join(map(str, result))
            client_socket.send(result_str.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()