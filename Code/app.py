import os
from flask import Flask, render_template, Response, request, redirect, url_for
from werkzeug.utils import secure_filename

# --- Import our new detector classes ---
from camera import VideoCamera
from lane_detector import LaneCamera

# --- Flask App Setup ---
app = Flask(__name__)

# --- Configuration for File Uploads ---
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ====================================================================
#  MAIN AND UPLOAD PAGES
# ====================================================================

@app.route('/')
def home():
    """The main home page with links to both detectors."""
    return render_template('home.html')

@app.route('/pothole_upload')
def pothole_upload_page():
    """Renders the page to upload a video for pothole detection."""
    return render_template('pothole_upload.html')

@app.route('/lane_upload')
def lane_upload_page():
    """Renders the page to upload a video for lane detection."""
    return render_template('lane_upload.html')

@app.route('/upload/pothole', methods=['POST'])
def upload_pothole_video():
    """Handles the video upload for pothole detection."""
    if 'video' not in request.files:
        return redirect(request.url)
    file = request.files['video']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return redirect(url_for('pothole_player_page', filename=filename))

@app.route('/upload/lane', methods=['POST'])
def upload_lane_video():
    """Handles the video upload for lane detection."""
    if 'video' not in request.files:
        return redirect(request.url)
    file = request.files['video']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return redirect(url_for('lane_player_page', filename=filename))

# ====================================================================
#  VIDEO PLAYER AND STREAMING PAGES
# ====================================================================

@app.route('/pothole_player/<filename>')
def pothole_player_page(filename):
    """Renders the player for the pothole detection stream."""
    return render_template('pothole_player.html', filename=filename)

@app.route('/lane_player/<filename>')
def lane_player_page(filename):
    """Renders the player for the lane detection stream."""
    return render_template('lane_player.html', filename=filename)

def gen_pothole_stream(camera):
    """Generator for pothole video stream."""
    while True:
        frame = camera.get_frame()
        if frame is None: break
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen_lane_stream(camera):
    """Generator for lane video stream."""
    while True:
        frame = camera.get_frame()
        if frame is None: break
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/pothole_video_feed/<filename>')
def pothole_video_feed(filename):
    """The video feed for pothole detection."""
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return Response(gen_pothole_stream(VideoCamera(video_path)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/lane_video_feed/<filename>')
def lane_video_feed(filename):
    """The video feed for lane detection."""
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return Response(gen_lane_stream(LaneCamera(video_path)), mimetype='multipart/x-mixed-replace; boundary=frame')

# ====================================================================
#  NEW: ADDED ROUTES FOR YOUR OTHER PAGES
# ====================================================================

@app.route('/chart')
def chart_page():
    """Renders the chart page."""
    return render_template('chart.html')

@app.route('/info')
def info_page():
    """Renders the info page."""
    return render_template('info.html')

@app.route('/login')
def login_page():
    """Renders the login page."""
    return render_template('login.html')

# --- Main Application Runner ---
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)
