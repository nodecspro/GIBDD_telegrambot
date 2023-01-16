import sqlite3  # Библиотека для работы с базой данных
from cgitb import html  # Библиотека для работы форматирования текста
import telebot  # Библиотека для работы с телеграмм ботом
from io import BytesIO  # Библиотека для работы с файлами
from docxtpl import DocxTemplate  # Библиотека для работы с шаблонами
from telebot import types  # Библиотека для работы с кнопками
from telebot.types import InlineKeyboardButton  # Библиотека для работы с кнопками
import hashlib  # Библиотека для работы с хэшами

doc = DocxTemplate("Выходной документ.docx")  # Путь к шаблону

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

bot = telebot.TeleBot(
    "5243511593:AAHGAPyiDax6hZCPoYO_b581PXsNs2eYoFM")  # Токен API к Telegram
sqlite_connection = sqlite3.connect(
    'dbpr.db', check_same_thread=False)  # Подключение к базе данных
cursor = sqlite_connection.cursor()  # Создание курсора


def next_step(id, step):  # Функция для перехода на следующий шаг
    try:
        user = []
        user = sqlite_connection.execute('SELECT id FROM users WHERE id = ?', (
            id, )).fetchone()  # Проверка на наличие пользователя в базе данных
        if not user:  # Если пользователя нет в базе данных, то добавляем его
            sqlite_connection.execute(
                'INSERT INTO users (step, id) values (?, ?)', (
                    step,
                    id,
                ))  # Добавление пользователя в базу данных
            sqlite_connection.commit()  # Сохранение изменений
        else:  # Если пользователь есть в базе данных, то обновляем его шаг
            sqlite_connection.execute('UPDATE users SET step = ? WHERE ID = ?',
                                      (
                                          step,
                                          id,
                                      ))  # Обновление шага пользователя
            sqlite_connection.commit()  # Сохранение изменений
    except sqlite3.Error as error:  # Обработка ошибок
        print("Ошибка при работе с SQLite:", error)  # Вывод ошибки


def numberauto(
        id, numberauto):  # Функция для обновления номера авто в таблице users
    sqlite_connection.execute('UPDATE users SET Numberauto = ? WHERE ID = ?', (
        numberauto,
        id,
    ))  # Обновление номера авто
    sqlite_connection.commit()  # Сохранение изменений


def EngineIDauto(id, EngineIDauto
                 ):  # Функция для обновления номера двигателя в таблице users
    sqlite_connection.execute('UPDATE users SET EngineIDauto = ? WHERE ID = ?',
                              (
                                  EngineIDauto,
                                  id,
                              ))  # Обновление номера двигателя
    sqlite_connection.commit()  # Сохранение изменений


def BodyIDauto(
        id,
        BodyIDauto):  # Функция для обновления номера кузова в таблице users
    sqlite_connection.execute('UPDATE users SET BodyIDAuto = ? WHERE ID = ?', (
        BodyIDauto,
        id,
    ))  # Обновление номера кузова
    sqlite_connection.commit()  # Сохранение изменений


def get_button(x):  # Функция для создания кнопок
    return types.ReplyKeyboardMarkup(row_width=x, resize_keyboard=True)


# Главное меню бота
mainmenu = get_button(2).add('🔍 Поиск ТС', '➕ Добавление ТС',
                             '➕ Добавление инспектора', '💼 Профиль')

# Меню авто
automenu = get_button(3).add('👨 Информация о владельце',
                             '📝 Редактировать информацию ТС',
                             '📝 Редактировать информацию о ТО',
                             '📄 Получить документ', '📝 Информация о ТО',
                             '♻️ Удаление авто', '🚪 Главное меню')
# Меню поиска авто
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


@bot.message_handler(commands=['start', 's', 'help',
                               'h'])  # Команды для запуска бота
def start(message):
    mess = f'Привет👋, <b>{message.from_user.first_name}</b>, ты запустил сервис ГИБДД.\nДля продолжения выберите нужную вам категорию👇'
    bot.send_message(message.chat.id,
                     mess,
                     reply_markup=mainmenu,
                     parse_mode='html')  # Отправка сообщения с кнопками
    next_step(message.from_user.id, 1)  # Запись в базу данных


