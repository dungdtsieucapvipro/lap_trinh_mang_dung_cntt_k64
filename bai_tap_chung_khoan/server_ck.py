import socket
from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_stock_info(stock_symbol):
    url = "https://eoddata.com/stocklist/NASDAQ/A.htm"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    data = []
    for row in soup.select('#ctl00_cph1_divSymbols table tr:has(td)'):
        d = dict(zip(soup.select_one('#ctl00_cph1_divSymbols table tr:has(th)').stripped_strings, row.stripped_strings))
        d.update({'url': 'https://eoddata.com' + row.a.get('href')})
        data.append(d)

    df = pd.DataFrame(data)

    # Tìm mã chứng khoán
    stock_info = df[df.eq(stock_symbol).any(axis=1)]
    return stock_info.to_string() if not stock_info.empty else "Stock symbol not found."


# Tạo socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen()

print('Server đang chờ kết nối...')

while True:
    conn, addr = server_socket.accept()
    print(f'Kết nối từ {addr}')
    
    # Nhận mã chứng khoán từ client
    stock_symbol = conn.recv(1024).decode()
    
    # Lấy thông tin mã chứng khoán
    result = get_stock_info(stock_symbol)
    
    # Gửi kết quả lại cho client
    conn.sendall(result.encode())
    conn.close()
