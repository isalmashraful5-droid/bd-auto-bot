from flask import Flask, request
import telebot

TOKEN = "8658276400:AAFhnhmzujZDfaYxPy_8iyUXURaEh4-0pFU"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

users = {}
requests_db = {}

@app.route('/')
def home():
    return "Bot Running"

@bot.message_handler(commands=['start'])
def start(msg):
    users[msg.chat.id] = {"balance":0}
    bot.send_message(msg.chat.id, "Welcome!\n/deposit\n/withdraw\n/balance")

@bot.message_handler(commands=['balance'])
def balance(msg):
    bal = users[msg.chat.id]["balance"]
    bot.send_message(msg.chat.id, f"Balance: {bal} TK")

@bot.message_handler(commands=['deposit'])
def deposit(msg):
    bot.send_message(msg.chat.id, "Send money to: 01XXXXXXXXX\nThen send: amount last4digit")

@bot.message_handler(func=lambda m: True)
def handle(msg):
    try:
        amount, last4 = msg.text.split()
        requests_db[last4] = {"amount": int(amount), "user": msg.chat.id}
        bot.send_message(msg.chat.id, "Request received. Wait for auto confirmation.")
    except:
        pass

@app.route('/sms', methods=['POST'])
def sms():
    data = request.json
    amount = data['amount']
    last4 = data['phone'][-4:]

    if last4 in requests_db:
        req = requests_db[last4]
        if req['amount'] == amount:
            uid = req['user']
            users[uid]["balance"] += amount
            bot.send_message(uid, f"Deposit Success: {amount} TK")

    return "ok"

if __name__ == "__main__":
    bot.infinity_polling()
