import telebot
import subprocess

# 🔐 Token de tu bot
BOT_TOKEN = "8175598995:AAH1NoEVhzfKOa4LvOEqcloip8BmY5MJ0Dc"
bot = telebot.TeleBot(BOT_TOKEN)

# 🟢 Comando inicial
@bot.message_handler(commands=["start", "ayuda"])
def bienvenida(mensaje):
    bot.reply_to(mensaje, "👋 Hola jefe, soy tu bot SAMPRO.\nEscribe /actualizar para ejecutar el scraping de Bet365.")

# 🔁 Comando para actualizar cuotas
@bot.message_handler(commands=["actualizar"])
def ejecutar_scraping(mensaje):
    bot.reply_to(mensaje, "⚙️ Ejecutando scraping de Bet365...")
    try:
        resultado = subprocess.run(["python", "utils/apis/bot_bet365.py"], capture_output=True, text=True)
        if resultado.returncode == 0:
            bot.send_message(mensaje.chat.id, "✅ Archivo actualizado correctamente.")
        else:
            bot.send_message(mensaje.chat.id, f"❌ Error:\n{resultado.stderr}")
    except Exception as e:
        bot.send_message(mensaje.chat.id, f"❌ Fallo al ejecutar: {str(e)}")

# 🛰️ Activa el bot
bot.polling()
