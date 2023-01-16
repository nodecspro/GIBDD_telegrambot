import sqlite3
from cgitb import html
import telebot
from io import BytesIO
from docxtpl import DocxTemplate
from telebot import types
from telebot.types import InlineKeyboardButton
import hashlib

doc = DocxTemplate("Выходной документ.docx")

autoinfo = r'''f"""
Данные об авто:

1) Номер ТС: {x[0]}
2) Номер кузова: {x[1]}
3) Номер двигателя: {x[2]}
4) Марка автомобиля: {x[3]}
5) Модель автомобиля: {x[4]}
6) Цвет автомобиля: {x[5]}
7) Объем двигателя: {x[6]} л.
8) Примечание для авто: {x[7]}
9) Расположение руля: {x[8]}
10) Привод авто: {x[9]}
11) Год выпуска: {x[10]}
12) Тип кузова: {x[11]}
13) Находится ли авто в угоне? - {x[12]}
14) Дата угона: {x[13]}
15) Тип владельца: {x[14]}                             (Физ. лицо - 1, Юр. лицо - 0)
"""'''

autoinfoedit = r'''f"""
Данные об авто:

1) Номер ТС: {x[0]}
2) Номер кузова: {x[1]}
3) Номер двигателя: {x[2]}
4) Марка автомобиля: {x[3]}
5) Модель автомобиля: {x[4]}
6) Цвет автомобиля: {x[5]}
7) Объем двигателя: {x[6]} л.
8) Примечание для авто: {x[7]}
9) Расположение руля: {x[8]}
10) Привод авто: {x[9]}
11) Год выпуска: {x[10]}
12) Тип кузова: {x[11]}
13) Находится ли авто в угоне? - {x[12]}
14) Дата угона: {x[13]}
15) Тип владельца: {x[14]}                             (Физ. лицо - 1, Юр. лицо - 0)
"""'''

new_auto = [
    """
Введите ответы на следующие вопросы:
(Ответы осуществляются посредством ввода через Enter)

1) Номер ТС*
(Пример: А111АА111, ввод происходит кириллицей)
2) Номер кузова*
3) Номер двигателя*
4) Марка автомобиля*
5) Модель автомобиля*
6) Цвет автомобиля*
7) Объем двигателя*
8) Примечание для авто
9) Расположение руля*
10) Привод авто*
11) Год выпуска*
12) Тип кузова*
13) Находится ли авто в угоне?* 
(Да/Нет)
14) Дата угона
(Автомобиль не угнан? Введите - Нет. Угнан? - дату угона.)
(Пример: 12.12.2012)
15) Тип владельца*
(Физ. лицо - 1, Юр. лицо - 0)

Поля помеченные "*" - обязательные
"""
]

new_vladelec = [
    """
Введите ответы на следующие вопросы:
(Ответы осуществляются посредством ввода через Enter)

1) ФИО*
2) Номер телефона*
3) Адрес проживания*
4) Номер ТС*
5) Номер кузова ТС*
6) Номер двигателя ТС*

Поля помеченные "*" - обязательные
"""
]

new_org = [
    """
Введите ответы на следующие вопросы:
(Ответы осуществляются посредством ввода через Enter)

1) ИНН*
2) Название организации*
3) ФИО начальника*
4) Адрес*
5) Номер телефона*
6) Номер ТС*
7) Номер кузова ТС*
8) Номер двигателя ТС*

Поля помеченные "*" - обязательные
"""
]

new_insp = [
    """
Введите ответы на следующие вопросы:
(Ответы осуществляются посредством ввода через Enter)

1) ФИО*
2) День рождение*
3) ID тех. осмотра*

Поля помеченные "*" - обязательные
"""
]

OwnerInfo = r'''f"""
Информация о владельце:

1) ФИО: {x[1]}
2) Номер телефона: {x[2]}
3) Адрес проживания: {x[3]}
4) Номер ТС: {x[4]}
5) Номер кузова ТС: {x[5]}
6) Номер двигателя ТС: {x[6]}

"""'''

OrgInfo = r'''f"""
Информация об организации:

1) ИНН: {x[0]}
2) Название: {x[1]}
3) ФИО владельца организации: {x[2]}
4) Адрес: {x[3]}
5) Номер телефона: {x[4]}
"""'''

ToNew = [
    """
Введите ответы на следующие вопросы:
(Ответы осуществляются посредством ввода через Enter)

1) Дата осмотра ТС:*
2) ID инспектора: *
3) Годовой налог на авто:* 
4) Стоимость ТО: 
5) Статус технического осмотра:* 
6) Причины по которым ТО не было пройдено:
7) Номер ТС: *
8) Номер кузова: *
9) Номер двигателя: *

Поля помеченные "*" - обязательные
"""
]

