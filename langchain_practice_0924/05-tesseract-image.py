# 老师 0924.zip 原版适配 Windows：tesseract 路径 Mac → Windows
import pytesseract as pt
from PIL import Image
# 指定 tesseract 的完整路径（Mac 原版：pt.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'）
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# 打开图片并识别
image = Image.open('./files/02.jpg')
text = pt.image_to_string(image, lang='chi_sim+eng') # 识别中文
print(text)
