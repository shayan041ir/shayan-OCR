from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from ocr import main as ocr_main

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../data')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '../output')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        ocr_main()  # اجرای تابع OCR

        output_filename = f"out_{os.path.splitext(file.filename)[0]}.txt"
        return redirect(url_for('output_file', filename=output_filename))

@app.route('/output/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True,port=8000)
