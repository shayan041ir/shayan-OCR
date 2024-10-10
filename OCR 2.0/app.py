from flask import Flask, render_template, request, redirect, url_for
import pytesseract
from PIL import Image
import os

# اگر از ویندوز استفاده می‌کنید مسیر نصب Tesseract را وارد کنید
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'




app = Flask(__name__)

# مسیر برای آپلود فایل‌ها
import os

# مسیر آپلود فایل
UPLOAD_FOLDER = 'uploads'

# بررسی و ایجاد پوشه اگر وجود ندارد
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# صفحه اصلی که فرم آپلود تصویر را نمایش می‌دهد
@app.route('/')
def index():
    return render_template('index.html')

# مسیری برای پردازش تصویر
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file:
        print("file is here")
        # ذخیره فایل در مسیر آپلود
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # استفاده از OCR برای استخراج متن از تصویر
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image, lang='eng+fas')
        
        # نمایش نتیجه در صفحه
        return render_template('result.html', text=text)

if __name__ == '__main__':
    app.run(debug=True,port="8080")
