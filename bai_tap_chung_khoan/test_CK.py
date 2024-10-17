import time
from playwright.sync_api import sync_playwright

# Hàm cuộn trang xuống
def scroll_down(page, scroll_element_selector, step=50, max_height=300):
    scroll_position = 0
    while scroll_position < max_height:
        page.eval_on_selector(scroll_element_selector, f"el => el.scrollTop = {scroll_position}")
        scroll_position += step
        time.sleep(0.5)

# Sử dụng Playwright
with sync_playwright() as p:
    # Mở trình duyệt Edge hoặc Chromium (thay thế bằng 'firefox' nếu cần)
    browser = p.chromium.launch(headless=False)  # headless=False để xem quá trình chạy
    page = browser.new_page()

    # Mở trang web
    page.goto("https://iboard.ssi.com.vn/")

    # Đợi trang web tải
    time.sleep(10)

    # Tìm và cuộn xuống dần dần phần tử có class 'ag-body-viewport ag-layout-normal ag-row-animation scroll-base'
    scroll_down(page, ".ag-body-viewport.ag-layout-normal.ag-row-animation.scroll-base")

    # Tìm tất cả các phần tử có class 'ag-pinned-left-cols-container'
    elements = page.query_selector_all(".ag-pinned-left-cols-container")

    # Lấy và in ra nội dung của phần tử thứ hai (nếu có)
    if len(elements) >= 2:
        content = elements[1].inner_text()
        content_horizontal = content.replace("\n", ", ")
        print("Danh sách công ty:", content_horizontal)
    else:
        print("Không tìm thấy đủ phần tử.")

    # Đóng trình duyệt
    browser.close()
