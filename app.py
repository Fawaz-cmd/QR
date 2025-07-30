from flask import Flask, render_template, request, send_file
import os
import qrcode
from PIL import Image
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['QR_FOLDER'] = 'static/qr'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['QR_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # handle uploaded file here
        ...
    return render_template('index.html')


@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    if 'image' not in request.files:
        return "No image file uploaded.", 400

    image_file = request.files['image']
    if image_file.filename == '':
        return "No selected file.", 400

    img_filename = str(uuid.uuid4()) + "_" + image_file.filename
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
    image_file.save(img_path)

    qr = qrcode.make(f"Uploaded image: {img_filename}")
    qr_filename = img_filename.replace(".", "_") + "_qr.png"
    qr_path = os.path.join(app.config['QR_FOLDER'], qr_filename)
    qr.save(qr_path)

    return render_template('index.html', qr_image=qr_path, qr_name=qr_filename)

@app.route('/download/<filename>')
def download_qr(filename):
    return send_file(os.path.join(app.config['QR_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)

