import cv2
import numpy as np
from flask import Flask, Response, request
import threading
import time
import datetime

app = Flask(__name__)
current_frame = None
frame_count_client = 0
frame_count_server = 0

# Specify the desired dimensions for the resized frames
RESIZED_WIDTH = 1200
RESIZED_HEIGHT = 800

@app.route('/')
def home():
    return "Welcome to Video Streaming Server!!!"

@app.route('/video_feed', methods=['POST', 'GET'])
def video_feed():
    global current_frame, frame_count_client, frame_count_server

    if request.method == 'POST':
        try:
            frame_data = request.data
            frame = np.frombuffer(frame_data, np.uint8)
            img = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            frame_width = int(request.headers.get('Frame-Width', RESIZED_WIDTH))
            frame_height = int(request.headers.get('Frame-Height', RESIZED_HEIGHT))
            client_timestamp = float(request.headers.get('Client-Timestamp', time.time()))

            server_to_client_delay = time.time() - client_timestamp
            print(f'Delay time (client to server): {server_to_client_delay:.4f} seconds')

            img = cv2.resize(img, (RESIZED_WIDTH, RESIZED_HEIGHT))

            # Placeholder for processing (e.g., object detection)
            start_time = time.time()
            # results = model.predict(img)
            end_time = time.time()
            processing_delay = end_time - start_time
            print(f'Processing delay: {processing_delay:.4f} seconds')

            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print(f'Frame received by server at: {current_time}')

            # Simulate object detection results for demonstration
            # Replace this with actual processing logic
            results = []  # Empty list to indicate no detection for now

            for result in results:
                for obj in result.boxes:
                    x1, y1, x2, y2 = map(int, obj.xyxy[0])
                    label = result.names[int(obj.cls[0])]
                    confidence = obj.conf[0]

                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, f'{label}: {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', img)
            current_frame = buffer.tobytes()

            frame_count_client += 1
            frame_count_server += 1
            print(f"Received frame from client. Total frames received: {frame_count_client}")
            print(f"Total frames processed: {frame_count_server}")

            server_timestamp = time.time()
            server_to_browser_delay = server_timestamp - client_timestamp
            print(f'Delay time (server to browser URL): {server_to_browser_delay:.4f} seconds')

            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print(f'Frame sent to browser at: {current_time}')

            return "Video frame received."
        except Exception as e:
            print(f"Error processing frame: {e}")
            return "Error processing frame.", 500
    else:
        return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate():
    global current_frame
    while True:
        if current_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')

def process_frame():
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    threading.Thread(target=process_frame, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
