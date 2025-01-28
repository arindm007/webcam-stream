import cv2
import requests
import time
import datetime

# Define the server URL
SERVER_URL = 'http://127.0.0.1:8080/video_feed'

# Initialize the webcam
camera = cv2.VideoCapture(0)

# Set the desired webcam resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frames_sent_to_server = 0

try:
    print('Connected to Cache Server.')

    while True:
        # Capture a frame from the webcam
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        # Resize the frame
        frame_resized = cv2.resize(frame, (320, 240))

        # Convert the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame_resized)
        frame_data = buffer.tobytes()

        # Prepare headers
        headers = {
            'Content-Type': 'application/octet-stream',
            'Frame-Width': str(frame_resized.shape[1]),
            'Frame-Height': str(frame_resized.shape[0]),
            'Client-Timestamp': str(time.time())
        }

        # Send the frame to the server
        start_time = time.time()
        try:
            response = requests.post(SERVER_URL, data=frame_data, headers=headers)
            response.raise_for_status()
            print(f'Frame sent to server: {response.status_code}')
        except requests.RequestException as e:
            print(f"Failed to send frame: {e}")
        end_time = time.time()

        # Calculate and display delay
        delay = end_time - start_time
        print(f'Delay time (client to server): {delay:.4f} seconds')

        frames_sent_to_server += 1
        print(f"Frame count: {frames_sent_to_server}")

        # Display the frame being transmitted
        # cv2.imshow("TRANSMITTING TO CACHE SERVER", frame_resized)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    # Release the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()

print(f"Total frames sent to server: {frames_sent_to_server}")
