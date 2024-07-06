import cv2
import torch
import requests
import numpy as np
from torchvision import transforms
from datetime import datetime

import sys
sys.path.append('/home/anano/moses/Defector3D/yolov5')


from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression

MODEL_PATH = './defector.pt'
# Load your PyTorch model

model = attempt_load(MODEL_PATH)

model.eval()


def preprocess_frame(frame):
    # Convert frame to RGB (OpenCV uses BGR by default)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert to tensor
    frame_tensor = torch.from_numpy(frame_rgb).float()
    
    # Normalize the tensor
    frame_tensor /= 255.0
    
    # Reorder dimensions to CxHxW
    frame_tensor = frame_tensor.permute(2, 0, 1).unsqueeze(0)
    
    return frame_tensor


def detect_defect(frame):
    img = preprocess_frame(frame)
    
    device = next(model.parameters()).device
    img = img.to(device)

    # Model inference
    with torch.no_grad():
        pred = model(img)[0]

    pred = non_max_suppression(pred, 0.4, 0.5, classes=None, agnostic=False)
    return len(pred[0]) > 0

# Function to stop the 3D printer
def stop_printer():
    #print('CANCELLED JOB')
    # Replace with your OctoPrint API endpoint and API key
    OCTOPRINT_URL = "http://localhost:5000/api/job"
    API_KEY = "3241F0BECBEE4C31A25F944A2D7E868B"
    
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": API_KEY,
    }
    
    data = {
        "command": "cancel"
    }
    
    response = requests.post(OCTOPRINT_URL, headers=headers, json=data)
    if response.status_code == 204:
        print("Print job canceled successfully.")
    else:
        pass
        #print("Failed to cancel print job:", response.content)

# Main function to watch the camera stream
def main():
    # Open the camera stream
    cap = cv2.VideoCapture('http://localhost:8080/?action=stream')

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    print("---DEFECTOR3D STARTED CHECKING---")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            continue

        # Run the defect detection model on the frame
        if detect_defect(frame):
            print("Defect detected! Stopping the printer.", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            stop_printer()
            cv2.imwrite('detected_frame.png', frame)
            #break
        else:
            pass
            #print("No problem for now at", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        # Display the frame (optional, for debugging)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close display window
    cap.release()

if __name__ == "__main__":
    main()

