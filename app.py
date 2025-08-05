from flask import Flask, request, send_file
import os
import requests
import uuid
import subprocess

app = Flask(__name__)

@app.route('/add-heading', methods=['POST'])
def add_heading():
    # Get form fields
    video_file = request.files.get('video_url')
if video_file:
    input_path = f"/tmp/{uuid.uuid4()}.mp4"
    video_file.save(input_path)
else:
    video_url = request.form.get('video_url')
    r = requests.get(video_url)
    input_path = f"/tmp/{uuid.uuid4()}.mp4"
    with open(input_path, 'wb') as f:
        f.write(r.content)
    heading = request.form.get('heading', 'Sample Text')
    font_size = int(request.form.get('font_size', 48))
    font_color = request.form.get('font_color', 'white')
    text_bg_color = request.form.get('text_bg_color', 'red')
    position = request.form.get('position', 'top')  # top, center, bottom
    margin_px = int(request.form.get('margin_px', 60))
    start_time = float(request.form.get('start_time', 0))
    end_time = float(request.form.get('end_time', 5))

    # Download video
    input_path = f"/tmp/{uuid.uuid4()}.mp4"
    output_path = f"/tmp/{uuid.uuid4()}_output.mp4"
    r = requests.get(video_url)
    with open(input_path, 'wb') as f:
        f.write(r.content)

    # Calculate y position based on choice
    if position == 'top':
        y = margin_px
    elif position == 'bottom':
        y = f"h-text_h-{margin_px}"
    else:
        y = "(h-text_h)/2"

    # FFmpeg command
    cmd = [
        "ffmpeg", "-i", input_path,
        "-vf", f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
               f"text='{heading}':"
               f"fontcolor={font_color}:"
               f"fontsize={font_size}:"
               f"box=1:boxcolor={text_bg_color}:"
               f"x=(w-text_w)/2:y={y}:"
               f"enable='between(t,{start_time},{end_time})'",
        "-c:a", "copy", output_path
    ]

    subprocess.run(cmd, check=True)
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
