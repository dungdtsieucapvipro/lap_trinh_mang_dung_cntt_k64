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

    # Cuộn xuống phần tử có class 'ag-body-viewport ag-layout-normal ag-row-animation scroll-base'
    scroll_down(page, ".ag-body-viewport.ag-layout-normal.ag-row-animation.scroll-base")

    # Cuộn xuống phần tử có class 'ag-center-cols-clipper'
    scroll_down(page, ".ag-center-cols-clipper")

    # Đợi một chút để đảm bảo nội dung đã được tải sau khi cuộn
    time.sleep(3)

    # Tìm tất cả các phần tử có class "ag-cell ag-cell-not-inline-editing ag-cell-normal-height ag-cell-color-ceil ag-cell-bg-highlight cursor-pointer"
    cells = page.query_selector_all(".ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-color-ceil.ag-cell-bg-highlight.cursor-pointer")

    if cells:
        for index, cell in enumerate(cells):
            content = cell.inner_text()  # Lấy nội dung của từng ô
            print(f"Nội dung ô TRAN thứ {index + 1}:", content)
    else:
        print("Không tìm thấy ô nào có class 'ag-cell ag-cell-not-inline-editing ag-cell-normal-height ag-cell-color-ceil ag-cell-bg-highlight cursor-pointer'.")

    # Đóng trình duyệt
    browser.close()