import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import mss
import pandas as pd
import time
import os
from PIL import Image
import re

MONITOR_WIDTH = 3840
MONITOR_HEIGHT = 2160

REGION_DAY = {
    "top": 80,
    "left": 2100,
    "width": 300,
    "height": 120
}
REGION_STATS_1 = {
    "top": 600,
    "left": 1350,
    "width": 800,
    "height": 1000
}
REGION_STATS_2 = {
    "top": 600,
    "left": 2150,
    "width": 800,
    "height": 1000
}

def preprocess_img(img):
    img = img.convert("L")
    img = img.point(lambda x: 0 if x < 140 else 255, '1')
    return img

COLUMNS = [
    'Day','Customer_Happy','Customer_Neutral','Customer_Angry','Customer_Failure','Customer_Count',
    'Revenues','Expenses','Balance',
    'Customer_Movement_Speed','Customer_Sleep_Speed','Customer_Eat_Speed','Customer_Bath_Speed','Customer_Steam_Bath_Speed','Tip_Chance','Tip_Amount',
    'Staff_Movement_Speed','Cooking_Speed','Pouring_Speed','Bed_Tidying_Speed','Bath_Fill_Speed','Bartender_Salary','Waitress_Salary','Housekeeper_Salary',
    'Cook_Salary','Bath_Attendant_Salary','Bard_Salary','Bartender_Recruitment_Cost','Waitress_Recruitment_Cost','Housekeeper_Recruitment_Cost',
    'Cook_Recruitment_Cost','Bath_Attendant_Recruitment_Cost','Bard_Recruitment_Cost',
    'Drink_Price','Food_Price','Bed_Price','Bath_Price','Steam_Bath_Price',
    'Tavern_Object_Cost','Bedroom_Object_Cost','Kitchen_Object_Cost','Bathroom_Object_Cost','Cellar_Object_Cost',
    'Experience_Modifier','Reputation_Modifier'
]

PATTERNS = {
    'Customer_Happy': r'Happy[:\s]*([0-9]+)',
    'Customer_Neutral': r'Neutral[:\s]*([0-9]+)',
    'Customer_Angry': r'Angry[:\s]*([0-9]+)',
    'Customer_Failure': r'Failure[:\s]*([0-9]+)',
    'Customer_Count': r'Customer\s*Count[:\s]*([0-9]+)',
    'Revenues': r'Revenues.*?(-?[0-9]+)',
    'Expenses': r'Expenses.*?(-?[0-9]+)',
    'Balance': r'Balance.*?(-?[0-9]+)',
    'Customer_Movement_Speed': r'Customer Movement Speed\s*([+\-0-9]+)\s*%',
    'Customer_Sleep_Speed': r'Customer Sleep Speed\s*([+\-0-9]+)\s*%',
    'Customer_Eat_Speed': r'Customer Eat Speed\s*([+\-0-9]+)\s*%',
    'Customer_Bath_Speed': r'Customer Bath Speed\s*([+\-0-9]+)\s*%',
    'Customer_Steam_Bath_Speed': r'Customer Steam Bath Speed\s*([+\-0-9]+)\s*%',
    'Tip_Chance': r'Tip Chance\s*([+\-0-9]+)\s*%',
    'Tip_Amount': r'Tip Amount\s*([+\-0-9]+)\s*%',
    'Staff_Movement_Speed': r'Staff Movement Speed\s*([+\-0-9]+)\s*%',
    'Cooking_Speed': r'Cooking Speed\s*([+\-0-9]+)\s*%',
    'Pouring_Speed': r'Pouring Speed\s*([+\-0-9]+)\s*%',
    'Bed_Tidying_Speed': r'Bed Tidying Speed\s*([+\-0-9]+)\s*%',
    'Bath_Fill_Speed': r'Bath Fill Speed\s*([+\-0-9]+)\s*%',
    'Bartender_Salary': r'Bartender Salary\s*([+\-0-9]+)\s*%',
    'Waitress_Salary': r'Waitress Salary\s*([+\-0-9]+)\s*%',
    'Housekeeper_Salary': r'Housekeeper Salary\s*([+\-0-9]+)\s*%',
    'Cook_Salary': r'Cook Salary\s*([+\-0-9]+)\s*%',
    'Bath_Attendant_Salary': r'Bath Attendant Salary\s*([+\-0-9]+)\s*%',
    'Bard_Salary': r'Bard Salary\s*([+\-0-9]+)\s*%',
    'Bartender_Recruitment_Cost': r'Bartender Recruitment Cost\s*([+\-0-9]+)\s*%',
    'Waitress_Recruitment_Cost': r'Waitress Recruitment Cost\s*([+\-0-9]+)\s*%',
    'Housekeeper_Recruitment_Cost': r'Housekeeper Recruitment Cost\s*([+\-0-9]+)\s*%',
    'Cook_Recruitment_Cost': r'Cook Recruitment Cost\s*([+\-0-9]+)\s*%',
    'Bath_Attendant_Recruitment_Cost': r'Bath Attendant Recruitment Cost\s*([+\-0-9]+)\s*%',
    'Bard_Recruitment_Cost': r'Bard Recruitment Cost\s*([+\-0-9]+)\s*%',
    'Drink_Price': r'Drink Price\s*([+\-0-9]+)\s*%',
    'Food_Price': r'Food Price\s*([+\-0-9]+)\s*%',
    'Bed_Price': r'Bed Price\s*([+\-0-9]+)\s*%',
    'Bath_Price': r'Bath Price\s*([+\-0-9]+)\s*%',
    'Steam_Bath_Price': r'Steam Bath Price\s*([+\-0-9]+)\s*%',
    'Tavern_Object_Cost': r'Tavern Object Cost\s*([+\-0-9]+)\s*%',
    'Bedroom_Object_Cost': r'Bedroom Object Cost\s*([+\-0-9]+)\s*%',
    'Kitchen_Object_Cost': r'Kitchen Object Cost\s*([+\-0-9]+)\s*%',
    'Bathroom_Object_Cost': r'Bathroom Object Cost\s*([+\-0-9]+)\s*%',
    'Cellar_Object_Cost': r'Cellar Object Cost\s*([+\-0-9]+)\s*%',
    'Experience_Modifier': r'Experience Modifier\s*([+\-0-9]+)\s*%',
    'Reputation_Modifier': r'Reputation Modifier\s*([+\-0-9]+)\s*%',
}

