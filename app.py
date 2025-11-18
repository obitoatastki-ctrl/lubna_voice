from flask import Flask, render_template, request, jsonify
import sqlite3
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# إعداد Cloudinary
cloudinary.config(
  cloud_name='YOUR_CLOUD_NAME',
  api_key='YOUR_API_KEY',
  api_secret='YOUR_API_SECRET'
)

# إنشاء قاعدة البيانات إذا لم تكن موجودة
conn = sqlite3.connect('videos.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS videos
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, url TEXT)''')
conn.commit()
conn.close()

@app.route('/awami')
def awami():
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    c.execute("SELECT * FROM videos ORDER BY id DESC")
    videos = c.fetchall()
    conn.close()
    return render_template('awami.html', videos=videos, cloud_name='YOUR_CLOUD_NAME', upload_preset='YOUR_UPLOAD_PRESET')

@app.route('/add_video', methods=['POST'])
def add_video():
    data = request.get_json()
    name = data['name']
    url = data['url']
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    c.execute("INSERT INTO videos (name, url) VALUES (?,?)", (name, url))
    video_id = c.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'id': video_id})

@app.route('/delete', methods=['POST'])
def delete_video():
    data = request.get_json()
    video_id = data['id']
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    c.execute("SELECT url FROM videos WHERE id=?", (video_id,))
    row = c.fetchone()
    if row:
        url = row[0]
        public_id = url.split('/')[-1].split('.')[0]
        cloudinary.uploader.destroy(public_id, resource_type="video")
    c.execute("DELETE FROM videos WHERE id=?", (video_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == "__main__":
    app.run(debug=True)
