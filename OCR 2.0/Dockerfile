# استفاده از تصویر پایه پایتون
FROM python:3.9-slim

# نصب وابستگی‌ها
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی فایل‌های پروژه به دایرکتوری کاری
COPY . /app

# نصب کتابخانه‌های پایتون
RUN pip install --no-cache-dir -r requirements.txt

# تنظیم متغیر محیطی برای Tesseract
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

# باز کردن پورت 8080
EXPOSE 8080

# اجرای برنامه
CMD ["python", "app.py"]
