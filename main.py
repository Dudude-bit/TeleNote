import telebot
import sql

TOKEN = '1109252246:AAElFSsGAb7Y_fa_sGbUlnbnKfe-3ZwPH0c'

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def handling_start(message: telebot.types.Message) :
    kb = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text='Добавить заметку', callback_data='add_note')
    kb.add(btn1)
    bot.send_message(message.chat.id,
                     'Здравствуйте, это простой бот, который Вам поможет сохранять заметки. Для более подробной информации введите команду /help',
                     reply_markup=kb)


@bot.message_handler(commands=['help'])
def handling_help(message: telebot.types.Message) :
    text = """
    Здравствуйте, это простой бот, который Вам будет поомгать сохранять заметки, не выходя из Telegram. Бот также поддерживает сохранения из другого чата, для этого просто можно ввести название бота через @, а затем ввести то, что Вы хотите.
    """
    bot.send_message(message.chat.id, text=text)
