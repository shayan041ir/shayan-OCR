import os
import re

import cv2
import numpy as np
import pytesseract
from PIL import Image

# تنظیم مسیر Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def process_image(img_path):
    """
    پردازش اولیه تصویر شامل تغییر اندازه، حذف نویز و چرخش صحیح
    """
    temp_filename = resize_image(img_path)
    img = remove_noise_and_smooth(temp_filename)
    img = fix_rotation(img)
    # img = remove_lines(img) # فعال‌سازی در صورت نیاز

    return img


def resize_image(img_path):
    """
    تغییر اندازه تصویر برای بهبود OCR
    """
    try:
        img = Image.open(img_path)
        length_x, width_y = img.size
        factor = max(1, int(1800 / length_x))  # 1800 برای بهبود دقت Tesseract
        size = factor * length_x, factor * width_y
        # اصلاح مشکل حذف شده Image.ANTIALIAS
        im_resized = img.resize(size, Image.LANCZOS)

        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".TIFF")
        temp_filename = temp_file.name
        im_resized.save(temp_filename, dpi=(300, 300))  # بهترین DPI برای OCR

        return temp_filename
    except IOError:
        print("خطا در هنگام خواندن فایل.")


def remove_noise_and_smooth(img_path):
    """
    حذف نویز و صاف کردن تصویر برای بهبود دقت OCR
    """
    try:
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # اعمال مورفولوژی برای کاهش نویز
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        img = cv2.bitwise_or(img, closing)
        show_wait_destroy('bitwise_or', img)

        return img
    except IOError:
        print("خطا در هنگام خواندن فایل.")


def apply_threshold(img, argument):
    """
    اعمال روش‌های مختلف آستانه‌گذاری
    """
    switcher = {
        1: cv2.threshold(cv2.GaussianBlur(img, (9, 9), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        2: cv2.threshold(cv2.GaussianBlur(img, (7, 7), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        3: cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        4: cv2.threshold(cv2.medianBlur(img, 5), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        5: cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        6: cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 31, 2),
        7: cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31,
                                 2),
    }
    return switcher.get(argument, "روش نامعتبر")


def smooth_image(img):
    """
    اعمال فیلتر محوشدگی
    """
    blur_img = cv2.GaussianBlur(img, (1, 1), 0)
    show_wait_destroy('blur', blur_img)

    return blur_img


def fix_rotation(img):
    """
    اصلاح چرخش تصویر براساس خروجی Tesseract OSD
    """
    rotated_img = img
    tess_data = pytesseract.image_to_osd(img, nice=1)
    angle = int(re.search(r"(?<=Rotate: )\d+", tess_data).group(0))
    print("زاویه: " + str(angle))

    if angle != 0 and angle != 360:
        (h, w) = img.shape[:2]
        center = (w / 2, h / 2)

        # انجام چرخش تصویر
        rotation_mat = cv2.getRotationMatrix2D(center, -angle, 1.0)
        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        bound_w = int(h * abs_sin + w * abs_cos)
        bound_h = int(h * abs_cos + w * abs_sin)

        rotation_mat[0, 2] += bound_w / 2 - center[0]
        rotation_mat[1, 2] += bound_h / 2 - center[1]

        rotated_img = cv2.warpAffine(img, rotation_mat, (bound_w, bound_h))

    return rotated_img


def remove_lines(img):
    """
    حذف خطوط از تصاویر برای بهبود دقت در اسناد جدولی
    """
    result = img.copy()
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # حذف خطوط افقی
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(result, [c], -1, (255, 255, 255), 5)

    # حذف خطوط عمودی
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(result, [c], -1, (255, 255, 255), 5)

    show_wait_destroy('nolines', result)

    return result


def show_wait_destroy(winname, img, active=False):
    """
    نمایش تصویر به همراه وقفه تا زمان بسته شدن پنجره
    """
    if active:
        cv2.imshow(winname, cv2.resize(img, (960, 540)))
        cv2.moveWindow(winname, 500, 0)
        cv2.waitKey(0)
        cv2.destroyWindow(winname)


def save_image(img, img_path, method, active=False):
    """
    ذخیره تصویر فیلتر شده در مسیر خروجی
    """
    if active:
        filename = os.path.basename(img_path).split('.')[0]
        filename = filename.split()[0]
        save_path = os.path.join("../output", filename + "_filter_" + method + ".jpg")
        cv2.imwrite(save_path, img)