ToInfo = r'''f"""
Данные о ТО:

1) ID Тех. осмотра: {x[0]}
2) Дата осмотра ТС: {x[1]}
3) ID инспектора: {x[2]}
4) Годовой налог на авто: {x[3]} руб.
5) Стоимость ТО: {x[4]} руб.
6) Статус технического осмотра: {x[5]}
7) Причины по которым ТО не было пройдено: {x[6]}
8) Номер ТС: {x[7]}
9) Номер кузова: {x[8]}
10) Номер двигателя: {x[9]}
"""'''

ToInfoedit = r'''f"""
Данные о ТО:

ID Тех. осмотра: {x[0]}
2) Дата осмотра ТС: {x[1]}
3) ID инспектора: {x[2]}
4) Годовой налог на авто: {x[3]} руб.
5) Стоимость ТО: {x[4]} руб.
6) Статус технического осмотра: {x[5]}
7) Причины по которым ТО не было пройдено: {x[6]}
Номер ТС: {x[7]}
Номер кузова: {x[8]}
Номер двигателя: {x[9]}
"""'''

answers = []

bot = telebot.TeleBot("5243511593:AAHGAPyiDax6hZCPoYO_b581PXsNs2eYoFM")
sqlite_connection = sqlite3.connect('dbpr.db', check_same_thread=False)
cursor = sqlite_connection.cursor()


def next_step(id, step):
    try:
        user = []
        user = sqlite_connection.execute('SELECT id FROM users WHERE id = ?',
                                         (id, )).fetchone()[0]
        if not user:
            sqlite_connection.execute(
                'INSERT INTO users (step, ID) values (?,?)', (
                    step,
                    id,
                ))
            sqlite_connection.commit()
        else:
            sqlite_connection.execute('UPDATE users SET step = ? WHERE ID = ?',
                                      (
                                          step,
                                          id,
                                      ))
            sqlite_connection.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)


def numberauto(id, numberauto):
    sqlite_connection.execute('UPDATE users SET Numberauto = ? WHERE ID = ?', (
        numberauto,
        id,
    ))
    sqlite_connection.commit()


def EngineIDauto(id, EngineIDauto):
    sqlite_connection.execute('UPDATE users SET EngineIDauto = ? WHERE ID = ?',
                              (
                                  EngineIDauto,
                                  id,
                              ))
    sqlite_connection.commit()


def BodyIDauto(id, BodyIDauto):
    sqlite_connection.execute('UPDATE users SET BodyIDAuto = ? WHERE ID = ?', (
        BodyIDauto,
        id,
    ))
    sqlite_connection.commit()


def loginreg(id, login):
    sqlite_connection.execute('UPDATE users SET login = "?" WHERE ID = ?', (
        login,
        id,
    ))
    sqlite_connection.commit()


def passreg(id, password):
    sqlite_connection.execute('UPDATE users SET password = "?" WHERE ID = (?)',
                              (
                                  password,
                                  id,
                              ))
    sqlite_connection.commit()


def get_button(x):
    return types.ReplyKeyboardMarkup(row_width=x, resize_keyboard=True)


# Главное меню
mainmenu = get_button(2).add('🔍 Поиск ТС', '➕ Добавление ТС',
                             '➕ Добавление инспектора', '💼 Профиль')

# Авто найдено
automenu = get_button(3).add('👨 Информация о владельце',
                             '📝 Редактировать информацию ТС',
                             '📝 Редактировать информацию о ТО',
                             '📄 Получить документ', '📝 Информация о ТО',
                             '♻️ Удаление авто', '🚪 Главное меню')
# Поиск авто
searchauto = get_button(3).add('🔍 Поиск по номеру ТС',
                               '🔍 Поиск по номеру кузова',
                               '🔍 Поиск по номеру двигателя', '🚪 Главное меню')
# Изменить владельцев
editownersmenu = get_button(3).add('🔀 Изменить владельца',
                                   '👨 Добавление владельца', '⬅️ Назад')
# Регистрация, вход и выход аккаунта
reg = get_button(2).add('🔑Войти', '📝Регистрация', '🚪 Главное меню')
logout = get_button(3).add('📝Изменить логин или пароль', '♻️Удалить аккаунт',
                           '📊Статистика', '🚪 Выйти из аккаунта',
                           '🚪 Главное меню')

#Изменить логин или пароль аккаунта
editaccount = get_button(2).add('📝Изменить логин', '📝Изменить пароль',
                                '🚪 Главное меню')
delaccount = get_button(2).add('✅Да', '🚫Нет')

#Добавление ТО
addTO = get_button(2).add('📝 Добавить информацию о прохождении ТО', '⬅️ Назад')

# Выход
exit = get_button(1).add('🚪 Главное меню')

# Назад
back = get_button(1).add('↩️ Назад')
back1 = get_button(1).add('⬅️ Назад')
back2 = get_button(1).add('◀️ Назад')
back3 = get_button(1).add('🔙 Назад')


