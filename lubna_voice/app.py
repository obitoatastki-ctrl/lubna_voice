from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "lubna_voice_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///services.db"
app.config["UPLOAD_FOLDER"] = "static/uploads"
db = SQLAlchemy(app)

# نموذج الطلب
class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    service_type = db.Column(db.String(100))
    status = db.Column(db.String(50), default="قيد المعالجة")
    source = db.Column(db.String(50), default="زبون")

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

# صفحة اتصل بنا
@app.route('/contact')
def contact():
    return render_template('contact.html')

# صفحة أعمالي
@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

# صفحة أطلب خدمة
@app.route('/request_service', methods=['GET', 'POST'])
def request_service():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        service_type = request.form['service_type']
        new_request = ServiceRequest(name=name, email=email, service_type=service_type)
        db.session.add(new_request)
        db.session.commit()
        flash('تم إرسال طلبك بنجاح! سيتم التواصل معك قريبًا.')
        return redirect(url_for('home'))
    return render_template('request_service.html')

# صفحة لوحة الطلبات
@app.route('/dashboard')
def dashboard():
    requests = ServiceRequest.query.all()
    return render_template('dashboard.html', requests=requests)

if __name__ == "__main__":
    if not os.path.exists("services.db"):
        with app.app_context():
            db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