def extract_day(text):
    match = re.search(r"Day\s*:? ?(\d+)", text)
    if match:
        return int(match.group(1))
    return None

def parse_stats(text):
    data = {}
    for key, pat in PATTERNS.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            data[key] = m.group(1)
        else:
            data[key] = None
    return data

def screenshot_region(mss_ctx, region):
    img = mss_ctx.grab({
        "top": region["top"],
        "left": region["left"],
        "width": region["width"],
        "height": region["height"]
    })
    return Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')

csv_path = "game_stats.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=COLUMNS)

last_saved_day = None

print("Iniciando coleta (pressione Ctrl+C para encerrar)...")
try:
    with mss.mss() as sct:
        while True:
            day_img = screenshot_region(sct, REGION_DAY)
            day_img = preprocess_img(day_img)
            day_text = pytesseract.image_to_string(day_img, lang="eng")
            current_day = extract_day(day_text)

            if current_day is None:
                print("Dia não encontrado. Ajuste a região do OCR.")
                time.sleep(5)
                continue

            stats_img_1 = screenshot_region(sct, REGION_STATS_1)
            stats_img_2 = screenshot_region(sct, REGION_STATS_2)
            stats_img_1 = preprocess_img(stats_img_1)
            stats_img_2 = preprocess_img(stats_img_2)
            stats_text_1 = pytesseract.image_to_string(stats_img_1, lang="eng")
            stats_text_2 = pytesseract.image_to_string(stats_img_2, lang="eng")
            stats_text = stats_text_1 + "\n" + stats_text_2

            print("\n===== TEXTO OCR CONCATENADO =====\n", stats_text, "\n===============================\n")

            with open("ocr_debug.txt", "w", encoding="utf-8") as f:
                f.write(stats_text)

            if last_saved_day is None:
                last_saved_day = current_day
                print(f"Primeira leitura: Dia {current_day}. Aguardando mudança para salvar os dados do dia {current_day}...")
                time.sleep(8)
                continue

            if current_day > last_saved_day:
                data_row = {'Day': last_saved_day}
                stats_data = parse_stats(stats_text)
                data_row.update(stats_data)
                print("Linha extraída:", data_row)
                df = pd.concat([df, pd.DataFrame([data_row])], ignore_index=True)
                df.to_csv(csv_path, index=False)
                print(f"Dados do dia {last_saved_day} salvos!")
                last_saved_day = current_day
            else:
                print(f"Dia atual: {current_day} | Esperando mudar para coletar dados...")
            time.sleep(8)

except KeyboardInterrupt:
    print("Coleta encerrada pelo usuário. Salvando dataset...")
    df.to_csv(csv_path, index=False)
    print("Finalizado.")
