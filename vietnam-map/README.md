# Việt Nam Atlas — chạy local

Trang web bản đồ tương tác, ghép từ 34 tệp SVG và danh sách CSV trong thư mục `../data`.

## Mở trang web

Nhấp đúp `start-local.cmd`. Trình duyệt sẽ mở `http://127.0.0.1:4173/`. Giữ cửa sổ máy chủ mở trong lúc dùng; nhấn Ctrl+C để dừng.

Bạn cũng có thể mở trực tiếp `index.html` hoặc `dist/index.html` bằng trình duyệt hay Live Server. Trang đã chứa toàn bộ hình học và dữ liệu, không cần cài thư viện. Phông Google Fonts là tùy chọn; khi ngoại tuyến trang dùng Arial.

Để chạy bằng máy chủ cục bộ:

```powershell
python serve.py
```

Truy cập `http://127.0.0.1:4173`. Nếu cổng đang được dùng, chạy `python serve.py --port 4174`. Nếu tab cũ vẫn trống, nhấn Ctrl+F5.

## Tương tác

- Rê chuột lên tỉnh/thành để nâng vùng đất, đổi màu, đổ bóng và hiện tên.
- Nhấn vào bản đồ hoặc danh sách để giữ lựa chọn; nhấn lại, chọn “Bỏ chọn”, hoặc nhấn Escape để bỏ chọn.
- Tìm tên địa phương có dấu hoặc không dấu.
- Dùng nút điều khiển để ẩn/hiện tên, phóng to, thu nhỏ và đặt lại.
- Trên thiết bị cảm ứng, chạm để chọn. Bàn phím hỗ trợ Tab, Enter và Space. Tôn trọng thiết lập giảm chuyển động của thiết bị.

## Chỉnh sửa

Chỉnh giao diện trong `template.html.in`, rồi chạy `python build.py`. Trình dựng đọc dữ liệu gốc tại `../data` và tạo cả `index.html` lẫn `dist/index.html`. Các đường viền được giữ theo tọa độ trong SVG gốc; các ký hiệu đánh dấu màu nâu được bỏ khỏi lớp ranh giới.

Tệp `template.html` cũ tự chuyển đến trang hoàn chỉnh để tránh mở nhầm bản mẫu không có dữ liệu. Bản đồ và danh sách tỉnh được nhúng sẵn trong HTML; hiệu ứng rê chuột cơ bản hoạt động bằng CSS.

Đây là bản đồ tương tác tích hợp đầy đủ không gian địa lý, các thực thể đảo và dữ liệu chuyên sâu của 34 tỉnh thành cùng hai quần đảo Hoàng Sa (Đặc khu Hoàng Sa thuộc TP. Đà Nẵng) và Trường Sa (huyện Trường Sa thuộc tỉnh Khánh Hòa) dựa trên các tài liệu tổng hợp năm 2025-2026.

## Kiểm tra đã thực hiện

Đủ 36 đối tượng độc lập (34 tỉnh thành và 2 quần đảo Hoàng Sa, Trường Sa), cú pháp JavaScript hợp lệ, kiểm tra xử lý rê chuột, tìm kiếm có dấu / không dấu, chọn/bỏ chọn, bàn phím, phóng to/thu nhỏ, tên địa phương và đặt lại. Trang chi tiết (province.html) hỗ trợ đầy đủ 36 thực thể với số liệu thống kê, bài viết chuyên sâu về vị trí địa lý, căn cứ lịch sử - pháp lý, quốc phòng - an ninh và tiềm năng kinh tế biển.
