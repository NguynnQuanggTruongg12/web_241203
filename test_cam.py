from flask import Flask, Response
import cv2

app = Flask(__name__)

# Mở camera (0 là camera mặc định, hoặc thay bằng đường dẫn camera IP)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Đọc frame từ camera
        success, frame = camera.read()
        if not success:
            break
        else:
            # Mã hóa frame thành JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Tạo luồng video
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Trả về luồng video
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>IP Camera</title>
    </head>
    <body>
        <h1>Live Video Stream</h1>
        <img src="/video_feed" width="720" />
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
