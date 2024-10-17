import socket
import json

def fetch_data_from_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = b""
        while True:
            packet = s.recv(1024)
            if not packet:
                break
            data += packet
            if b"<END>" in data:
                break
        data = data.replace(b"<END>", b"")
        return json.loads(data.decode('utf-8'))

if __name__ == "__main__":
    data = fetch_data_from_server()
    print("Dữ liệu nhận được từ server:")
    for item in data:
        print(f"Mã chứng khoán: {item['stock_code']}, Giá trần: {item['ceiling_price']}, Giá sàn: {item['floor_price']}, Giá TC: {item['tc_price']}")
