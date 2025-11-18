from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# قراءة المفاتيح من Environment Variables في Render
cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET")
)

# قائمة الفيديوهات الحالية (ستأتي من Cloudinary عند التشغيل لاحقاً)
videos = []

@app.route('/awami', methods=['GET', 'POST'])
def awami():
    global videos
    if request.method == 'POST':
        file_to_upload = request.files['file']
        if file_to_upload:
            result = cloudinary.uploader.upload(
                file_to_upload, 
                resource_type="video",
                folder="lubna_videos"  # تنظيم الملفات في Cloudinary
            )
            videos.append({
                "public_id": result['public_id'],
                "url": result['secure_url']
            })
        return redirect(url_for('awami'))
    return render_template('awami.html', videos=videos)

@app.route('/delete/<public_id>')
def delete_video(public_id):
    global videos
    cloudinary.uploader.destroy(public_id, resource_type="video")
    videos = [v for v in videos if v['public_id'] != public_id]
    return redirect(url_for('awami'))

if __name__ == '__main__':
    app.run(debug=True)
