import os
from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# إعداد Cloudinary من متغيرات البيئة
cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET")
)

# قائمة الفيديوهات المخزنة (يمكن استبدالها بقاعدة بيانات لاحقًا)
videos = []

@app.route('/awami', methods=['GET', 'POST'])
def awami():
    if request.method == 'POST':
        file_to_upload = request.files.get('file')
        if file_to_upload:
            # رفع الفيديو إلى Cloudinary
            result = cloudinary.uploader.upload(file_to_upload, resource_type="video")
            videos.append({
                "public_id": result['public_id'],
                "url": result['secure_url']
            })
        return redirect(url_for('awami'))
    return render_template('awami.html', videos=videos)

@app.route('/delete/<public_id>', methods=['GET'])
def delete_video(public_id):
    # حذف الفيديو من Cloudinary
    cloudinary.uploader.destroy(public_id, resource_type="video")
    global videos
    videos = [v for v in videos if v['public_id'] != public_id]
    return redirect(url_for('awami'))

if __name__ == '__main__':
    # التشغيل على Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
