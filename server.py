import cv2
import numpy as np
from flask import Flask, Response, request
import threading
import time
import datetime

app = Flask(__name__)
current_frame = None
lock = threading.Lock()

# Resized dimensions
RESIZED_WIDTH = 1200
RESIZED_HEIGHT = 800

@app.route('/')
def home():
    return "Welcome to Video Streaming Server!!!"

@app.route('/video_feed', methods=['POST', 'GET'])
def video_feed():
    global current_frame

    if request.method == 'POST':
        try:
            # Receive frame data
            frame_data = request.data
            frame = np.frombuffer(frame_data, np.uint8)
            img = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            if img is None:
                print("Error decoding the frame")
                return "Invalid frame data", 400

            # Resize frame
            img = cv2.resize(img, (RESIZED_WIDTH, RESIZED_HEIGHT))

            # Simulate object detection or processing
            # (Placeholder for actual processing logic)
            start_time = time.time()
            time.sleep(0.01)  # Simulating processing delay
            processing_delay = time.time() - start_time
            print(f'Processing delay: {processing_delay:.4f} seconds')

            # Encode frame
            _, buffer = cv2.imencode('.jpg', img)
            with lock:
                current_frame = buffer.tobytes()

            print("Frame successfully updated in server")

            return "Frame received successfully", 200
        except Exception as e:
            print(f"Error processing frame: {e}")
            return "Error processing frame", 500

    elif request.method == 'GET':
        # Serve video stream
        return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate():
    global current_frame
    while True:
        with lock:
            if current_frame is not None:
                print(f"Serving frame at {datetime.datetime.now()}")  # Debug log
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')
            else:
                print("No frame available to serve")  # Debug log


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