@bot.message_handler(content_types=[
    'text', 'document', 'audio', 'photo', 'video', 'voice', 'location',
    'contact', 'sticker'
])  # Обработка сообщений
def start_quest(message):
    step = sqlite_connection.execute('SELECT step FROM users WHERE id = ?',
                                     (message.from_user.id, )).fetchall()[0][
                                         0]  # Получение шага из базы данных

    if message.text == '🚪 Главное меню':
        bot.send_message(
            message.from_user.id,
            'Вы вернулись в главное меню',
            reply_markup=mainmenu)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 1)  # Изменение шага в базе данных

    elif message.text == '↩️ Назад':
        bot.send_message(
            message.from_user.id,
            'Вы вернулись назад',
            reply_markup=searchauto)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 2)  # Изменение шага в базе данных

    elif message.text == '⬅️ Назад':
        bot.send_message(
            message.from_user.id, 'Вы вернулись назад',
            reply_markup=automenu)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 7)  # Изменение шага в базе данных

    elif message.text == '◀️ Назад':
        bot.send_message(
            message.from_user.id,
            'Вы вернулись назад',
            reply_markup=editownersmenu)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 7)  # Изменение шага в базе данных

    elif message.text == '🔙 Назад':
        bot.send_message(message.from_user.id,
                         'Вы вернулись назад',
                         reply_markup=reg)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 17)  # Изменение шага в базе данных

    elif message.text == '📝 Добавить информацию о прохождении ТО':
        bot.send_message(message.from_user.id, text=ToNew,
                         reply_markup=back1)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 12)  # Изменение шага в базе данных

    elif message.text == "🔍 Поиск ТС":
        bot.send_message(
            message.chat.id,
            'Выберите метод поиска ТС.',
            reply_markup=searchauto)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 2)  # Изменение шага в базе данных

    elif message.text == '🔍 Поиск по номеру ТС' and step == 2:
        bot.send_message(message.chat.id,
                         f'Введите номер ТС: \n<b>Пример: А111АА111</b>',
                         parse_mode='html',
                         reply_markup=back)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 3)  # Изменение шага в базе данных

    elif message.text == "💼 Профиль":
        try:
            x = sqlite_connection.execute(
                'SELECT enter FROM account WHERE userid = ?',
                (message.from_user.id,
                 )).fetchall()[0]  # Получение данных из базы данных
            if x == (1, ):  # Проверка на авторизацию
                bot.send_message(
                    message.chat.id,
                    'Вы уже авторизованы.',
                    reply_markup=logout)  # Отправка сообщения с кнопками
                next_step(message.from_user.id,
                          17)  # Изменение шага в базе данных
            else:  # Если не авторизован
                bot.send_message(
                    message.chat.id,
                    f'Нет аккаунта? - зарегистрируйте.\nЕсть аккаунт? - войдите.',
                    parse_mode='html',
                    reply_markup=reg)  # Отправка сообщения с кнопками
                next_step(message.from_user.id,
                          17)  # Изменение шага в базе данных
        except Exception as e:  # Обработка ошибок
            print(e)
            bot.send_message(
                message.chat.id,
                f'Нет аккаунта? - зарегистрируйте.\nЕсть аккаунт? - войдите.',
                parse_mode='html',
                reply_markup=reg)  # Отправка сообщения с кнопками
            next_step(message.from_user.id, 17)  # Изменение шага в базе данных

    elif message.text == "🚪 Выйти из аккаунта":
        sqlite_connection.execute(
            'UPDATE account SET enter = 0 WHERE userid = ?',
            (message.from_user.id, ))  # Изменение данных в базе данных
        sqlite_connection.commit()  # Сохранение изменений
        bot.send_message(message.chat.id,
                         '✅ Вы успешно вышли из аккаунта.',
                         reply_markup=reg)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 17)  # Изменение шага в базе данных

    elif step == 3:
        numberauto(message.from_user.id, message.text)  # Вызов функции
        try:  # Попытка получить данные из базы данных
            x = sqlite_connection.execute(
                'SELECT * FROM Auto WHERE Number = ?',
                (message.text,
                 )).fetchall()[0]  # Получение данных из базы данных
            bot.send_message(
                message.chat.id, eval(autoinfo),
                reply_markup=automenu)  # Отправка сообщения с кнопками
        except Exception as e:  # Обработка ошибок
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: ТС не найдено. Проверьте номер или добавьте новую машину.'
            )  # Отправка сообщения об ошибке
        next_step(message.from_user.id, 7)  # Изменение шага в базе данных

    elif message.text == '🔍 Поиск по номеру кузова' and step == 2:
        bot.send_message(message.chat.id,
                         'Введите номер кузова:',
                         reply_markup=back)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 4)  # Изменение шага в базе данных

    elif step == 4:
        try:  # Попытка получить данные из базы данных
            EngineIDauto(message.from_user.id, message.text)
            x = sqlite_connection.execute(
                'SELECT * FROM Auto WHERE BodyID = ?',
                (message.text,
                 )).fetchall()[0]  # Получение данных из базы данных
            bot.send_message(
                message.chat.id, eval(autoinfo),
                reply_markup=automenu)  # Отправка сообщения с кнопками
            next_step(message.from_user.id, 7)  # Изменение шага в базе данных

        except Exception as e:  # Обработка ошибок
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: ТС не найдено. Проверьте номер или добавьте новую машину.'
            )  # Отправка сообщения об ошибке

    elif message.text == '🔍 Поиск по номеру двигателя' and step == 2:
        bot.send_message(message.chat.id,
                         'Введите номер двигателя:',
                         reply_markup=back)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 5)  # Изменение шага в базе данных

    elif step == 5:
        try:  # Попытка получить данные из базы данных
            BodyIDauto(message.from_user.id, message.text)
            x = sqlite_connection.execute(
                'SELECT * FROM Auto WHERE EngineID = ?',
                (message.text,
                 )).fetchall()[0]  # Получение данных из базы данных
            bot.send_message(
                message.chat.id, eval(autoinfo),
                reply_markup=automenu)  # Отправка сообщения с кнопками
            next_step(message.from_user.id, 7)  # Изменение шага в базе данных
        except Exception as e:  # Обработка ошибок
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: ТС не найдено. Проверьте номер или добавьте новую машину.'
            )  # Отправка сообщения об ошибке

    elif message.text == '➕ Добавление ТС':
        bot.send_message(message.from_user.id,
                         text=new_auto,
                         reply_markup=exit)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 6)  # Изменение шага в базе данных

    elif step == 6:
        try:
            info = []
            for i in message.text.split(
                    '\n'):  # Разделение сообщения на строки
                info.append(i)  # Получение данных из сообщения
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
                ))  # Добавление данных в базу данных
            sqlite_connection.commit()  # Сохранение изменений
            bot.send_message(message.from_user.id,
                             '✅ТС успешно добавлено')  # Отправка сообщения
        except Exception as e:  # Обработка ошибок
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫Ошибка: Проверьте ввод данных. '
                             )  # Отправка сообщения об ошибке

    elif message.text == '👨 Информация о владельце' and step == 7:
        try:  # Попытка получить данные из базы данных
            ts = []
            ts = sqlite_connection.execute(
                'SELECT OwnerType FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id,
                 )).fetchall()[0]  # Получение данных из базы данных
            if ts[0] == '1':  # Проверка владельца на физическое лицо
                x = []
                x = sqlite_connection.execute(
                    'SELECT * FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                    (message.from_user.id,
                     )).fetchall()[0]  # Получение данных из базы данных
                bot.send_message(message.from_user.id,
                                 eval(OwnerInfo),
                                 reply_markup=editownersmenu
                                 )  # Отправка сообщения с кнопками
            else:  # Проверка владельца на юридическое лицо
                x = []
                x = sqlite_connection.execute(
                    'SELECT * FROM AutoOrg WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                    (message.from_user.id,
                     )).fetchall()[0]  # Получение данных из базы данных
                bot.send_message(message.from_user.id,
                                 eval(OrgInfo),
                                 reply_markup=editownersmenu
                                 )  # Отправка сообщения с кнопками
        except:  # У авто нет владельцев
            bot.send_message(
                message.from_user.id,
                'У авто нет владельцев. Добавьте его.',
                reply_markup=editownersmenu)  # Отправка сообщения с кнопками

    elif message.text == '👨 Добавление владельца' and step == 7:
        bot.send_message(message.from_user.id,
                         text=new_vladelec,
                         reply_markup=back2)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 16)  # Переход на следующий шаг

    elif step == 16:
        try:  # Попытка добавить данные в базу данных
            info = []
            for i in message.text.split(
                    '\n'):  # Разделение сообщения на строки
                info.append(i)  # Получение данных из сообщения
            sqlite_connection.execute(
                'INSERT INTO AutoVladelca (OwnerFIO, OwnerPhone, OwnerAddress, AutoNumber, AutoBodyID, AutoEngineID) VALUES (?, ?, ?, ?, ?, ?)',
                (
                    info[0],
                    info[1],
                    info[2],
                    info[3],
                    info[4],
                    info[5],
                ))  # Добавление данных в базу данных
            sqlite_connection.commit()  # Сохранение изменений
            bot.send_message(
                message.from_user.id,
                '✅ Владелец успешно добавлен')  # Отправка сообщения
        except Exception as e:  # Ошибка при добавлении данных в базу данных
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫Ошибка: Проверьте ввод данных. '
                             )  # Отправка сообщения об ошибкой

    elif message.text == '🔀 Изменить владельца' and step == 7:
        try:  # Попытка получить данные из базы данных
            ts = []
            ts = sqlite_connection.execute(
                'SELECT OwnerType FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id,
                 )).fetchall()[0]  # Получение типа владельца

            if ts[0] == '1':  # Проверка типа владельца на физическое лицо
                x = []
                x = sqlite_connection.execute(
                    'SELECT * FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                    (message.from_user.id,
                     )).fetchall()[0]  # Получение данных из базы данных
                bot.send_message(
                    message.from_user.id,
                    eval(OwnerInfo) +
                    '\nВведите номер пункта, который вы хотите редактировать',
                    reply_markup=back2)  # Отправка сообщения с кнопками
            else:  # Проверка типа владельца на юридическое лицо
                x = []
                x = sqlite_connection.execute(
                    'SELECT * FROM AutoOrg WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                    (message.from_user.id,
                     )).fetchall()[0]  # Получение данных из базы данных
                bot.send_message(
                    message.from_user.id,
                    eval(OrgInfo) +
                    '\nВведите номер пункта, который вы хотите отредактировать:',
                    reply_markup=back2)  # Отправка сообщения с кнопками
            next_step(message.from_user.id, 9)  # Переход к следующему шагу
        except Exception as e:  # Ошибка при получении данных из базы данных
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫Ошибка: У авто нет владельцев.'
                             )  # Отправка сообщения об ошибке

    elif step == 9:
        if message.text == '1':  # Проверка на номер пункта
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 41)  # Переход к следующему шагу
        elif message.text == '2':  # Проверка на номер пункта
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 42)  # Переход к следующему шагу
        elif message.text == '3':  # Проверка на номер пункта
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 43)  # Переход к следующему шагу

    elif step == 41:  # Изменение ФИО владельца
        sqlite_connection.execute(
            'UPDATE AutoVladelca SET OwnerFIO = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text,
             message.from_user.id))  # Изменение данных в базе данных
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id,
             )).fetchall()[0]  # Получение данных из базы данных
        bot.send_message(
            message.from_user.id,
            eval(OwnerInfo) +
            '✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 9)  # Переход к следующему шагу

    elif step == 42:  # Изменение телефона владельца
        sqlite_connection.execute(
            'UPDATE AutoVladelca SET OwnerPhone = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text,
             message.from_user.id))  # Изменение данных в базе данных
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id,
             )).fetchall()[0]  # Получение данных из базы данных

        bot.send_message(
            message.from_user.id,
            eval(OwnerInfo) +
            '✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 9)  # Переход к следующему шагу

    elif step == 43:  # Изменение адреса владельца
        sqlite_connection.execute(
            'UPDATE AutoVladelca SET OwnerAddress = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text,
             message.from_user.id))  # Изменение данных в базе данных
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id,
             )).fetchall()[0]  # Получение данных из базы данных

        bot.send_message(
            message.from_user.id,
            eval(OwnerInfo) +
            '✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 9)  # Переход к следующему шагу

    elif message.text == '📝 Редактировать информацию ТС' and step == 7:
        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id,
             )).fetchall()[0]  # Получение данных из базы данных
        bot.send_message(
            message.from_user.id,
            eval(autoinfo) +
            '\nВведите номер пункта, который вы хотите отредактировать:',
            reply_markup=back1,
        )  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 8:
        if message.text == '1':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 51)  # Переход к следующему шагу
        elif message.text == '2':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 52)  # Переход к следующему шагу
        elif message.text == '3':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 53)  # Переход к следующему шагу
        elif message.text == '4':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 54)  # Переход к следующему шагу
        elif message.text == '5':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 55)  # Переход к следующему шагу
        elif message.text == '6':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 56)  # Переход к следующему шагу
        elif message.text == '7':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 57)  # Переход к следующему шагу
        elif message.text == '8':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 58)  # Переход к следующему шагу
        elif message.text == '9':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 59)  # Переход к следующему шагу
        elif message.text == '10':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 510)  # Переход к следующему шагу
        elif message.text == '11':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 511)  # Переход к следующему шагу
        elif message.text == '12':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 512)  # Переход к следующему шагу
        elif message.text == '13':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 513)  # Переход к следующему шагу
        elif message.text == '14':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 514)  # Переход к следующему шагу
        elif message.text == '15':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 515)  # Переход к следующему шагу
        else:
            bot.send_message(message.from_user.id,
                             "🚫 Ошибка: такого пункта нет, введите заново"
                             )  # Отправка сообщения

    elif step == 51:
        sqlite_connection.execute(
            'UPDATE Auto SET Number = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД
        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 52:
        sqlite_connection.execute(
            'UPDATE Auto SET BodyId = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 53:
        sqlite_connection.execute(
            'UPDATE Auto SET EngineId = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 54:
        sqlite_connection.execute(
            'UPDATE Auto SET Brand = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 55:
        sqlite_connection.execute(
            'UPDATE Auto SET Model = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 56:
        sqlite_connection.execute(
            'UPDATE Auto SET Color = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 57:
        sqlite_connection.execute(
            'UPDATE Auto SET Volume = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 58:
        sqlite_connection.execute(
            'UPDATE Auto SET Comment = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 59:
        sqlite_connection.execute(
            'UPDATE Auto SET Helm = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 510:
        sqlite_connection.execute(
            'UPDATE Auto SET Drive = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 511:
        sqlite_connection.execute(
            'UPDATE Auto SET Year = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 512:
        sqlite_connection.execute(
            'UPDATE Auto SET TypeBody = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 513:
        sqlite_connection.execute(
            'UPDATE Auto SET DrivingAway = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 514:
        sqlite_connection.execute(
            'UPDATE Auto SET DateAway = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif step == 515:
        sqlite_connection.execute(
            'UPDATE Auto SET OwnerType = ? WHERE Number IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(autoinfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 8)  # Переход к следующему шагу

    elif message.text == '➕ Добавление инспектора' and step == 1:
        bot.send_message(message.from_user.id,
                         text=new_insp,
                         reply_markup=exit)  # Отправка сообщения
        next_step(message.from_user.id, 10)  # Переход к следующему шагу

    elif step == 10:
        try:  # Попытка добавить инспектора
            info = []
            for i in message.text.split('\n'):  # Разделение данных
                info.append(i)  # Добавление данных в список
            sqlite_connection.execute(
                'INSERT INTO Inspector (InspFIO, InspDR, TOid) VALUES (?, ?, ?)',
                (
                    info[0],
                    info[1],
                    info[2],
                ))  # Добавление данных в БД
            sqlite_connection.commit()  # Сохранение изменений
            bot.send_message(
                message.from_user.id,
                '✅ Инспектор успешно добавлен')  # Отправка сообщения
        except Exception as e:  # Если произошла ошибка
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫Ошибка: Проверьте ввод данных. ')  # Отправка сообщения

    elif message.text == '📝 Информация о ТО' and step == 7:
        try:
            x = []
            x = sqlite_connection.execute(
                'SELECT * FROM Toauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id,
                 )).fetchall()[0]  # Получение данных из БД
            bot.send_message(
                message.from_user.id, eval(ToInfo),
                reply_markup=back1)  # Отправка сообщения с кнопками
            next_step(message.from_user.id, 7)  # Переход к следующему шагу
        except Exception as e:  # Если произошла ошибка
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: Запись о ТО не найдена. Проверьте номер или добавьте новое ТО.',
                reply_markup=addTO)  # Отправка сообщения с кнопками

    elif message.text == '👨 Новый владелец' and step == 7:
        bot.send_message(message.from_user.id,
                         text=new_vladelec,
                         reply_markup=exit)  # Отправка сообщения с кнопками
        next_step(message.from_user.id, 10)  # Переход к следующему шагу

    elif step == 10:
        try:  # Попытка добавить владельца
            info = []
            for i in message.text.split('\n'):  # Разделение данных
                info.append(i)  # Добавление данных в список
            sqlite_connection.execute(
                'INSERT INTO AutoVladelca (OwnerFIO, OwnerPhone, OwnerAddress, AutoNumber, BodyID, EngineID) VALUES (?, ?, ?, ?, ?, ?)',
                (
                    info[0],
                    info[1],
                    info[2],
                    info[3],
                    info[4],
                    info[5],
                ))  # Добавление данных в БД
            sqlite_connection.commit()  # Сохранение изменений
            bot.send_message(
                message.from_user.id,
                '✅Владелец успешно добавлен')  # Отправка сообщения
        except Exception as e:  # Если произошла ошибка
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫Ошибка: Проверьте ввод данных. ')  # Отправка сообщения

    elif step == 12:
        try:  # Попытка добавить ТО
            info = []
            for i in message.text.split('\n'):  # Разделение данных
                info.append(i)  # Добавление данных в список
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
                ))  # Добавление данных в БД
            sqlite_connection.commit()  # Сохранение изменений
            bot.send_message(
                message.from_user.id,
                '✅ Данные о ТО успешно добавлены')  # Отправка сообщения
        except Exception as e:  # Если произошла ошибка
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫Ошибка: Проверьте ввод данных. ')  # Отправка сообщения

    elif message.text == '📝 Редактировать информацию о ТО' and step == 7:
        try:  # Попытка получить данные о ТО
            x = []
            x = sqlite_connection.execute(
                'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id,
                 )).fetchall()[0]  # Получение данных из БД
            bot.send_message(
                message.from_user.id,
                eval(ToInfoedit) +
                '\nВведите номер пункта, который вы хотите редактировать',
                reply_markup=back1)  # Отправка сообщения
            next_step(message.from_user.id, 14)  # Смена шага
        except:  # Если произошла ошибка
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: Запись о ТО не найдена. Проверьте номер или добавьте новое ТО.',
                reply_markup=addTO)  # Отправка сообщения

    elif step == 14:
        if message.text == '2':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 62)  # Смена шага
        elif message.text == '3':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 63)  # Смена шага
        elif message.text == '4':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 64)  # Смена шага
        elif message.text == '5':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 65)  # Смена шага
        elif message.text == '6':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 66)  # Смена шага
        elif message.text == '7':
            bot.send_message(message.from_user.id,
                             'Введите ответ на пункт:')  # Отправка сообщения
            next_step(message.from_user.id, 67)  # Смена шага
        else:  # Если произошла ошибка
            bot.send_message(
                message.from_user.id,
                '🚫Ошибка: Этот пункт нельзя изменить.')  # Отправка сообщения

    elif step == 62:
        sqlite_connection.execute(
            'UPDATE TOauto SET DateSee = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 14)  # Смена шага

    elif step == 63:
        sqlite_connection.execute(
            'UPDATE TOauto SET InspID = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 14)  # Смена шага

    elif step == 64:
        sqlite_connection.execute(
            'UPDATE TOauto SET YearTax = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 14)  # Смена шага
    elif step == 65:
        sqlite_connection.execute(
            'UPDATE TOauto SET TOtax = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 14)  # Смена шага
    elif step == 66:
        sqlite_connection.execute(
            'UPDATE TOauto SET Okey = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 14)  # Смена шага
    elif step == 67:
        sqlite_connection.execute(
            'UPDATE TOauto SET Reason = ? WHERE AutoNumber IN (SELECT numberauto FROM users WHERE Id = ?)',
            (message.text, message.from_user.id))  # Изменение данных в БД
        sqlite_connection.commit()  # Сохранение изменений

        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

        bot.send_message(
            message.from_user.id,
            eval(ToInfoedit) +
            '\n\n✅ Пункт изменён\nХотите изменить ещё один пункт? - Введите его номер'
        )  # Отправка сообщения
        next_step(message.from_user.id, 14)  # Смена шага

    elif message.text == "📄 Получить документ" and step == 7:
        x = []
        x = sqlite_connection.execute(
            'SELECT * FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?)',
            (message.from_user.id, )).fetchall()[0]  # Получение данных из БД

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

        doc.render(context)  # Заполнение шаблона
        buffer = BytesIO()  # Создание буфера
        doc.save(buffer)  # Сохранение в буфер
        buffer.seek(0)  # Перемещение указателя в начало буфера
        bot.send_document(
            message.from_user.id,
            buffer,
            caption='✅ Документ успешно сгенерирован!',
            visible_file_name=f'{x[0]}.docx')  # Отправка документа

    elif message.text == '♻️ Удаление авто' and step == 7:
        bot.send_message(
            message.from_user.id,
            'Вы действительно хотите удалить запись об авто?\n Введите "+", если вы хотите это сделать',
            reply_markup=back1)  # Отправка сообщения
        next_step(message.from_user.id, 15)  # Смена шага

    elif step == 15:
        if message.text == '+':  # Проверка на ввод "+"
            sqlite_connection.execute(
                'DELETE FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM AutoOrg WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM AutoVladelca WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM TOauto WHERE AutoNumber IN(SELECT numberauto FROM users WHERE Id = ?)',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM Auto WHERE BodyID IN(SELECT BodyID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM AutoOrg WHERE AutoBodyID IN(SELECT BodyID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM AutoVladelca WHERE AutoBodyID IN(SELECT BodyID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM TOauto WHERE AutoBodyID IN(SELECT BodyID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM Auto WHERE EngineID IN(SELECT EngineID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM AutoOrg WHERE AutoEngineID IN(SELECT EngineID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM AutoVladelca WHERE AutoEngineID IN(SELECT EngineID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM TOauto WHERE AutoEngineID IN(SELECT EngineID FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))  # Удаление данных из БД

            sqlite_connection.execute(
                'DELETE FROM Inspector WHERE TOid IN(SELECT TOid FROM Auto WHERE Number IN(SELECT numberauto FROM users WHERE Id = ?))',
                (message.from_user.id, ))  # Удаление данных из БД

            bot.send_message(message.from_user.id,
                             '✅ Авто успешно удалено',
                             reply_markup=exit)  # Отправка сообщения
        else:  # Если введено не "+"
            bot.send_message(
                message.from_user.id,
                'Для удаления необходимо написать "+", если хотиnе выйти, нажмите кнопку ниже'
            )  # Отправка сообщения

    elif message.text == '🔑Войти' and step == 17:
        bot.send_message(
            message.from_user.id,
            f'Введите логин и пароль (через enter) для входа в ваш аккаунт.\n<b>(Пример:\nlogin\npassword)</b>',
            reply_markup=exit,
            parse_mode='html')  # Отправка сообщения
        next_step(message.from_user.id, 18)  # Смена шага

    elif step == 18:
        try:
            info = []
            for i in message.text.split(
                    '\n'):  # Разделение сообщения на логин и пароль
                info.append(i)  # Добавление в список

            z = []
            z = sqlite_connection.execute(
                'SELECT login, password FROM account WHERE userID = ?',
                (message.from_user.id,
                 )).fetchall()[0]  # Получение данных из БД
            login = z[0]
            password = z[1]

            login1 = info[0]
            password1 = info[1]
            hash_object = hashlib.md5(
                str(password1).encode())  # Хеширование пароля
            c = hash_object.hexdigest()  # Хеширование пароля

            if login == login1 and c == password:  # Проверка логина и пароля
                bot.send_message(message.from_user.id,
                                 '✅ Вы успешно вошли в аккаунт!',
                                 reply_markup=logout)  # Отправка сообщения
                sqlite_connection.execute('UPDATE account SET enter = ?',
                                          (1, ))  # Обновление данных в БД
                sqlite_connection.commit()  # Сохранение данных в БД
                next_step(message.from_user.id, 17)  # Смена шага
            else:  # Если логин или пароль введены неверно
                sqlite_connection.execute('UPDATE account SET enter = ?',
                                          (0, ))  # Обновление данных в БД
                sqlite_connection.commit()  # Сохранение данных в БД
                bot.send_message(
                    message.from_user.id,
                    'Логин или пароль введены неверно. Проверьте правильность ввода или зарегестрируйтесь.',
                    reply_markup=exit)  # Отправка сообщения
        except:
            sqlite_connection.execute('UPDATE account SET enter = ?',
                                      (0, ))  # Обновление данных в БД
            sqlite_connection.commit()  # Сохранение данных в БД
            bot.send_message(
                message.from_user.id,
                'Логин или пароль введены неверно. Проверьте правильность ввода или зарегестрируйтесь.',
                reply_markup=exit)  # Отправка сообщения

    elif message.text == '📝Регистрация' and step == 17:
        try:  # Проверка на наличие аккаунта
            z = []
            z = sqlite_connection.execute(
                'SELECT login, password FROM account WHERE userID = ?',
                (message.from_user.id, )).fetchone()  # Получение данных из БД
            if not z:  # Если аккаунта нет
                bot.send_message(
                    message.from_user.id,
                    f'Введите логин и пароль (через enter) для создания вашего аккаунта.\n<b>(Пример:\nlogin\npassword)</b>',
                    reply_markup=exit,
                    parse_mode='html')  # Отправка сообщения
                next_step(message.from_user.id, 21)  # Смена шага
            else:  # Если аккаунт есть
                bot.send_message(
                    message.from_user.id,
                    '❌ У вас уже есть аккаунт! Удалите его, чтобы создать новый.',
                    reply_markup=reg)  # Отправка сообщения
                next_step(message.from_user.id, 17)  # Смена шага
        except:
            bot.send_message(message.from_user.id,
                             '🚫Ошибка')  # Отправка сообщения

    elif step == 21:
        try:
            f1 = False  # Переменная для проверки наличия заглавных букв
            f2 = False  # Переменная для проверки наличия цифр
            f3 = False  # Переменная для проверки наличия символов
            f4 = False  # Переменная для проверки наличия русских букв в логине
            f5 = False  # Переменная для проверки наличия русских букв в пароле
            info = []
            for i in message.text.split(
                    '\n'):  # Разделение строки на логин и пароль
                info.append(i)  # Добавление в список
            m = info[1]  # Переменная для проверки длины пароля
            a = info[0]  # Переменная для проверки длины логина
            # Проверка на нахождения в строке m символов из списка symbols, заглавных букв и цифр
            sybmols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                       '_']  # Список символов
            Capital_letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Список заглавных букв
            digits = '1234567890'  # Список цифр
            rualph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'  # Список русских букв
            for i in a:  # Проверка на наличие русских букв в логине
                if i in rualph:  # Если есть
                    f4 = True  # Переменная f4 становится True
            for i in m:  # Проверка на наличие символов, заглавных букв, цифр и русских букв в пароле
                if i in sybmols:  # Если есть
                    f1 = True  # Переменная f1 становится True
                if i in Capital_letter:  # Если есть
                    f2 = True  # Переменная f2 становится True
                if i in digits:  # Если есть
                    f3 = True  # Переменная f3 становится True
                if i in rualph:  # Если есть
                    f5 = True  # Переменная f5 становится True
                    break  # Прерывание цикла
            if len(m) < 17 and len(
                    m
            ) > 3 and f1 != True and f2 == True and f3 == True and f4 != True and f5 != True:  # Проверка на длину пароля и наличие символов, заглавных букв и цифр в пароле
                f1 = False
                f2 = False
                f3 = False
                f4 = False
                f5 = False
                h = info[1]
                hash_object = hashlib.md5(
                    str(h).encode())  # Хеширование пароля
                h = hash_object.hexdigest()  # Хеширование пароля
                sqlite_connection.execute(
                    'INSERT INTO account (login, password, userID) VALUES (?, ?, ?)',
                    (
                        info[0],
                        h,
                        message.from_user.id,
                    ))  # Добавление в базу данных
                sqlite_connection.commit()  # Сохранение изменений
                bot.send_message(message.from_user.id,
                                 '✅ Аккаунт успешно создан!',
                                 reply_markup=reg)  # Отправка сообщения
                next_step(message.from_user.id,
                          17)  # Переход к следующему шагу
            else:  # Если данные не соответствуют требованиям
                bot.send_message(
                    message.from_user.id,
                    'Требование к логину:\n1. Логин должен содержать только английские буквы.\nТребования к паролю:\n1. Пароль должен быть от 4 до 16 символов.\n2. Пароль не должен содержать символы: !@#$%^&*()_\n3. Пароль должен содержать хотя бы одну цифру и заглавную букву.\n4. Пароль должен содержать только английские буквы.\nПопробуйте еще раз.',
                    parse_mode='html')  # Отправка сообщения
        except Exception as e:  # Если произошла ошибка
            print(e)
            bot.send_message(
                message.from_user.id,
                '🚫 Ошибка: Данный логин уже зарегистрирован. Попробуйте войти.',
                reply_markup=back3)  # Отправка сообщения

    elif message.text == '📝Изменить логин или пароль' and step == 17:
        try:
            z = []
            z = sqlite_connection.execute(
                'SELECT login, password FROM account WHERE userID = ?',
                (message.from_user.id,
                 )).fetchall()[0]  # Получение логина и пароля из базы данных
            bot.send_message(message.from_user.id,
                             'Выберите действие: ',
                             reply_markup=editaccount)  # Отправка сообщения
            next_step(message.from_user.id, 22)  # Переход к следующему шагу
        except Exception as e:  # Если произошла ошибка
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫 Ошибка: Выберите действие из предложенных.',
                             reply_markup=editaccount)  # Отправка сообщения

    elif message.text == '📝Изменить логин' and step == 22:
        bot.send_message(message.from_user.id,
                         'Введите новый логин:',
                         reply_markup=exit)  # Отправка сообщения
        next_step(message.from_user.id, 23)  # Переход к следующему шагу

    elif step == 23:
        try:
            z = []
            z = sqlite_connection.execute(
                'SELECT login FROM account WHERE userID = ?',
                (message.from_user.id,
                 )).fetchall()[0]  # Получение логина из базы данных
            f1 = False
            info = []
            for i in message.text.split(
                    '\n'):  # Разделение сообщения на строки
                info.append(i)  # Добавление строки в список
            login = info[0]  # Получение логина из списка
            rualph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'  # Список русских букв
            for i in login:  # Проверка на русские буквы
                if i in rualph:  # Если есть русские буквы
                    f1 = True  # f1 становится True
                    break
            if login == z[0]:  # Если логин совпадает с текущим
                bot.send_message(
                    message.from_user.id,
                    'Введённый логин совпадает с текущим.\nИзмените его и попробуйте ещё раз.',
                    parse_mode='html')  # Отправка сообщения
            else:  # Если логин не совпадает с текущим
                if f1 != True:  # Если нет русских букв
                    f1 = False  # f1 становится False
                    sqlite_connection.execute(
                        'UPDATE account SET login = ? WHERE userID = ?', (
                            info[0],
                            message.from_user.id,
                        ))  # Обновление логина в базе данных
                    sqlite_connection.commit()  # Сохранение изменений

                    z = []
                    z = sqlite_connection.execute(
                        'SELECT login FROM account WHERE userID = ?',
                        (message.from_user.id,
                         )).fetchall()[0]  # Получение логина из базы данных
                    bot.send_message(message.from_user.id,
                                     '✅Логин успешно изменён!\nНовый логин: ' +
                                     z[0],
                                     reply_markup=logout,
                                     parse_mode='html')  # Отправка сообщения
                    next_step(message.from_user.id,
                              17)  # Переход к следующему шагу
                else:  # Если есть русские буквы
                    bot.send_message(
                        message.from_user.id,
                        'Требование к логину:\n1. Логин должен содержать только английские буквы.\nПопробуйте еще раз.',
                        parse_mode='html')  # Отправка сообщения
        except Exception as e:  # Если произошла ошибка
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫 Ошибка: Выберите действие из предложенных.',
                             reply_markup=editaccount)  # Отправка сообщения
            next_step(message.from_user.id, 22)  # Переход к следующему шагу

    elif message.text == '📝Изменить пароль' and step == 22:
        bot.send_message(message.from_user.id,
                         'Введите новый пароль:',
                         reply_markup=exit)  # Отправка сообщения
        next_step(message.from_user.id, 24)  # Переход к следующему шагу

    elif step == 24:
        try:
            f1 = False
            f2 = False
            f3 = False
            f4 = False
            info = []
            for i in message.text.split(
                    '\n'):  # Разделение сообщения на строки
                info.append(i)  # Добавление строки в список
            password = info[0]
            sybmols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                       '_']  # Список символов
            Capital_letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Список заглавных букв
            digits = '1234567890'  # Список цифр
            rualph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'  # Список русских букв
            for i in password:  # Проверка пароля на соответствие требованиям
                if i in sybmols:  # Если есть символы
                    f1 = True  # Переменная f1 = True
                if i in Capital_letter:  # Если есть заглавные буквы
                    f2 = True  # Переменная f2 = True
                if i in digits:  # Если есть цифры
                    f3 = True  # Переменная f3 = True
                if i in rualph:  # Если есть русские буквы
                    f4 = True  # Переменная f4 = True
                    break
            if len(password) < 17 and len(
                    password
            ) > 3 and f1 != True and f2 == True and f3 == True and f4 != True:  # Если пароль соответствует требованиям
                f1 = False
                f2 = False
                f3 = False
                f4 = False
                hash_object = hashlib.md5(
                    str(password).encode())  # Хеширование пароля
                c = hash_object.hexdigest()  # Получение хеша

                sqlite_connection.execute(
                    'UPDATE account SET password = ? WHERE userID = ?', (
                        c,
                        message.from_user.id,
                    ))  # Изменение пароля в базе данных
                sqlite_connection.commit()  # Сохранение изменений
                bot.send_message(message.from_user.id,
                                 '✅Пароль успешно изменен!',
                                 reply_markup=logout)  # Отправка сообщения
                next_step(message.from_user.id,
                          17)  # Переход к следующему шагу
            else:  # Если пароль не соответствует требованиям
                bot.send_message(
                    message.from_user.id,
                    'Требования к паролю:\n1. Пароль должен быть от 4 до 16 символов.\n2. Пароль не должен содержать символы: !@#$%^&*()_\n3. Пароль должен содержать хотя бы одну цифру и заглавную букву.\n4. Пароль должен содержать только английские буквы.\nПопробуйте еще раз.',
                    parse_mode='html')  # Отправка сообщения
        except Exception as e:  # Если произошла ошибка
            print(e)
            bot.send_message(message.from_user.id,
                             '🚫 Ошибка: Выберите действие из предложенных.',
                             reply_markup=editaccount)  # Отправка сообщения
            next_step(message.from_user.id, 22)  # Переход к следующему шагу

    elif message.text == '♻️Удалить аккаунт' and step == 17:  # Если пользователь выбрал удалить аккаунт
        bot.send_message(message.from_user.id,
                         'Вы уверены?',
                         reply_markup=delaccount)  # Отправка сообщения
        next_step(message.from_user.id, 25)  # Переход к следующему шагу

    elif message.text == '✅Да' and step == 25:  # Если пользователь выбрал да
        sqlite_connection.execute(
            'DELETE FROM account WHERE userID = ?',
            (message.from_user.id, ))  # Удаление аккаунта из базы данных
        sqlite_connection.commit()  # Сохранение изменений
        bot.send_message(message.from_user.id,
                         '✅Аккаунт успешно удален!',
                         reply_markup=exit)  # Отправка сообщения

    elif message.text == '🚫Нет' and step == 25:  # Если пользователь выбрал нет
        bot.send_message(message.from_user.id,
                         'Вы отменили удаление аккаунта.',
                         reply_markup=logout)  # Отправка сообщения
        next_step(message.from_user.id, 17)  # Переход к следующему шагу

    elif message.text == '📊Статистика' and step == 17:
        x = []
        x = sqlite_connection.execute(
            'SELECT COUNT(id) FROM account').fetchall()[
                0]  # Получение количества аккаунтов
        bot.send_message(message.from_user.id,
                         'Количество зарегистрированных аккаунтов: ' +
                         str(x[0]))  # Отправка сообщения
    else:  # Если пользователь ввел неизвестную команду
        bot.send_message(
            message.from_user.id,
            '🧐Хмм... Что-то я не припоминаю такой команды.\nПопробуйте - /start'
        )  # Отправка сообщения

    try:  # Попытка сохранить изменения
        sqlite_connection.commit()  # Сохранение изменений
    except:  # Если произошла ошибка
        pass  # Если произошла ошибка, то ничего не делать


bot.polling(non_stop=True)  # Запуск бота
