import cv2
import numpy as np
import winsound
import time

# --- Model and Class Setup ---
# Load the YOLO model and class names. This only needs to be done once.
net = cv2.dnn.readNetFromDarknet('models/yolov4_tiny_pothole.cfg', 'models/yolov4_tiny_pothole_last.weights')
classes = ['pothole']

class VideoCamera(object):
    """
    A class to handle video capturing and pothole detection on each frame.
    """
    
    # STEP 1: Modify the constructor (__init__)
    # It now accepts a 'video_path' so we can tell it which video to process.
    def __init__(self, video_path):
        """Initializes the video capture object with the provided video path."""
        self.video = cv2.VideoCapture(video_path)

    def __del__(self):
        """Releases the video capture object when the class instance is deleted."""
        self.video.release()

    def get_frame(self):
        """
        Reads one frame from the video, performs pothole detection,
        and returns the processed frame as a JPEG byte string.
        """
        # Read a single frame from the video stream
        ret, frame = self.video.read()
        
        # If 'ret' is False, it means the video has ended or there was an error.
        if not ret:
            return None # Return None to signal the end of the stream

        try:
            # --- Frame Preparation ---
            t = time.time()
            # Resize the frame for consistent processing
            frame = cv2.resize(frame, (800, 450), interpolation=cv2.INTER_AREA)
            ht, wt, _ = frame.shape
            
            # Create a blob from the image to feed into the YOLO network
            blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
            net.setInput(blob)
            
            # --- Inference ---
            last_layer = net.getUnconnectedOutLayersNames()
            layer_out = net.forward(last_layer)
            
            # --- Process Detections ---
            boxes = []
            confidences = []
            cls_ids = []
            
            for output in layer_out:
                for detection in output:
                    score = detection[5:]
                    clsid = np.argmax(score)
                    conf = score[clsid]
                    if conf > 0.25: # Confidence threshold
                        centreX = int(detection[0] * wt)
                        centreY = int(detection[1] * ht)
                        w = int(detection[2] * wt)
                        h = int(detection[3] * ht)
                        x = int(centreX - w / 2)
                        y = int(centreY - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(conf))
                        cls_ids.append(clsid)

            # --- Draw Bounding Boxes on Frame ---
            # Apply Non-Max Suppression to remove overlapping boxes
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, .25, .2)
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            
            # IMPROVEMENT: Check if any detections exist before looping
            if len(indexes) > 0:
                pothole_detected_in_frame = False
                for i in indexes.flatten():
                    x, y, w, h = boxes[i]
                    area = w * h // 400
                    label = str(classes[cls_ids[i]])
                    
                    # Draw the bounding box and labels
                    cv2.rectangle(frame, (x-2, y-2), (x + w+2, y + h+2), (0, 0, 255), 2)
                    cv2.rectangle(frame, (x-2, y-2), (x + 120, y - 18), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, f"{label} {confidences[i]:.2f}", (x, y - 7), font, .6, (255, 255, 255), 1)
                    
                    if label == 'pothole':
                        pothole_detected_in_frame = True

                # Play sound once if any pothole was detected in this frame
                if pothole_detected_in_frame:
                    winsound.PlaySound('beep.wav', winsound.SND_ASYNC)

            # --- Display FPS and Encode Frame ---
            t2 = time.time()
            fps = round(1 / (t2 - t))
            cv2.putText(frame, f'FPS: {fps}', (24, 30), font, 1.4, (55, 255, 255), 2)
            
            # Encode the final frame to JPEG format
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

        except Exception as e:
            print(f"Error processing frame: {e}")
            # If an error occurs, return the original frame without annotations
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
