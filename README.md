# 🤖 AI RealTime Detection Of DamagedRoad & LaneDetection
![Demo Video](images/Landandpotholes.gif)

This project is an advanced perception system that uses computer vision to perform real-time lane detection and identify damaged road conditions from a video feed.

By analyzing road imagery, the application can pinpoint potential hazards like cracks and potholes while simultaneously tracking lane boundaries, making it a powerful tool for road maintenance analysis and driver-assistance systems.

---

## 📁 Project Structure

```
Code/
    app.py                # Main Flask application
    camera.py             # Pothole detection (YOLO)
    lane_detector.py      # Lane detection logic
    detector.py           # Lane detection (standalone script)
    detection_test.py     # Lane detection test script
    streamImage.py        # Flask image streaming demo
    streamVideo.py        # Flask video streaming demo
    location.py           # (Planned) Location logging
    models/               # YOLO model files (.cfg, .weights)
    templates/            # HTML templates for Flask
    static/               # CSS, JS, images, vendor assets
    requirements.txt      # Python dependencies
    app.yaml              # Deployment config (App Engine)
    uploads/, videos/, OutputImg/, test_images/ # Data folders
```


## 🚀 Key Features

-   **Real-Time Lane Detection:** Implements computer vision techniques like the Hough Transform to accurately identify and track lane lines on various road types.
-   **Damaged Road Detection:** A key safety feature that analyzes the road texture and surface to detect potential hazards like potholes and significant cracks.
-   **Dual Mode Operation:**
    -   **Video File Analysis:** Process any pre-recorded video of a road to test and validate the detection algorithms.
    -   **Live Camera Feed:** Use a webcam to perform lane and hazard detection in real-time.
-   **Interactive Web Interface:** A clean UI built with Flask to handle video uploads and display the processed output with detections overlaid.
-   **Optimized for Performance:** Utilizes the highly efficient OpenCV library for real-time video frame processing.

-   **YOLOv4 Pothole Detection:** Uses pretrained YOLOv4-tiny model (`models/yolov4_tiny_pothole_last.weights`, `.cfg`) for pothole detection.
-   **Audio Alert:** Plays a beep sound (`beep.wav`) when a pothole is detected in a video frame.
-   **Multiple Endpoints:**
    - `/` Home
    - `/pothole_upload`, `/lane_upload` Video upload pages
    - `/upload/pothole`, `/upload/lane` POST endpoints for uploads
    - `/pothole_player/<filename>`, `/lane_player/<filename>` Video player pages
    - `/pothole_video_feed/<filename>`, `/lane_video_feed/<filename>` Streaming endpoints
    - `/chart`, `/info`, `/login` Additional pages


---

## 🛠️ Technologies & Libraries Used

-   **Backend:** Python, Flask
-   **Computer Vision:** OpenCV
-   **Numerical Processing:** NumPy
-   **Version Control:** Git & Git LFS (for handling large video files)
-   **Deployment (Planned):** Render, Gunicorn

-   **Deep Learning:** YOLOv4-tiny (Darknet)
-   **Other:** winsound (audio), pandas, scikit-learn, scipy

---

## 🏁 Getting Started: How to Run Locally

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.8+ and Pip
-   Git and [Git LFS](https://git-lfs.github.com/) must be installed.

-   Download YOLO model files (`models/yolov4_tiny_pothole_last.weights`, `models/yolov4_tiny_pothole.cfg`) and place them in the `models/` folder.
-   Ensure `beep.wav` is present in the `Code/` directory for audio alerts.

### Installation & Setup

1.  **Clone the repository:**
    *This command will also download the large video files handled by Git LFS.*
    ```sh
    git clone [https://github.com/CodewithShaaz/AI-RealTime-Detection-Of-DamagedRoad-LaneDetection.git](https://github.com/CodewithShaaz/AI-RealTime-Detection-Of-DamagedRoad-LaneDetection.git)
    cd AI-RealTime-Detection-Of-DamagedRoad-LaneDetection
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```sh
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```sh
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` doesn't exist yet, create it with `pip freeze > requirements.txt`)*

### Running the Application

### Running the Application

1.  **Navigate to the Code directory:**
    ```sh
    cd Code
    ```

2.  **Run the Flask app:**
    ```sh
    python app.py
    ```

3.  Open your web browser and go to `http://127.0.0.1:5000` to see the application live.

#### Other scripts
- `detector.py`, `detection_test.py`: Standalone lane detection scripts for testing
- `streamImage.py`, `streamVideo.py`: Demo Flask apps for image/video streaming
- `location.py`: (Planned) Location logging to database (currently commented out)

---

## 🚀 Deployment

This project includes an `app.yaml` for deployment (e.g., Google App Engine Flexible Environment). Example:

```yaml
entrypoint: "gunicorn -b :$PORT main:app"
env: flex
runtime: python
runtime_config:
    python_version: 3
```

You may need to adjust the entrypoint and runtime settings for your cloud provider.

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.

## ⚠️ Known Issues / TODOs

- Location logging (`location.py`) is not yet active (requires MongoDB and geocoder setup).
- Deployment instructions may need to be adapted for your cloud provider.
- Model files (`.weights`, `.cfg`) are not included due to size—download separately.


