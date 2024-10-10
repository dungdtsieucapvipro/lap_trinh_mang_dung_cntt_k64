import socket
from playwright.sync_api import sync_playwright

def fetch_definition(url):
    with sync_playwright() as p:
        # Mở trình duyệt
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Truy cập URL với thời gian timeout cao hơn
            page.goto(url, wait_until="load", timeout=60000)  # Thay đổi timeout thành 60 giây
            
            # Lấy nội dung của thẻ định nghĩa tiếng Anh (div.def ddef_d db)
            english_definition = page.locator("div.def.ddef_d.db").inner_text()
            
            # Lấy nội dung của thẻ định nghĩa tiếng Việt (span.trans.dtrans)
            vietnamese_translation = page.locator("span.trans.dtrans").inner_text()
        except Exception as e:
            print(f"Error while fetching definition: {e}")
            return None, None
        finally:
            browser.close()
        
        return english_definition, vietnamese_translation


def extract_word_from_url(word):
    # Tạo URL từ từ tiếng Anh
    base_url = "https://dictionary.cambridge.org/vi/dictionary/english-vietnamese/"
    return base_url + word

def start_server():
    host = '127.0.0.1'
    port = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server is listening on {host}:{port}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                
                try:
                    # Tạo URL từ từ tiếng Anh
                    url = extract_word_from_url(data.strip())
                    
                    # Truy cập URL mà client yêu cầu
                    english_definition, vietnamese_translation = fetch_definition(url)
                    
                    # Chuẩn bị phản hồi với từ cuối cùng từ URL
                    response = (
                        f"Word: {data.strip()}\n"  # Thêm từ cuối cùng của URL (ví dụ: hello)
                        f"English definition: {english_definition}\n"
                        f"Vietnamese translation: {vietnamese_translation}"
                    )
                except Exception as e:
                    response = f"Error fetching definition: {str(e)}"
                
                conn.sendall(response.encode())

if __name__ == "__main__":
    start_server()
