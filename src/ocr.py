import os
import re
import pytesseract
from pdf2image import convert_from_path
from preprocess import process_image

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

langs = "fas+eng"  # زبان برای OCR، در صورت نیاز می‌توانید eng+fas کنید

dirname = os.path.dirname(os.path.dirname(__file__))
input_dir = os.path.join(dirname, "data")
output_dir = os.path.join(dirname, "output")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def main():
    """پردازش تمام فایل‌های موجود در پوشه ورودی و استخراج متن از آنها"""
    for filename in os.listdir(input_dir):
        try:
            if filename.endswith('.pdf'):
                print(f"پردازش فایل PDF: {filename}")
                fullName = os.path.join(input_dir, filename)
                pages = convert_from_path(fullName, 500)
                image_counter = 1
                for page in pages:
                    image_name = os.path.splitext(fullName)[0] + '_' + str(image_counter) + '.tiff'
                    page.save(image_name, format='TIFF')
                    image_counter += 1

            img_ext = ['.png', '.jpg', '.jpeg', '.tiff']
            if filename.endswith(tuple(img_ext)):
                print(f"پردازش تصویر: {filename}")
                fileAddress = os.path.join(input_dir, filename)
                img = process_image(fileAddress)

                # OCR روی تصویر
                config = ''
                text = str(pytesseract.image_to_string(img, lang=langs, config=config))

                # حذف خطوط خالی
                text = os.linesep.join([s for s in text.splitlines() if s.strip()])

                # جدا کردن متن فارسی و انگلیسی
                persian_text = re.findall(r'[\u0600-\u06FF\s]+', text)
                english_text = re.findall(r'[A-Za-z\s]+', text)

                # تبدیل لیست به رشته
                persian_text = ' '.join(persian_text)
                english_text = ' '.join(english_text)

                # ذخیره متون جداگانه
                write_output(filename, persian_text, "persian")
                write_output(filename, english_text, "english")

        except Exception as e:
            print(f"خطا در پردازش {filename}: {e}")

def write_output(filename, text, lang):
    """ذخیره خروجی متنی در فایل خروجی"""
    outfile = os.path.join(output_dir, f'out_{os.path.splitext(filename)[0]}_{lang}.txt')
    with open(outfile, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

if __name__ == "__main__":
    main()
