from flask import Flask, render_template, request, redirect, url_for
import os
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# قراءة مفاتيح Cloudinary من Environment Variables
cloudinary.config(
    cloud_name=os.environ.get('CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
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
                "url": result['secure_url']
            })
        return redirect(url_for('awami'))
    return render_template('awami.html', videos=videos)

@app.route('/delete/<public_id>')
def delete_video(public_id):
    cloudinary.uploader.destroy(public_id, resource_type="video")
    global videos
    videos = [v for v in videos if v['public_id'] != public_id]
    return redirect(url_for('awami'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
