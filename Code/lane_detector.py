import cv2
import numpy as np

class LaneCamera(object):
    """
    A class to handle video capturing and lane detection on each frame.
    """

    def __init__(self, video_path):
        """Initializes the video capture object with the provided video path."""
        self.video = cv2.VideoCapture(video_path)

    def __del__(self):
        """Releases the video capture object."""
        self.video.release()

    def _roi(self, img, vertices):
        """Applies a region of interest mask to an image."""
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, vertices, 255)
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    def _draw_lines(self, img, lines):
        """Draws detected lane lines on a blank image."""
        img = np.copy(img)
        line_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), thickness=5)
        
        # Superimpose the lines onto the original image
        img = cv2.addWeighted(img, 0.8, line_image, 1, 0.0)
        return img

    def _process_frame(self, image):
        """The main processing pipeline for detecting lane lines in a single frame."""
        height = image.shape[0]
        width = image.shape[1]
        
        # Define the triangular region of interest
        region_of_interest_vertices = [
            (0, height),
            (width / 2, height / 2),
            (width, height)
        ]
        
        # Convert to grayscale and apply Canny edge detection
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        canny_image = cv2.Canny(gray_image, 100, 120)
        
        # Apply the region of interest mask
        cropped_image = self._roi(canny_image, np.array([region_of_interest_vertices], np.int32))
        
        # Use Hough Transform to find lines in the cropped image
        lines = cv2.HoughLinesP(cropped_image,
                                rho=2,
                                theta=np.pi / 60,
                                threshold=160,
                                lines=np.array([]),
                                minLineLength=40,
                                maxLineGap=25)
        
        # Draw the detected lines on the original image
        image_with_lines = self._draw_lines(image, lines)
        return image_with_lines

    def get_frame(self):
        """Reads one frame, processes it for lanes, and returns it as a JPEG."""
        ret, frame = self.video.read()
        
        if not ret:
            # If the video has ended, return None
            return None
        
        # Process the frame to detect lanes
        processed_frame = self._process_frame(frame)
        
        # Encode the processed frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', processed_frame)
        return jpeg.tobytes()
