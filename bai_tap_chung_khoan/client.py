import socket
import json

def fetch_data_from_server(option, stock_code=None, host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        if option == 1 and stock_code:
            s.sendall(stock_code.encode('utf-8'))
        else:
            s.sendall("ALL".encode('utf-8'))
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
    print("Chọn tùy chọn:")
    print("1. Nhập mã chứng khoán bất kỳ")
    print("2. Lấy tất cả thông tin về chứng khoán")
    option = int(input("Nhập lựa chọn (1 hoặc 2): "))

    if option == 1:
        stock_code = input("Nhập mã chứng khoán: ")
        data = fetch_data_from_server(option, stock_code)
        if "error" in data:
            print(data["error"])
        else:
            print("Dữ liệu nhận được từ server:")
            print(f"Mã chứng khoán: {data['stock_code']}, Giá trần: {data['ceiling_price']}, Giá sàn: {data['floor_price']}, Giá TC: {data['tc_price']}")
    elif option == 2:
        data = fetch_data_from_server(option)
        print("Dữ liệu nhận được từ server:")
        for item in data:
            print(f"Mã chứng khoán: {item['stock_code']}, Giá trần: {item['ceiling_price']}, Giá sàn: {item['floor_price']}, Giá TC: {item['tc_price']}")
    else:
        print("Lựa chọn không hợp lệ")
