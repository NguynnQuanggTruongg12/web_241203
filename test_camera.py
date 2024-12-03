import time
from flask import Flask, render_template, Response
import cv2
app=Flask(__name__)
camera=cv2.VideoCapture("/dev/video0")
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)  # Đặt chiều rộng khung hình
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)  # Đặt chiều cao khung hình
from pyngrok import ngrok
import requests
import threading

def generate_frames():
    while True:
        # Đọc khung hình từ camera
        success, frame = camera.read()
        if not success:
            break

        # Chuyển đổi khung hình thành dạng JPEG
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY),15])
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

def print_a():
     app.run(debug=False, port=5050)
def print_b():
    ngrok.set_auth_token("2enpisT7VAgTzuWFQtoO0VXxxMO_5rddLzyqJ9WWd5TCrbR1s")
    if ngrok.get_ngrok_process():
        print("Đóng kết nối ngrok hiện tại...")
        ngrok.kill()
    ngrok_tunnel = ngrok.connect("http://127.0.0.1:5050")
    public_url = ngrok_tunnel.public_url
    print("Kết nối đã tạo:", public_url)
    try:
        try:
            url_post_link = 'https://optimarobotics.com/Library_Robot_V1/post_link_ngrok.php'
            data = {'content': public_url}
            response = requests.post(url_post_link, data=data)
            print("send thanh cong try", response)
        except Exception as e:
            print("error", e)
            url_post_link = 'https://optimarobotics.com/Library_Robot_V1/post_link_ngrok.php'
            data = {'content': public_url}
            response = requests.post(url_post_link, data=data)
            print("send thanh cong try", response)
        print('url gui len duoc', public_url)
        input("Nhấn Enter để dừng kết nối ngrok...")
    finally:
        ngrok.kill()

if __name__=="__main__":
    thread_a = threading.Thread(target=print_a)
    thread_b = threading.Thread(target=print_b)
    thread_a.start()
    time.sleep(2)
    thread_b.start()
    thread_a.join()
    thread_b.join()
    print("Both threads have finished.")


