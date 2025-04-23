import telebot
import requests

TOKEN = "AQUI_TU_TOKEN_DEL_BOT"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'parley'])
def enviar_parley(message):
    url = "http://localhost:5000/parley_seguro_vida_json"
    try:
        res = requests.get(url)
        datos = res.json()

        if "error" in datos:
            bot.reply_to(message, f"⚠️ {datos['error']}")
            return

        parlays = datos.get("parleys", [])
        for p in parlays:
            texto = f"""
<b>{p['nombre']}</b>
🎯 Cuota Total: {p['cuota_total']}
📈 Probabilidad: {round(p['probabilidad']*100, 2)}%
💰 Inversión: {p['inversion']} soles
🧮 VE: {p['valor_esperado']}
🔐 Código SAMPRO: {p['codigo_sampro']}
"""
            for pick in p['picks']:
                texto += f"• {pick['partido']} — {pick['mercado']} — Cuota: {pick['cuota']} — Confianza: {pick['confianza']}%\n"

            bot.send_message(message.chat.id, texto, parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

print("🤖 Bot activo. Esperando comandos /start o /parley")
bot.polling()
