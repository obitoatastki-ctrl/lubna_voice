from flask import Flask, render_template, request, redirect, url_for
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# Cloudinary configuration using environment variables (مفضل للسرية)
cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET")
)

# صفحة الأعمال
@app.route('/awami', methods=['GET', 'POST'])
def awami():
    if request.method == 'POST':
        file_to_upload = request.files.get('file')
        if file_to_upload:
            # رفع الفيديو إلى Cloudinary
            result = cloudinary.uploader.upload(
                file_to_upload,
                resource_type="video",
                folder="lubna_video"
            )
        return redirect(url_for('awami'))

    # جلب قائمة الفيديوهات الموجودة في Cloudinary
    try:
        videos_data = cloudinary.api.resources(
            type="upload",
            resource_type="video",
            prefix="lubna_video/"
        )
        videos = [{"public_id": v["public_id"], "url": v["secure_url"]} for v in videos_data.get("resources", [])]
    except Exception as e:
        videos = []
        print("Error fetching videos:", e)

    return render_template('awami.html', videos=videos)

# حذف فيديو
@app.route('/delete/<public_id>', methods=['POST'])
def delete_video(public_id):
    try:
        cloudinary.uploader.destroy(public_id, resource_type="video")
    except Exception as e:
        print("Error deleting video:", e)
    return redirect(url_for('awami'))

# تحويل الصفحة الرئيسية إلى صفحة أعمالك
@app.route('/')
def home():
    return redirect(url_for('awami'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
