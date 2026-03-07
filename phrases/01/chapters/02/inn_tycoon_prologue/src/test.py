import pytesseract
from PIL import Image

# Defina o caminho do executável (se ainda não fez no script)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Troque pelo caminho de uma imagem da sua máquina com texto claro!
imagem_teste = r'C:\Users\isaac\Desktop\inn_tycoon_prologue\assets\game_interface_view_resized.png'

# Abre a imagem e faz o OCR
img = Image.open(imagem_teste)
texto = pytesseract.image_to_string(img, lang='eng')
print(texto)
