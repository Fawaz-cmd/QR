from flask import Flask, render_template, request, send_file
import os
import qrcode
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
QR_FOLDER = 'static/qr'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', error='No file part')
        
        image = request.files['image']
        if image.filename == '':
            return render_template('index.html', error='No selected file')

        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

        # Generate QR Code from the image path (or any data you want)
        qr = qrcode.make(image_path)
        qr_path = os.path.join(QR_FOLDER, f'{filename}_qr.png')
        qr.save(qr_path)

        return render_template('index.html', qr_code=qr_path)

    return render_template('index.html')
