from requests import Session
import telebot
from urllib3.exceptions import InsecureRequestWarning
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from db import TOKEN, USER_ID, message, count_falhas, cout_vela

bot = telebot.TeleBot(TOKEN)
user_id = USER_ID

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3")

driver = webdriver.Chrome(options=options)

driver.get('https://stake.games/casino/games/crash')
time.sleep(1)

valores_capturados = set()
cont = 0

lista = []

while True:
    time.sleep(0.5)
    try:
        spans = driver.find_elements(By.XPATH, '//button[contains(@class, "variant-")]//span')
        
        for span in spans:
            valor = span.text.strip().replace("×", "").replace("x", "")  
            if valor and valor not in valores_capturados:
                valores_capturados.add(valor)
                
                try:
                    # Remove pontos e troca a vírgula pelo ponto
                    numero = float(valor.replace('.', '').replace(',', '.'))
                    print(f"📌 Result: {numero}")
                    alerta_msg = f"⚠️ Alert! Only 1 more to reach the limit of {count_falhas}..\n\n📈 Last value: {numero}x"
                    alerta = bot.send_message(user_id, alerta_msg, parse_mode='HTML', disable_web_page_preview=True)
                    lista.append(numero)
                    
                    # Mantém no máximo 'count_falhas' elementos
                    if len(lista) > count_falhas:
                        lista.pop(0)
                    
                    if numero < float(cout_vela):
                        cont += 1
                        
                        if cont == count_falhas - 1:
                            alerta_msg = f"⚠️ Alert! Only 1 more to reach the limit of {count_falhas}..\n\n📈 Last value: {numero}x"
                            alerta = bot.send_message(user_id, alerta_msg, parse_mode='HTML', disable_web_page_preview=True)

                    else:
                        try:
                            bot.delete_message(user_id, alerta.message_id)
                        except:
                            pass
                        cont = 0
                    
                    if cont == count_falhas:
                        try:
                            bot.delete_message(user_id, alerta.message_id)
                        except:
                            pass
                        cont = 0
                        
                        print('Atenção: encontrou o sinal')
                        msg = f"{message}\n\n📈 {numero}x 📉\n\nResults: {lista}"
                        bot.send_message(user_id, msg, parse_mode='HTML', disable_web_page_preview=True)

                except ValueError:
                    print(f"⚠️ Valor inválido: {valor}")

    
    except Exception as e:
        print(e)
        pass