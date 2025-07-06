from flask import Flask, render_template, redirect, flash, request
from sender import send
from receiver import receive

app = Flask(__name__)
app.secret_key = 'my_super_secret_key'

# Trang chính, cho phép GET và POST để tránh lỗi 405 nếu form gửi sai
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

# Trang người gửi
@app.route('/sender', methods=['GET'])
def sender_page():
    return render_template("sender.html")

# Trang người nhận
@app.route('/receiver', methods=['GET'])
def receiver_page():
    return render_template("receiver.html")

# Xử lý gửi file
@app.route('/send', methods=['POST'])
def send_file():
    return send(request)

# Xử lý nhận file
@app.route('/receive', methods=['POST'])
def receive_file():
    return receive(request)

if __name__ == '__main__':
    app.run(debug=True)
