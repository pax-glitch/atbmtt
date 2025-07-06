Gửi bài tập chia thành nhiều phần 📚 Dự án này triển khai một hệ thống truyền dữ liệu an toàn bằng Python, bao gồm cơ chế gửi và nhận dữ liệu với việc tạo khóa mã hóa để đảm bảo bảo mật. Ứng dụng cho phép tạo khóa mã hóa, gửi dữ liệu đã mã hóa và nhận/giải mã dữ liệu thông qua giao diện dòng lệnh đơn giản. 🚀 📖 Tổng quan dự án Dự án bao gồm bốn file Python chính:

generate_keys.py: Tạo cặp khóa công khai và riêng tư để mã hóa và giải mã. 🔑 sender.py: Xử lý mã hóa và gửi dữ liệu. 📤 receiver.py: Nhận và giải mã dữ liệu. 📥 app.py: File chính để chạy ứng dụng, điều phối giữa sender và receiver. ⚙️

Hệ thống này thể hiện một cách triển khai cơ bản của truyền thông an toàn, phù hợp để học tập hoặc mở rộng cho các trường hợp phức tạp hơn. ✨ Tính năng

Tạo khóa: Tạo cặp khóa công khai/riêng tư để mã hóa và giải mã. 🔒 Mã hóa dữ liệu: Mã hóa dữ liệu trước khi gửi (xử lý bởi sender.py). 🛡️ Giải mã dữ liệu: Giải mã dữ liệu nhận được để lấy lại thông điệp gốc (xử lý bởi receiver.py). 🔓 Giao diện dòng lệnh: Giao diện CLI đơn giản để tương tác thông qua app.py. 💻 Thiết kế mô-đun: Tách biệt logic tạo khóa, gửi và nhận dữ liệu để dễ bảo trì. 🧩

🛠️ Yêu cầu cài đặt

Python 3.8 trở lên 🐍 Thư viện Python cần thiết: cryptography (dùng cho tạo khóa và mã hóa)

Terminal hoặc giao diện dòng lệnh 💻

🔧 Hướng dẫn cài đặt

Cài đặt các thư viện cần thiết: pip install cryptography

🚀 Hướng dẫn sử dụng

Tạo khóa:Chạy script tạo khóa để sinh cặp khóa công khai/riêng tư: python generate_keys.py

Script này sẽ tạo các khóa cần thiết cho mã hóa và giải mã. 🔑

Chạy ứng dụng:Chạy script chính để khởi động sender và receiver: python app.py

Làm theo hướng dẫn trên màn hình để gửi hoặc nhận dữ liệu. 📬

Quy trình mẫu:

Chạy generate_keys.py để tạo khóa. 🔑 Sử dụng app.py để gửi tin nhắn từ sender đến receiver. 📤 Receiver sẽ giải mã và hiển thị tin nhắn. 📥

Ảnh sản phẩm:

Giao diện mã hóa ( gửi file và khóa ) :

![guifile](https://github.com/user-attachments/assets/633d3053-9082-480c-97d2-5107546899d3)

Giao diện nhận và giải mã :

![nhanfile](https://github.com/user-attachments/assets/00d3de1f-1225-492c-bcfd-10115bb98a99)

Giao diện hoàn thành và thông báo :
* Mã hòa và gửi:
* 
![guifillethanhcong](https://github.com/user-attachments/assets/9d67b3b6-5509-4a96-863a-11fbbccce580)
* Nhận và giải mã:
* 
![giaimathanhcong](https://github.com/user-attachments/assets/51b8d9b5-aaf9-4d2b-8ba9-917fd9424624)
* kết quả sau khi giải mã:
* 
![ketqua](https://github.com/user-attachments/assets/14c6960d-c8cc-4786-9a6d-841849cd1030)