@bot.message_handler(commands=['start', 's', 'help', 'h'])
def start(message):
    mess = f'Привет👋, <b>{message.from_user.first_name}</b>, ты запустил сервис ГИБДД.\nДля продолжения выберите нужную вам категорию👇'
    bot.send_message(message.chat.id,
                     mess,
                     reply_markup=mainmenu,
                     parse_mode='html')
    next_step(message.from_user.id, 1)


@bot.message_handler(content_types=[
    'text', 'document', 'audio', 'photo', 'video', 'voice', 'location',
    'contact', 'sticker'
])
def start_quest(message):
    step = sqlite_connection.execute('SELECT step FROM users WHERE id = ?',
                                     (message.from_user.id, )).fetchall()[0][0]

    if message.text == '🚪 Главное меню':
        bot.send_message(message.from_user.id,
                         'Вы вернулись в главное меню',
                         reply_markup=mainmenu)
        next_step(message.from_user.id, 1)

    elif message.text == '↩️ Назад':
        bot.send_message(message.from_user.id,
                         'Вы вернулись назад',
                         reply_markup=searchauto)
        next_step(message.from_user.id, 2)

    elif message.text == '⬅️ Назад':
        bot.send_message(message.from_user.id,
                         'Вы вернулись назад',
                         reply_markup=automenu)
        next_step(message.from_user.id, 7)

    elif message.text == '◀️ Назад':
        bot.send_message(message.from_user.id,
                         'Вы вернулись назад',
                         reply_markup=editownersmenu)
        next_step(message.from_user.id, 7)

    elif message.text == '🔙 Назад':
        bot.send_message(message.from_user.id,
                         'Вы вернулись назад',
                         reply_markup=reg)
        next_step(message.from_user.id, 17)

    elif message.text == '📝 Добавить информацию о прохождении ТО':
        bot.send_message(message.from_user.id, text=ToNew, reply_markup=back1)
        next_step(message.from_user.id, 12)

    elif message.text == "🔍 Поиск ТС":
        bot.send_message(message.chat.id,
                         'Выберите метод поиска ТС.',
                         reply_markup=searchauto)
        next_step(message.from_user.id, 2)

    elif message.text == '🔍 Поиск по номеру ТС' and step == 2:
        bot.send_message(message.chat.id,
                         f'Введите номер ТС: \n<b>Пример: А111АА111</b>',
                         parse_mode='html',
                         reply_markup=back)
        next_step(message.from_user.id, 3)

    elif message.text == "💼 Профиль":
        try:
            x = sqlite_connection.execute(
                'SELECT enter FROM account WHERE userid = ?',
                (message.from_user.id, )).fetchall()[0]
            if x == (1, ):
                bot.send_message(message.chat.id,
                                 'Вы уже авторизованы.',
                                 reply_markup=logout)
                next_step(message.from_user.id, 17)
            else:
                bot.send_message(
                    message.chat.id,
                    f'Нет аккаунта? - зарегистрируйте.\nЕсть аккаунт? - войдите.',
                    parse_mode='html',
                    reply_markup=reg)
                next_step(message.from_user.id, 17)
        except Exception as e:
            print(e)
            bot.send_message(
                message.chat.id,
                f'Нет аккаунта? - зарегистрируйте.\nЕсть аккаунт? - войдите.',
                parse_mode='html',
                reply_markup=reg)
            next_step(message.from_user.id, 17)

    elif message.text == "🚪 Выйти из аккаунта":
        sqlite_connection.execute(
            'UPDATE account SET enter = 0 WHERE userid = ?',
            (message.from_user.id, ))
        sqlite_connection.commit()
        bot.send_message(message.chat.id,
                         '✅ Вы успешно вышли из аккаунта.',
                         reply_markup=reg)
        next_step(message.from_user.id, 17)

    elif step == 3:
        numberauto(message.from_user.id, message.text)
        try:
            x = sqlite_connection.execute(
                'SELECT * FROM Auto WHERE Number = ?',
                (message.text, )).fetchall()[0]
            bot.send_message(message.chat.id,
                             eval(autoinfo),
                             reply_markup=automenu)
        except Exception as e:
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: ТС не найдено. Проверьте номер или добавьте новую машину.'
            )
        next_step(message.from_user.id, 7)

    elif message.text == '🔍 Поиск по номеру кузова' and step == 2:
        bot.send_message(message.chat.id,
                         'Введите номер кузова:',
                         reply_markup=back)
        next_step(message.from_user.id, 4)

    elif step == 4:
        try:
            EngineIDauto(message.from_user.id, message.text)
            x = sqlite_connection.execute(
                'SELECT * FROM Auto WHERE BodyID = ?',
                (message.text, )).fetchall()[0]
            bot.send_message(message.chat.id,
                             eval(autoinfo),
                             reply_markup=automenu)
            next_step(message.from_user.id, 7)

        except Exception as e:
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: ТС не найдено. Проверьте номер или добавьте новую машину.'
            )

    elif message.text == '🔍 Поиск по номеру двигателя' and step == 2:
        bot.send_message(message.chat.id,
                         'Введите номер двигателя:',
                         reply_markup=back)
        next_step(message.from_user.id, 5)

    elif step == 5:
        try:
            BodyIDauto(message.from_user.id, message.text)
            x = sqlite_connection.execute(
                'SELECT * FROM Auto WHERE EngineID = ?',
                (message.text, )).fetchall()[0]
            bot.send_message(message.chat.id,
                             eval(autoinfo),
                             reply_markup=automenu)
            next_step(message.from_user.id, 7)

        except Exception as e:
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: ТС не найдено. Проверьте номер или добавьте новую машину.'
            )

    elif message.text == '➕ Добавление ТС':
        bot.send_message(message.from_user.id,
                         text=new_auto,
                         reply_markup=exit)
        next_step(message.from_user.id, 6)

    elif step == 6:
        try:
            info = []
            for i in message.text.split('\n'):
                info.append(i)
            boolean14 = 1 if info[14] == '1' else '0'
            sqlite_connection.execute(
                'INSERT INTO Auto (Number, BodyID, EngineID, Brand, Model, Color, Volume, Comment, Helm, Drive, Year, TypeBody, DrivingAway, DateAway, OwnerType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    info[0],
                    info[1],
                    info[2],
                    info[3],
                    info[4],
                    info[5],
                    float(info[6]),
                    info[7],
                    info[8],
                    info[9],
                    info[10],
                    info[11],
                    info[12],
                    info[13],
                    boolean14,
                ))
            sqlite_connection.commit()
            bot.send_message(message.from_user.id, '✅ТС успешно добавлено')
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫Ошибка: Проверьте ввод данных. ')

    elif message.text == '👨 Информация о владельце' and step == 7:
        try:
            ts = []
            ts = sqlite_connection.execute(
                'SELECT OwnerType FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, )).fetchall()[0]
            if ts[0] == '1':
                x = []
                x = sqlite_connection.execute(
                    'SELECT * FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                    (message.from_user.id, )).fetchall()[0]
                bot.send_message(message.from_user.id,
                                 eval(OwnerInfo),
                                 reply_markup=editownersmenu)
            else:
                x = []
                x = sqlite_connection.execute(
                    'SELECT * FROM AutoOrg WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                    (message.from_user.id, )).fetchall()[0]
                bot.send_message(message.from_user.id,
                                 eval(OrgInfo),
                                 reply_markup=editownersmenu)
        except:
            bot.send_message(message.from_user.id,
                             'У авто нет владельцев. Добавьте его.',
                             reply_markup=editownersmenu)

    elif message.text == '👨 Добавление владельца' and step == 7:
        bot.send_message(message.from_user.id,
                         text=new_vladelec,
                         reply_markup=back2)
        next_step(message.from_user.id, 16)

    elif step == 16:
        try:
            info = []
            for i in message.text.split('\n'):
                info.append(i)
            sqlite_connection.execute(
                'INSERT INTO AutoVladelca (OwnerFIO, OwnerPhone, OwnerAddress, AutoNumber, AutoBodyID, AutoEngineID) VALUES (?, ?, ?, ?, ?, ?)',
                (
                    info[0],
                    info[1],
                    info[2],
                    info[3],
                    info[4],
                    info[5],
                ))
            sqlite_connection.commit()
            bot.send_message(message.from_user.id,
                             '✅ Владелец успешно добавлен')
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫Ошибка: Проверьте ввод данных. ')

    elif message.text == '🔀 Изменить владельца' and step == 7:
        try:
            ts = []
            ts = sqlite_connection.execute(
                'SELECT OwnerType FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, )).fetchall()[0]

            if ts[0] == '1':
                x = []
                x = sqlite_connection.execute(
                    'SELECT * FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                    (message.from_user.id, )).fetchall()[0]
                bot.send_message(
                    message.from_user.id,
                    eval(OwnerInfo) +
                    '\nВведите номер пункта, который вы хотите редактировать',
                    reply_markup=back2)
            else:
                x = []
                x = sqlite_connection.execute(
                    'SELECT * FROM AutoOrg WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                    (message.from_user.id, )).fetchall()[0]
                bot.send_message(
                    message.from_user.id,
                    eval(OrgInfo) +
                    '\nВведите номер пункта, который вы хотите отредактировать:',
                    reply_markup=back2)

            next_step(message.from_user.id, 9)
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫Ошибка: У авто нет владельцев.')

    elif step == 9:
        if message.text == '1':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 41)
        elif message.text == '2':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 42)
        elif message.text == '3':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 43)

    elif step == 41:
        sqlite_connection.execute(
            'UPDATE AutoVladelca SET OwnerFIO = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(OwnerInfo) +
            '✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 9)

    elif step == 42:
        sqlite_connection.execute(
            'UPDATE AutoVladelca SET OwnerPhone = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(OwnerInfo) +
            '✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 9)

    elif step == 43:
        sqlite_connection.execute(
            'UPDATE AutoVladelca SET OwnerAddress = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(OwnerInfo) +
            '✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 9)

    elif message.text == '📝 Редактировать информацию ТС' and step == 7:
        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]
        bot.send_message(
            message.from_user.id,
            eval(autoinfo) +
            '\nВведите номер пункта, который вы хотите отредактировать:',
            reply_markup=back1,
        )
        next_step(message.from_user.id, 8)

    elif step == 8:
        if message.text == '1':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 51)
        elif message.text == '2':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 52)
        elif message.text == '3':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 53)
        elif message.text == '4':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 54)
        elif message.text == '5':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 55)
        elif message.text == '6':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 56)
        elif message.text == '7':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 57)
        elif message.text == '8':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 58)
        elif message.text == '9':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 59)
        elif message.text == '10':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 510)
        elif message.text == '11':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 511)
        elif message.text == '12':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 512)
        elif message.text == '13':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 513)
        elif message.text == '14':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 514)
        elif message.text == '15':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 515)
        else:
            bot.send_message(message.from_user.id,
                             "🚫 Ошибка: такого пункта нет, введите заново")

    elif step == 51:
        sqlite_connection.execute(
            'UPDATE Auto SET Number = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]
        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 52:
        sqlite_connection.execute(
            'UPDATE Auto SET BodyId = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 53:
        sqlite_connection.execute(
            'UPDATE Auto SET EngineId = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 54:
        sqlite_connection.execute(
            'UPDATE Auto SET Brand = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 55:
        sqlite_connection.execute(
            'UPDATE Auto SET Model = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 56:
        sqlite_connection.execute(
            'UPDATE Auto SET Color = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 57:
        sqlite_connection.execute(
            'UPDATE Auto SET Volume = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 58:
        sqlite_connection.execute(
            'UPDATE Auto SET Comment = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 59:
        sqlite_connection.execute(
            'UPDATE Auto SET Helm = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 510:
        sqlite_connection.execute(
            'UPDATE Auto SET Drive = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 511:
        sqlite_connection.execute(
            'UPDATE Auto SET Year = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 512:
        sqlite_connection.execute(
            'UPDATE Auto SET TypeBody = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 513:
        sqlite_connection.execute(
            'UPDATE Auto SET DrivingAway = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 514:
        sqlite_connection.execute(
            'UPDATE Auto SET DateAway = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif step == 515:
        sqlite_connection.execute(
            'UPDATE Auto SET OwnerType = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 8)

    elif message.text == '➕ Добавление инспектора' and step == 1:
        bot.send_message(message.from_user.id,
                         text=new_insp,
                         reply_markup=exit)
        next_step(message.from_user.id, 10)

    elif step == 10:
        try:
            info = []
            for i in message.text.split('\n'):
                info.append(i)
            sqlite_connection.execute(
                'INSERT INTO Inspector (InspFIO, InspDR, TOid) VALUES (?, ?, ?)',
                (
                    info[0],
                    info[1],
                    info[2],
                ))
            sqlite_connection.commit()
            bot.send_message(message.from_user.id,
                             '✅ Инспектор успешно добавлен')
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫Ошибка: Проверьте ввод данных. ')

    elif message.text == '📝 Информация о ТО' and step == 7:
        try:
            x = []
            x = sqlite_connection.execute(
                'SELECT * FROM Toauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, )).fetchall()[0]
            bot.send_message(message.from_user.id,
                             eval(ToInfo),
                             reply_markup=back1)
            next_step(message.from_user.id, 7)
        except Exception as e:
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: Запись о ТО не найдена. Проверьте номер или добавьте новое ТО.',
                reply_markup=addTO)

    elif message.text == '👨 Новый владелец' and step == 7:
        bot.send_message(message.from_user.id,
                         text=new_vladelec,
                         reply_markup=exit)
        next_step(message.from_user.id, 10)

    elif step == 10:
        try:
            info = []
            for i in message.text.split('\n'):
                info.append(i)
            sqlite_connection.execute(
                'INSERT INTO AutoVladelca (OwnerFIO, OwnerPhone, OwnerAddress, AutoNumber, BodyID, EngineID) VALUES (?, ?, ?, ?, ?, ?)',
                (
                    info[0],
                    info[1],
                    info[2],
                    info[3],
                    info[4],
                    info[5],
                ))
            sqlite_connection.commit()
            bot.send_message(message.from_user.id,
                             '✅Владелец успешно добавлен')
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫Ошибка: Проверьте ввод данных. ')

    elif step == 12:
        try:
            info = []
            for i in message.text.split('\n'):
                info.append(i)
            sqlite_connection.execute(
                'INSERT INTO TOauto (DateSee, InspID, YearTax, TOtax, Okey, Reason, AutoNumber, AutoBodyID, AutoEngineID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    info[0],
                    info[1],
                    info[2],
                    info[3],
                    info[4],
                    info[5],
                    info[6],
                    info[7],
                    info[8],
                ))
            sqlite_connection.commit()
            bot.send_message(message.from_user.id,
                             '✅ Данные о ТО успешно добавлены')
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫Ошибка: Проверьте ввод данных. ')

    elif message.text == '📝 Редактировать информацию о ТО' and step == 7:
        try:
            x = []
            x = sqlite_connection.execute(
                'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, )).fetchall()[0]
            bot.send_message(
                message.from_user.id,
                eval(ToInfoedit) +
                '\nВведите номер пункта, который вы хотите редактировать',
                reply_markup=back1)
            next_step(message.from_user.id, 14)
        except:
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: Запись о ТО не найдена. Проверьте номер или добавьте новое ТО.',
                reply_markup=addTO)

    elif step == 14:
        if message.text == '2':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 62)
        elif message.text == '3':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 63)
        elif message.text == '4':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 64)
        elif message.text == '5':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 65)
        elif message.text == '6':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 66)
        elif message.text == '7':
            bot.send_message(message.from_user.id, 'Введите ответ на пункт:')
            next_step(message.from_user.id, 67)
        else:
            bot.send_message(message.from_user.id,
                             '🚫Ошибка: Этот пункт нельзя изменить.')

    elif step == 62:
        sqlite_connection.execute(
            'UPDATE TOauto SET DateSee = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 14)

    elif step == 63:
        sqlite_connection.execute(
            'UPDATE TOauto SET InspID = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 14)

    elif step == 64:
        sqlite_connection.execute(
            'UPDATE TOauto SET YearTax = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 14)
    elif step == 65:
        sqlite_connection.execute(
            'UPDATE TOauto SET TOtax = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 14)
    elif step == 66:
        sqlite_connection.execute(
            'UPDATE TOauto SET Okey = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 14)
    elif step == 67:
        sqlite_connection.execute(
            'UPDATE TOauto SET Reason = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))
        sqlite_connection.commit()

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )
        next_step(message.from_user.id, 14)

    elif message.text == "📄 Получить документ" and step == 7:
        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]

        context = {
            'nomerts': x[0],
            'nomerkyzova': x[1],
            'nomerengine': x[2],
            'markaauto': x[3],
            'modelauto': x[4],
            'colorauto': x[5],
            'volume': x[6],
            'comment': x[7],
            'helm': x[8],
            'drive': x[9],
            'year': x[10],
            'typebody': x[11],
            'drivingaway': x[12],
            'dateaway': x[13],
            'ownertype': x[14],
            'toid': x[17]
        }

        doc.render(context)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        bot.send_document(message.from_user.id,
                          buffer,
                          caption='✅ Документ успешно сгенерирован!',
                          visible_file_name=f'{x[0]}.docx')

    elif message.text == '♻️ Удаление авто' and step == 7:
        bot.send_message(
            message.from_user.id,
            'Вы действительно хотите удалить запись об авто?\n Введите "+", если вы хотите это сделать',
            reply_markup=back1)
        next_step(message.from_user.id, 15)

    elif step == 15:
        if message.text == '+':
            sqlite_connection.execute(
                'DELETE FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM AutoOrg WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM Auto WHERE BodyID IN(SELECT BodyID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM AutoOrg WHERE AutoBodyID IN(SELECT BodyID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM AutoVladelca WHERE AutoBodyID IN(SELECT BodyID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM TOauto WHERE AutoBodyID IN(SELECT BodyID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM Auto WHERE EngineID IN(SELECT EngineID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM AutoOrg WHERE AutoEngineID IN(SELECT EngineID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM AutoVladelca WHERE AutoEngineID IN(SELECT EngineID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM TOauto WHERE AutoEngineID IN(SELECT EngineID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))

            sqlite_connection.execute(
                'DELETE FROM Inspector WHERE TOid IN(SELECT TOid FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))

            bot.send_message(message.from_user.id,
                             '✅ Авто успешно удалено',
                             reply_markup=exit)
        else:
            bot.send_message(
                message.from_user.id,
                'Для удаления необходимо написать "+", если хотиnе выйти, нажмите кнопку ниже'
            )

    elif message.text == '🔑Войти' and step == 17:
        bot.send_message(
            message.from_user.id,
            f'Введите логин и пароль (через enter) для входа в ваш аккаунт.\n<b>(Пример:\nlogin\npassword)</b>',
            reply_markup=exit,
            parse_mode='html')
        next_step(message.from_user.id, 18)

    elif step == 18:
        try:
            info = []
            for i in message.text.split('\n'):
                info.append(i)

            sqlite_connection.execute(
                'UPDATE users SET loginacc = ?, passacc = ? WHERE ID = ?', (
                    info[0],
                    info[1],
                    message.from_user.id,
                ))
            sqlite_connection.commit()

            z = []
            z = sqlite_connection.execute(
                'SELECT login, password FROM account WHERE userID = ?',
                (message.from_user.id, )).fetchall()[0]
            login = z[0]
            password = z[1]

            x = []
            x = sqlite_connection.execute(
                'SELECT loginacc, passacc FROM users WHERE ID = ?',
                (message.from_user.id, )).fetchall()[0]
            login1 = x[0]
            password1 = x[1]
            hash_object = hashlib.md5(str(password1).encode())
            c = hash_object.hexdigest()

            if login == login1 and c == password:
                bot.send_message(message.from_user.id,
                                 '✅ Вы успешно вошли в аккаунт!',
                                 reply_markup=logout)
                sqlite_connection.execute('UPDATE account SET enter = ?',
                                          (1, ))
                sqlite_connection.commit()
                next_step(message.from_user.id, 17)
            else:
                sqlite_connection.execute('UPDATE account SET enter = ?',
                                          (0, ))
                sqlite_connection.commit()
                bot.send_message(
                    message.from_user.id,
                    'Логин или пароль введены неверно. Проверьте правильность ввода или зарегестрируйтесь.',
                    reply_markup=exit)
        except:
            sqlite_connection.execute('UPDATE account SET enter = ?', (0, ))
            sqlite_connection.commit()
            bot.send_message(
                message.from_user.id,
                'Логин или пароль введены неверно. Проверьте правильность ввода или зарегестрируйтесь.',
                reply_markup=exit)

    elif message.text == '📝Регистрация' and step == 17:
        try:
            z = []
            z = sqlite_connection.execute(
                'SELECT login, password FROM account WHERE userID = ?',
                (message.from_user.id, )).fetchone()
            if not z:
                bot.send_message(
                    message.from_user.id,
                    f'Введите логин и пароль (через enter) для создания вашего аккаунта.\n<b>(Пример:\nlogin\npassword)</b>',
                    reply_markup=exit,
                    parse_mode='html')
                next_step(message.from_user.id, 21)
            else:
                bot.send_message(
                    message.from_user.id,
                    '❌ У вас уже есть аккаунт! Удалите его, чтобы создать новый.',
                    reply_markup=reg)
                next_step(message.from_user.id, 17)
        except:
            bot.send_message(message.from_user.id, '🚫Ошибка')

    elif step == 21:
        try:
            f1 = False
            f2 = False
            f3 = False
            f4 = False
            f5 = False
            info = []
            for i in message.text.split('\n'):
                info.append(i)
            m = info[1]
            a = info[0]
            #Проверка на нахождения в строке m символов из списка symbols, заглавных букв и цифр
            sybmols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_']
            Capital_letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            digits = '1234567890'
            rualph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
            for i in a:
                if i in rualph:
                    f4 = True
            for i in m:
                if i in sybmols:
                    f1 = True
                if i in Capital_letter:
                    f2 = True
                if i in digits:
                    f3 = True
                if i in rualph:
                    f5 = True
                    break
            if len(m) < 17 and len(
                    m
            ) > 3 and f1 != True and f2 == True and f3 == True and f4 != True and f5 != True:
                f1 = False
                f2 = False
                f3 = False
                f4 = False
                f5 = False
                h = info[1]
                hash_object = hashlib.md5(str(h).encode())
                h = hash_object.hexdigest()
                sqlite_connection.execute(
                    'INSERT INTO account (login, password, userID) VALUES (?, ?, ?)',
                    (
                        info[0],
                        h,
                        message.from_user.id,
                    ))
                sqlite_connection.commit()
                bot.send_message(message.from_user.id,
                                 '✅ Аккаунт успешно создан!',
                                 reply_markup=reg)
                next_step(message.from_user.id, 17)
            else:
                bot.send_message(
                    message.from_user.id,
                    'Требование к логину:\n1. Логин должен содержать только английские буквы.\nТребования к паролю:\n1. Пароль должен быть от 4 до 16 символов.\n2. Пароль не должен содержать символы: !@#$%^&*()_\n3. Пароль должен содержать хотя бы одну цифру и заглавную букву.\n4. Пароль должен содержать только английские буквы.\nПопробуйте еще раз.',
                    parse_mode='html')
        except Exception as e:
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: Данный логин уже зарегистрирован. Попробуйте войти.',
                reply_markup=back3)

    elif message.text == '📝Изменить логин или пароль' and step == 17:
        try:
            z = []
            z = sqlite_connection.execute(
                'SELECT login, password FROM account WHERE userID = ?',
                (message.from_user.id, )).fetchall()[0]
            bot.send_message(message.from_user.id,
                             'Выберите действие: ',
                             reply_markup=editaccount)
            next_step(message.from_user.id, 22)
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫 Ошибка: Выберите действие из предложенных.',
                             reply_markup=editaccount)

    elif message.text == '📝Изменить логин' and step == 22:
        bot.send_message(message.from_user.id,
                         'Введите новый логин:',
                         reply_markup=exit)
        next_step(message.from_user.id, 23)

    elif step == 23:
        try:
            z = []
            z = sqlite_connection.execute(
                'SELECT login FROM account WHERE userID = ?',
                (message.from_user.id, )).fetchall()[0]
            f1 = False
            info = []
            for i in message.text.split('\n'):
                info.append(i)
            login = info[0]
            rualph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
            for i in login:
                if i in rualph:
                    f1 = True
                    break
            if login == z[0]:
                bot.send_message(
                    message.from_user.id,
                    'Введённый логин совпадает с текущим.\nИзмените его и попробуйте ещё раз.',
                    parse_mode='html')
            else:
                if f1 != True:
                    f1 = False
                    sqlite_connection.execute(
                        'UPDATE account SET login = ? WHERE userID = ?', (
                            info[0],
                            message.from_user.id,
                        ))
                    sqlite_connection.commit()

                    z = []
                    z = sqlite_connection.execute(
                        'SELECT login FROM account WHERE userID = ?',
                        (message.from_user.id, )).fetchall()[0]
                    bot.send_message(message.from_user.id,
                                     '✅Логин успешно изменён!\nНовый логин: ' +
                                     z[0],
                                     reply_markup=logout,
                                     parse_mode='html')
                    next_step(message.from_user.id, 17)
                else:
                    bot.send_message(
                        message.from_user.id,
                        'Требование к логину:\n1. Логин должен содержать только английские буквы.\nПопробуйте еще раз.',
                        parse_mode='html')
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫 Ошибка: Выберите действие из предложенных.',
                             reply_markup=editaccount)
            next_step(message.from_user.id, 22)

    elif message.text == '📝Изменить пароль' and step == 22:
        bot.send_message(message.from_user.id,
                         'Введите новый пароль:',
                         reply_markup=exit)
        next_step(message.from_user.id, 24)

    elif step == 24:
        try:
            f1 = False
            f2 = False
            f3 = False
            f4 = False
            info = []
            for i in message.text.split('\n'):
                info.append(i)
            password = info[0]
            sybmols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_']
            Capital_letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            digits = '1234567890'
            rualph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
            for i in password:
                if i in sybmols:
                    f1 = True
                if i in Capital_letter:
                    f2 = True
                if i in digits:
                    f3 = True
                if i in rualph:
                    f4 = True
                    break
            if len(password) < 17 and len(
                    password
            ) > 3 and f1 != True and f2 == True and f3 == True and f4 != True:
                f1 = False
                f2 = False
                f3 = False
                f4 = False
                hash_object = hashlib.md5(str(password).encode())
                c = hash_object.hexdigest()

                sqlite_connection.execute(
                    'UPDATE account SET password = ? WHERE userID = ?', (
                        c,
                        message.from_user.id,
                    ))
                sqlite_connection.commit()
                bot.send_message(message.from_user.id,
                                 '✅Пароль успешно изменен!',
                                 reply_markup=logout)
                next_step(message.from_user.id, 17)
            else:
                bot.send_message(
                    message.from_user.id,
                    'Требования к паролю:\n1. Пароль должен быть от 4 до 16 символов.\n2. Пароль не должен содержать символы: !@#$%^&*()_\n3. Пароль должен содержать хотя бы одну цифру и заглавную букву.\n4. Пароль должен содержать только английские буквы.\nПопробуйте еще раз.',
                    parse_mode='html')
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫 Ошибка: Выберите действие из предложенных.',
                             reply_markup=editaccount)
            next_step(message.from_user.id, 22)

    elif message.text == '♻️Удалить аккаунт' and step == 17:
        bot.send_message(message.from_user.id,
                         'Вы уверены?',
                         reply_markup=delaccount)
        next_step(message.from_user.id, 25)

    elif message.text == '✅Да' and step == 25:
        sqlite_connection.execute('DELETE FROM account WHERE userID = ?',
                                  (message.from_user.id, ))
        sqlite_connection.commit()
        bot.send_message(message.from_user.id,
                         '✅Аккаунт успешно удален!',
                         reply_markup=exit)

    elif message.text == '🚫Нет' and step == 25:
        bot.send_message(message.from_user.id,
                         'Вы отменили удаление аккаунта.',
                         reply_markup=logout)
        next_step(message.from_user.id, 17)

    elif message.text == '📊Статистика' and step == 17:
        x = []
        x = sqlite_connection.execute(
            'SELECT COUNT(id) FROM account').fetchall()[0]
        bot.send_message(
            message.from_user.id,
            '📊Количество зарегистрированных аккаунтов: ' + str(x[0]))
    else:
        bot.send_message(
            message.from_user.id,
            '🧐Хмм... Что-то я не припоминаю такой команды.\nПопробуйте - /start'
        )

    try:
        sqlite_connection.commit()
    except:
        pass


bot.polling(non_stop=True)