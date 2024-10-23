#3.0
# import pytesseract
# import cv2

# # مسیر نصب Tesseract (برای ویندوز)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # خواندن تصویر
# image_path = 'sc.jpg'
# img = cv2.imread(image_path)

# # حذف نویز با استفاده از GaussianBlur
# blurred_img = cv2.GaussianBlur(img, (5, 5), 0)

# # افزایش کنتراست با استفاده از adaptiveThreshold (فقط برای پردازش)
# gray = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)
# _, thresholded_img = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# # انجام OCR با استفاده از Tesseract (حفظ تصویر رنگی برای نمایش)
# custom_config = r'--oem 3 --psm 6'
# text = pytesseract.image_to_string(img, lang='fas+eng', config=custom_config)

# # ذخیره نتایج در فایل متنی
# with open('ocr_output_tesseract.txt', 'w', encoding='utf-8') as file:
#     file.write(text)

# # اعلام اتمام عملیات
# print("عملیات OCR با Tesseract با موفقیت انجام شد. نتایج در فایل 'ocr_output_tesseract.txt' ذخیره شدند.")

#2.0
# import easyocr
# import cv2

# # خواندن تصویر
# image_path = 'sc.jpg'
# img = cv2.imread(image_path)

# # ایجاد یک خواننده OCR برای زبان فارسی
# reader = easyocr.Reader(['fa', 'en'])

# # انجام OCR روی تصویر
# result = reader.readtext(image_path)

# # باز کردن فایل متنی برای نوشتن نتایج
# with open('ocr_output.txt', 'w', encoding='utf-8') as file:
#     # نمایش و ذخیره نتایج
#     for (bbox, text, prob) in result:
#         # نوشتن متن و احتمال در فایل
#         file.write(f'Text: {text}, Probability: {prob:.4f}\n')
        
#         # نمایش تصویر با جعبه های مرزی
#         (top_left, top_right, bottom_right, bottom_left) = bbox
#         top_left = tuple(map(int, top_left))
#         bottom_right = tuple(map(int, bottom_right))
#         img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

# # اعلام اتمام عملیات
# print("عملیات OCR با موفقیت انجام شد. نتایج در فایل 'ocr_output.txt' ذخیره شدند.")



#1.0
# import easyocr
# import cv2
# from matplotlib import pyplot as plt

# # خواندن تصویر
# image_path = 'sc2.jpg'
# img = cv2.imread(image_path)

# # ایجاد یک خواننده OCR برای زبان فارسی
# reader = easyocr.Reader(['fa', 'en'])

# # انجام OCR روی تصویر
# result = reader.readtext(image_path)

# # نمایش نتایج
# for (bbox, text, prob) in result:
#     # چاپ کردن متن و احتمال
#     print(f'Text: {text}, Probability: {prob:.4f}')
    
#     # نمایش تصویر با جعبه های مرزی
#     (top_left, top_right, bottom_right, bottom_left) = bbox
#     top_left = tuple(map(int, top_left))
#     bottom_right = tuple(map(int, bottom_right))
#     img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

# # نمایش تصویر با جعبه‌های متنی
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# plt.show()
