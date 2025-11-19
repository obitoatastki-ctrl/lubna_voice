from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

videos = []

@app.route('/awami', methods=['GET', 'POST'])
def awami():
    if request.method == 'POST':
        file_to_upload = request.files['file']
        if file_to_upload:
            result = cloudinary.uploader.upload(file_to_upload, resource_type="video")
            videos.append({
                "public_id": result['public_id'],
                "url": result['secure_url'],
                "filename": file_to_upload.filename
            })
        return redirect(url_for('awami'))
    return render_template('awami.html', videos=videos)

@app.route('/delete/<public_id>')
def delete_video(public_id):
    cloudinary.uploader.destroy(public_id, resource_type="video")
    global videos
    videos = [v for v in videos if v['public_id'] != public_id]
    return redirect(url_for('awami'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
