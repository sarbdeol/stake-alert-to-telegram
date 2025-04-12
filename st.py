import asyncio
import telebot
from playwright.async_api import async_playwright
import time
from db import TOKEN, USER_ID, message, count_falhas, cout_vela

# Initialize Telegram bot
bot = telebot.TeleBot(TOKEN)
user_id = USER_ID

async def main():
    async with async_playwright() as playwright:
        # Browser setup with Playwright
        browser = await playwright.chromium.launch(
            headless=True,  # Set to True for headless mode

        )

        # Create a context with specific user agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3"
        )

        # Open a new page
        page = await context.new_page()
        await page.goto('https://stake.games/casino/games/crash')
        print('start')
        await asyncio.sleep(1)

        valores_capturados = set()
        cont = 0
        lista = []
        alerta = None  # Initialize alert message object

        while True:
            await asyncio.sleep(0.5)
            try:
                # Find elements using Playwright's selector
                spans = await page.query_selector_all('button[class*="variant-"] span')

                for span in spans:
                    valor = await span.inner_text()
                    valor = valor.strip().replace("×", "").replace("x", "")

                    if valor and valor not in valores_capturados:
                        valores_capturados.add(valor)

                        try:
                            # Remove dots and replace comma with dot for float conversion
                            numero = float(valor.replace('.', '').replace(',', '.'))
                            print(f"📌 Result: {numero}")
                            lista.append(numero)

                            # Keep only the last 'count_falhas' elements
                            if len(lista) > count_falhas:
                                lista.pop(0)

                            if numero < float(cout_vela):
                                cont += 1

                                if cont == count_falhas - 1:
                                    alerta_msg = f"⚠️ Alert! Only 1 more to reach the limit of {count_falhas}..\n\n📈 Last value: {numero}x"
                                    alerta = bot.send_message(user_id, alerta_msg, parse_mode='HTML', disable_web_page_preview=True)
                            else:
                                try:
                                    if alerta:
                                        bot.delete_message(user_id, alerta.message_id)
                                except Exception:
                                    pass
                                cont = 0

                            if cont == count_falhas:
                                try:
                                    if alerta:
                                        bot.delete_message(user_id, alerta.message_id)
                                except Exception:
                                    pass
                                cont = 0

                                print('Atenção: encontrou o sinal')
                                msg = f"{message}\n\n📈 {numero}x 📉\n\nResults: {lista}"
                                bot.send_message(user_id, msg, parse_mode='HTML', disable_web_page_preview=True)
                        except ValueError:
                            print(f"⚠️ Valor inválido: {valor}")

            except Exception as e:
                print(f"An error occurred: {e}")
                pass

if __name__ == "__main__":
    asyncio.run(main())