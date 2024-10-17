import socket
import time
import json
from playwright.sync_api import sync_playwright

# Hàm cuộn trang xuống
def scroll_down(page, scroll_element_selector, step=50, max_height=300):
    scroll_position = 0
    while scroll_position < max_height:
        page.eval_on_selector(scroll_element_selector, f"el => el.scrollTop = {scroll_position}")
        scroll_position += step
        time.sleep(0.5)

# Hàm chạy Playwright và lấy dữ liệu
def fetch_stock_data():
    with sync_playwright() as p:
        # Mở trình duyệt Edge hoặc Chromium (thay thế bằng 'firefox' nếu cần)
        browser = p.chromium.launch(headless=False)  # headless=False để xem quá trình chạy
        page = browser.new_page()

        # Mở trang web
        page.goto("https://iboard.ssi.com.vn/")

        # Đợi trang web tải
        time.sleep(10)

        # Cuộn xuống phần tử có class 'ag-body-viewport ag-layout-normal ag-row-animation scroll-base'
        scroll_down(page, ".ag-body-viewport.ag-layout-normal.ag-row-animation.scroll-base")

        # Cuộn xuống phần tử có class 'ag-center-cols-clipper'
        scroll_down(page, ".ag-center-cols-clipper")

        # Đợi một chút để đảm bảo nội dung đã được tải sau khi cuộn
        time.sleep(3)

        # Tìm và lấy danh sách mã chứng khoán
        elements = page.query_selector_all(".ag-pinned-left-cols-container")
        stock_codes = []
        if len(elements) >= 2:
            content = elements[1].inner_text()
            stock_codes = content.split("\n")  # Chia danh sách mã chứng khoán thành các phần tử
        else:
            print("Không tìm thấy đủ phần tử.")

        # Tìm tất cả các phần tử cho giá trần
        ceiling_cells = page.query_selector_all(".ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-color-ceil.ag-cell-bg-highlight.cursor-pointer")

        # Tìm tất cả các phần tử cho giá sàn
        floor_cells = page.query_selector_all(".ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-color-floor.ag-cell-bg-highlight.cursor-pointer.ag-cell-value")

        # Tìm tất cả các phần tử cho giá TC
        tc_cells = page.query_selector_all(".ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-color-ref.ag-cell-bg-highlight.cursor-pointer.ag-cell-value")

        # Lấy giá từ các ô giá trần
        ceiling_prices = []
        if ceiling_cells:
            for cell in ceiling_cells:
                content = cell.inner_text()  # Lấy nội dung của từng ô
                ceiling_prices.append(content)  # Thêm vào danh sách giá trần
        else:
            print("Không tìm thấy ô nào cho giá trần.")

        # Lấy giá từ các ô giá sàn
        floor_prices = []
        if floor_cells:
            for cell in floor_cells:
                content = cell.inner_text()  # Lấy nội dung của từng ô
                floor_prices.append(content)  # Thêm vào danh sách giá sàn
        else:
            print("Không tìm thấy ô nào cho giá sàn.")

        # Lấy giá từ các ô giá TC
        tc_prices = []
        if tc_cells:
            for cell in tc_cells:
                content = cell.inner_text()  # Lấy nội dung của từng ô
                tc_prices.append(content)  # Thêm vào danh sách giá TC
        else:
            print("Không tìm thấy ô nào cho giá TC.")

        # Đóng trình duyệt
        browser.close()

        # Trả về kết quả
        result = []
        for i in range(min(len(stock_codes), len(ceiling_prices), len(floor_prices), len(tc_prices))):
            result.append({
                "stock_code": stock_codes[i],
                "ceiling_price": ceiling_prices[i],
                "floor_price": floor_prices[i],
                "tc_price": tc_prices[i]
            })
        return result

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server đang lắng nghe trên {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print('Kết nối từ', addr)
                data = conn.recv(1024).decode('utf-8')
                if data:
                    stock_code = data.strip()
                    stock_data = fetch_stock_data()
                    if stock_code == "ALL":
                        json_data = json.dumps(stock_data) + "<END>"
                    else:
                        result = next((item for item in stock_data if item["stock_code"] == stock_code), None)
                        if result:
                            json_data = json.dumps(result) + "<END>"
                        else:
                            json_data = json.dumps({"error": "Stock code not found"}) + "<END>"
                    conn.sendall(json_data.encode('utf-8'))

if __name__ == "__main__":
    start_server()
