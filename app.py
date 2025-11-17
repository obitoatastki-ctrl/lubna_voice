from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'lubna_voice_secret_key'

# مجلد رفع الملفات
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# حدّ تحميل كبير (مثلاً 10GB) - ملاحظة: مضيف الاستضافة قد يقيّد أكثر
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024  # 10 GB

# أنواع الملفات المدعومة (يمكن توسيعها)
ALLOWED_EXT = {
    'mp4','mov','avi','mkv','webm','flv',
    'mp3','wav','ogg','flac','aac',
    'zip','rar'  # لو تريد دعم أرشيفات الأعمال
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

# نصوص/محتوى متعدد اللغات (بداية: العربية جاهزة، الإنجليزية والفرنسية نصوص بسيطة)
translations = {
    'ar': {
        'home': 'الرئيسية',
        'portfolio': 'أعمالي',
        'request': 'اطلب خدمة',
        'contact': 'اتصل بنا',
        'admin': 'لوحة الإدارة',
        'title': 'استوديو لبنى الصوتي',
        'intro': 'لبنى — معلقة صوتية، منشّطة رِكح، ومؤدية دبلجة رسوم كرتونية. احترافية في الأداء وإيصال المشاعر عبر الصوت.',
        'upload_label': 'اختر فيديو أو مقطع صوتي لرفعه',
        'upload_button': 'رفع الملف',
        'no_files': 'لا توجد أعمال بعد.',
        'upload_success': '✅ تم رفع الملف بنجاح!',
        'upload_error': '⚠️ حدث خطأ أثناء الرفع أو نوع الملف غير مدعوم.',
        'contact_email': 'lobnataib2@gmail.com',
        'choose_lang': 'اختر اللغة'
    },
    'en': {
        'home': 'Home',
        'portfolio': 'My Works',
        'request': 'Request Service',
        'contact': 'Contact',
        'admin': 'Admin Panel',
        'title': 'Lubna Voice Studio',
        'intro': 'Lubna — voice-over artist, stage host, and cartoon dubbing performer. Professional voice work that conveys emotion.',
        'upload_label': 'Choose a video or audio file to upload',
        'upload_button': 'Upload File',
        'no_files': 'No works yet.',
        'upload_success': '✅ File uploaded successfully!',
        'upload_error': '⚠️ Upload error or unsupported file type.',
        'contact_email': 'lobnataib2@gmail.com',
        'choose_lang': 'Choose language'
    },
    'fr': {
        'home': 'Accueil',
        'portfolio': 'Mes Travaux',
        'request': 'Demander un service',
        'contact': 'Contact',
        'admin': 'Panneau Admin',
        'title': 'Studio Voix Lubna',
        'intro': 'Lubna — comédienne voix-off, animatrice de scène et doubleuse de dessins animés. Performance vocale professionnelle.',
        'upload_label': 'Choisir une vidéo ou un fichier audio à téléverser',
        'upload_button': 'Téléverser le fichier',
        'no_files': 'Aucun fichier pour le moment.',
        'upload_success': '✅ Fichier téléversé avec succès!',
        'upload_error': "⚠️ Erreur d'envoi ou type de fichier non pris en charge.",
        'contact_email': 'lobnataib2@gmail.com',
        'choose_lang': 'Choisir la langue'
    }
}

def get_lang():
    lang = request.args.get('lang', 'ar')
    return lang if lang in translations else 'ar'

# ----- ROUTES -----
@app.route('/')
def index_root():
    return redirect(url_for('index', lang='ar'))

@app.route('/<lang>/')
def index(lang='ar'):
    lang = lang if lang in translations else 'ar'
    text = translations[lang]
    return render_template('index.html', lang=lang, text=text)

@app.route('/<lang>/portfolio', methods=['GET','POST'])
def portfolio(lang='ar'):
    lang = lang if lang in translations else 'ar'
    text = translations[lang]
    if request.method == 'POST':
        # رفع الملف
        if 'file' not in request.files:
            flash(text['upload_error'], 'danger')
            return redirect(url_for('portfolio', lang=lang))
        file = request.files['file']
        if file.filename == '':
            flash(text['upload_error'], 'danger')
            return redirect(url_for('portfolio', lang=lang))
        # اسم أمني
        filename = secure_filename(file.filename)
        if allowed_file(filename):
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash(text['upload_success'], 'success')
                return redirect(url_for('portfolio', lang=lang))
            except Exception as e:
                print("Save error:", e)
                flash(text['upload_error'], 'danger')
                return redirect(url_for('portfolio', lang=lang))
        else:
            flash(text['upload_error'], 'danger')
            return redirect(url_for('portfolio', lang=lang))
    # GET
    files = sorted(os.listdir(app.config['UPLOAD_FOLDER']), reverse=True)
    return render_template('portfolio.html', lang=lang, text=text, files=files)

@app.route('/<lang>/request_service', methods=['GET','POST'])
def request_service(lang='ar'):
    lang = lang if lang in translations else 'ar'
    text = translations[lang]
    if request.method == 'POST':
        # نحفظ الطلب محليًا كملف بسيط أو نعرض إشعارًا (يمكن ربط DB لاحقًا)
        name = request.form.get('name')
        email = request.form.get('email')
        service = request.form.get('service')
        details = request.form.get('details')
        # تحفظ كملف نصي صغير في uploads/requests.txt
        try:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], 'requests.txt'), 'a', encoding='utf-8') as f:
                f.write(f"Name: {name}\nEmail: {email}\nService: {service}\nDetails: {details}\n-----\n")
            flash('✅ تم إرسال طلبك! سنتواصل معك قريبًا.', 'success')
        except Exception as e:
            print("Request save error:", e)
            flash('⚠️ حدث خطأ أثناء إرسال الطلب.', 'danger')
        return redirect(url_for('request_service', lang=lang))
    return render_template('request_service.html', lang=lang, text=text)

@app.route('/<lang>/contact')
def contact(lang='ar'):
    lang = lang if lang in translations else 'ar'
    text = translations[lang]
    return render_template('contact.html', lang=lang, text=text)

# لوحة الإدارة: قائمة الملفات + حذف
@app.route('/admin')
def admin():
    files = sorted(os.listdir(app.config['UPLOAD_FOLDER']), reverse=True)
    return render_template('admin.html', files=files)

@app.route('/admin/delete/<filename>', methods=['POST'])
def admin_delete(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(path):
        try:
            os.remove(path)
            flash('تم حذف الملف بنجاح', 'success')
        except Exception as e:
            print("Delete error:", e)
            flash('حدث خطأ أثناء الحذف', 'danger')
    return redirect(url_for('admin'))

# Serve static root index quick
@app.errorhandler(413)
def file_too_large(e):
    flash('حجم الملف كبير جدًا. حاول ملفًا أصغر أو جهّز استضافة تدعم رفع كبير.', 'danger')
    return redirect(request.referrer or url_for('index', lang='ar'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
