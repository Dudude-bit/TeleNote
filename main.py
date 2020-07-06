import telebot
import db


TOKEN = '1109252246:AAElFSsGAb7Y_fa_sGbUlnbnKfe-3ZwPH0c'

bot = telebot.TeleBot(token=TOKEN)

step_dict = dict()

START, ADD_NOTE_TITLE ,ADD_NOTE = range(3)


title_dict = dict()


@bot.message_handler(commands=['start'])
def handling_start(message: telebot.types.Message) :
    kb = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text='Добавить заметку', callback_data='add_note')
    btn2 = telebot.types.InlineKeyboardButton(text='Показать Все заметки', callback_data='show_note')
    kb.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     'Здравствуйте, это простой бот, который Вам поможет сохранять заметки. Для более подробной информации введите команду /help',
                     reply_markup=kb)


@bot.message_handler(commands=['help'])
def handling_help(message: telebot.types.Message) :
    text = """
    Здравствуйте, это простой бот, который Вам будет помогать сохранять заметки, не выходя из Telegram. Бот также поддерживает сохранения из другого чата, для этого просто можно ввести название бота через @, а затем ввести то, что Вы хотите.
    """
    bot.send_message(message.chat.id, text=text)


@bot.callback_query_handler(func=lambda x: x.data == 'add_note')
def adding_note(callback_query: telebot.types.CallbackQuery):
    step_dict[callback_query.from_user.id] = ADD_NOTE_TITLE
    bot.send_message(callback_query.message.chat.id, text='Введите название Вашей заметки')


@bot.message_handler(content_types=['text'], func=lambda x: step_dict.get(x.from_user.id, START) == ADD_NOTE_TITLE)
def add_note_title(message: telebot.types.Message):
    note_title = message.text
    user_id = message.from_user.id
    title_dict[user_id] = note_title
    step_dict[message.from_user.id] = ADD_NOTE
    bot.send_message(message.chat.id, 'Введите теперь Вашу заметку')

@bot.message_handler(content_types=['text'], func=lambda x: step_dict.get(x.from_user.id, START) == ADD_NOTE)
def add_note(message: telebot.types.Message):
    title = title_dict.pop(message.from_user.id)
    text = message.text
    user_id = message.from_user.id
    connection = db.create_connection()
    db.create_note(connection, title, text, user_id)
    bot.send_message(message.chat.id, 'Вы добавили заметку')
    connection.close()

@bot.callback_query_handler(func=lambda m:m.data == 'show_note')
def show_note(callback_query: telebot.types.CallbackQuery):
    user_id = callback_query.from_user.id
    connection = db.create_connection()
    notes = db.get_notes(connection, user_id)
    for note in notes:
        bot.send_message(callback_query.message.chat.id, note[1])
    connection.close()


bot.polling()