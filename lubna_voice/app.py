from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Cloudinary configuration
cloudinary.config(
    cloud_name="dm84rwrrm",
    api_key="743793366569182",
    api_secret="Pku2tr25hXEVp_5Gy7Vqm5LX2Pk"
)

videos = []  # memory list (temporary)

@app.route('/awami', methods=['GET', 'POST'])
def awami():
    if request.method == 'POST':
        file_to_upload = request.files['file']
        if file_to_upload:
            result = cloudinary.uploader.upload(
                file_to_upload,
                resource_type="video",
                folder="awami_videos"
            )
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
    app.run(debug=True)
