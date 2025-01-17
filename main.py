import telebot
import db

TOKEN = '1109252246:AAElFSsGAb7Y_fa_sGbUlnbnKfe-3ZwPH0c'

bot = telebot.TeleBot(token=TOKEN)

step_dict = dict()

START, ADD_NOTE_TITLE, ADD_NOTE, SEARCH = range(4)

title_dict = dict()


def create_kb() :
    kb = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text='Добавить заметку', callback_data='add_note')
    btn2 = telebot.types.InlineKeyboardButton(text='Показать Все заметки', callback_data='show_note')
    btn3 = telebot.types.InlineKeyboardButton(text='Удалить все заметки', callback_data='del_notes')
    btn4 = telebot.types.InlineKeyboardButton(text='Искать среди заметок', callback_data='search')
    kb.row(btn1, btn2)
    kb.row(btn3)
    kb.row(btn4)
    return kb


@bot.message_handler(commands=['start'])
def handling_start(message: telebot.types.Message) :
    kb = create_kb()
    bot.send_message(message.chat.id,
                     'Здравствуйте, это простой бот, который Вам поможет сохранять заметки. Для более подробной информации введите команду /help',
                     reply_markup=kb)


@bot.callback_query_handler(func=lambda m : m.data == 'start')
def handling_to_start(callback_query: telebot.types.CallbackQuery) :
    kb = create_kb()
    bot.edit_message_text(
        text='Здравствуйте, это простой бот, который Вам поможет сохранять заметки. Для более подробной информации введите команду /help',
        chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=kb)


@bot.message_handler(commands=['help'])
def handling_help(message: telebot.types.Message) :
    text = """
    Здравствуйте, это простой бот, который Вам будет помогать сохранять заметки, не выходя из Telegram. Бот также поддерживает сохранения из другого чата, для этого просто можно ввести название бота через @, а затем ввести то, что Вы хотите.
    """
    bot.send_message(message.chat.id, text=text)


@bot.callback_query_handler(func=lambda x : x.data == 'add_note')
def adding_note(callback_query: telebot.types.CallbackQuery) :
    step_dict[callback_query.from_user.id] = ADD_NOTE_TITLE
    bot.send_message(callback_query.message.chat.id, text='Введите название Вашей заметки')


@bot.message_handler(content_types=['text'], func=lambda x : step_dict.get(x.from_user.id, START) == ADD_NOTE_TITLE)
def add_note_title(message: telebot.types.Message) :
    note_title = message.text
    user_id = message.from_user.id
    title_dict[user_id] = note_title
    step_dict[message.from_user.id] = ADD_NOTE
    bot.send_message(message.chat.id, 'Введите теперь Вашу заметку')


@bot.message_handler(content_types=['text'], func=lambda x : step_dict.get(x.from_user.id, START) == ADD_NOTE)
def add_note(message: telebot.types.Message) :
    title = title_dict.pop(message.from_user.id)
    text = message.text
    user_id = message.from_user.id
    connection = db.create_connection()
    db.create_note(connection, title, text, user_id)
    kb = create_kb()
    bot.send_message(message.chat.id, text='Вы добавили заметку', reply_markup=kb)
    connection.close()


@bot.callback_query_handler(func=lambda m : m.data == 'show_note')
def show_note(callback_query: telebot.types.CallbackQuery) :
    user_id = callback_query.from_user.id
    connection = db.create_connection()
    notes = db.get_notes(connection, user_id)
    kb = telebot.types.InlineKeyboardMarkup(row_width=1)
    for note in notes :
        kb.add(telebot.types.InlineKeyboardButton(text=note[3], callback_data=f'note_{note[0]}'))
    kb.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='start'))
    bot.edit_message_reply_markup(callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                  reply_markup=kb)
    connection.close()


@bot.callback_query_handler(func=lambda x : x.data.startswith('note'))
def get_one_note(message) :
    connection = db.create_connection()
    note_id = message.data.replace('note_', '')
    note = db.get_one_note(connection, note_id)[1]
    bot.send_message(message.message.chat.id, note)
    connection.close()


@bot.callback_query_handler(func=lambda m : m.data == 'del_notes')
def delete_all_note(callback_query: telebot.types.CallbackQuery) :
    user_id = callback_query.from_user.id
    connection = db.create_connection()
    db.delete_all_notes(connection, user_id)
    connection.close()
    bot.answer_callback_query(callback_query.id, text='Все заметки были удалены', show_alert=True)


@bot.inline_handler(func=lambda x : True)
def handling_inline(inline_query: telebot.types.InlineQuery) :
    text = inline_query.query
    q = telebot.types.InlineQueryResultArticle(
        id='1',
        title='Сохранить заметку',
        description='Сохранить введенную заметку',
        input_message_content=telebot.types.InputTextMessageContent(
            message_text='Заметка сохранена'
        )
    )
    bot.answer_inline_query(inline_query.id, [q])


@bot.callback_query_handler(func=lambda m : m.data == 'search')
def search_note(callback_query) :
    text = 'Ты можешь найти заметку среди их названий и текста. Для этого просто введи текст,который Вы хотите найти'
    bot.send_message(callback_query.message.chat.id, text=text)
    step_dict[callback_query.from_user.id] = SEARCH


@bot.message_handler(content_types=['text'], func=lambda m : step_dict[m.from_user.id] == SEARCH)
def searching_notes(message) :
    connection = db.create_connection()
    searching_query = message.text
    notes = db.search_notes(connection, searching_query)
    connection.close()
    kb = telebot.types.InlineKeyboardMarkup(row_width=1)
    for note in notes :
        kb.add(telebot.types.InlineKeyboardButton(text=note[3], callback_data=f'note_{note[0]}'))
    kb.add(telebot.types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='start'))
    bot.send_message(message.chat.id, text='Выберите заметку', reply_markup=kb)


bot.polling()
