import telebot #Импорт библиотеки telebot
from telebot import types #Импорт типов для дальнейшего добавления кнопок
token='6816111823:AAHTczebujZURGHs9M43Wj-cia1sWXGrucw' #Фиксируем токен, полученный у BotFather
bot = telebot.TeleBot(token) #Обозначаем нашего бота

#Алгоритм для применения техники тест-дизайна попарного тестирования
def pairwise_algoritm():
    #Сортируем параметры по количеству возможных состояний. От большего к меньшему.
    pw.sort(key=len)
    pw.reverse()
    #Набираем состояния двух параметров, имеющих наибольшую вариативность и все их возможные пары в первый и второй "столбцы" вложенных списков.
    for i in range(1, len(pw[0])):
        for j in range(1, len(pw[1])):
            pwt.append([]) #Добавляем строку вложенным списком.
            pwt[-1].append(pw[0][i])
            pwt[-1].append(pw[1][j])
    #Если было добавлено всего два параметра - прекращаем выполнение функции.
    if len(pw) == 2:
        return
    #Запускаем цикл для всех параметров, кроме первых двух.
    for parameter in range(2, len(pw)):
        #Обнуляем переменные, разбивающие столбец со статусами на эквивалентные значения.
        start = 0
        end = 0
        #Запускаем цикл для каждого столбца со статусами, добавленными ранее.
        for column in range(parameter - 1, -1, -1):
            pwt.sort(key=lambda x: x[column]) #Сортируем строки по обрабатываемому столбцу.
            #Запускаем цикл для каждой строки pwt.
            for line in range(0, len(pwt)):
                #Если список эквивалентных значений закончился.
                if pwt[line][column] != pwt[start][column] or line == len(pwt) - 1:
                    #Если это была последняя строка столбца - обновим значение переменной end.
                    if line == len(pwt) - 1:
                        end = line + 1
                    #Запускаем цикл для каждого статуса добавляемого параметра.
                    for status in range(1, len(pw[parameter])):
                        #Проверим, была ли добавлена пара ранее.
                        pair_free = None #Обнулим переменную для первой пустой строки для добавляемого статуса.
                        #Запустим цикл в рамках списка эквивалентных значений.
                        for i in range(start, end):
                            #Если статус добавляемого параметра не добавлен и пустая строка не была зафиксирована ранее - фиксируем значение.
                            if pair_free == None and len(pwt[i]) == parameter:
                                pair_free = i
                            #Проверяем было ли ранее добавлено состояние добавляемого параметра, и совпадает ли оно с нынешним.
                            elif len(pwt[i]) > parameter and pwt[i][parameter] == pw[parameter][status]:
                                break #Если ранее уже была добавлена данная пара - переходим к следующему состоянию.
                            elif i == end - 1: #Если дошли до конца списка эквивалентных значений.
                                if pair_free != None: #Если пустое место было зафиксировано ранее.
                                    pwt[pair_free].append(pw[parameter][status]) #Добавляем обрабатываемое состояние в зафиксированное ранее пустое место.
                                elif len(pwt[i]) == parameter: #Если пустое место не было зафиксировано ранее, но в последней строке пусто.
                                    pwt[i].append(pw[parameter][status]) #Добавляем обрабатываемое состояние в последнюю строку.
                                else:
                                    print('beda')
                    start = line
                    #Изменяем порядок состояний обрабатываемого параметра для корректной работы алгоритма.
                    pw[parameter].append(pw[parameter][1])
                    pw[parameter].pop(1)
                #Если список эквивалентных значений продолжается. 
                elif pwt[line][column] == pwt[start][column]:
                    end = line + 1
                    continue
        #Заполним строки в последнем столбце, оставленные пустыми.
        for line in range(0, len(pwt)):
            if len(pwt[line]) == parameter:
                pwt[line].append(pw[parameter][1])

#Добавляем приветственное сообщение и запуск бота на любое сообщение пользователя.
@bot.message_handler()
def menu(message):
    #Объявляем переменные, в которые будем добавлять параметры и тесты.
    global pw
    global pwt
    pw = []
    pwt = []
    #Добавляем меню с вариантами ответа в главном меню и все необходимые кнопки.
    global markup
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Добавить параметр')
    btn2 = types.KeyboardButton('Удалить последний внесённый параметр')
    btn3 = types.KeyboardButton('Показать внесённые параметры')
    btn4 = types.KeyboardButton('Очистить все параметры')
    btn5 = types.KeyboardButton('Применить Pairwise')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.add(btn5)
    #Отправляем приветственное сообщение.
    bot.send_message(message.chat.id,'Привет, меня зовут Tedi Free.\nМеня создали для применения техник тест-дизайна и на данный момент я уже умею генерировать тесты для попарного тестирования. Для работы со мной воспользуйтесь кнопками ответа, а если заметите неполадки в моей работе - свяжитесь с моим создателем @koshelev101.', reply_markup=markup)
    bot.register_next_step_handler(message, pairwise)

#Обрабатываем возможные ответы пользователя.
def pairwise(message):
    global pw
    global pwt
    user_message = message.text
    if user_message == 'Добавить параметр':
        bot.send_message(message.chat.id,'Отправьте мне название нового параметра.')
        bot.register_next_step_handler(message, add_parameter)#Перейдём к функции добавления параметра.
    elif user_message == 'Удалить последний внесённый параметр' and len(pw) > 0:
        response_message = 'Параметр: ' + pw[-1][0] + ' и его состояния: '
        for i in range (1, len(pw[-1])):
            response_message += ' ' + pw[-1][i] + ','
        response_message = response_message[:-1] + ' удалены.'
        pw.pop()
        bot.send_message(message.chat.id,response_message, reply_markup=markup)
        bot.register_next_step_handler(message, pairwise)
    elif user_message == 'Удалить последний внесённый параметр' and len(pw) == 0 or user_message == 'Очистить все параметры' and len(pw) == 0:
        bot.send_message(message.chat.id,'У вас нет внесённых параметров.', reply_markup=markup)
        bot.register_next_step_handler(message, pairwise)
    elif user_message == 'Очистить все параметры':
        pw = []
        bot.send_message(message.chat.id,'Все внесённые ранее параметры были удалены.', reply_markup=markup)
        bot.register_next_step_handler(message, pairwise)
    elif user_message == 'Показать внесённые параметры':
        if len(pw) > 0:
            response_message = 'Вы внесли следующие параметры:'
            for i in pw:
                response_message += '\n' + i[0] + ': '
                for j in range(1, len(i)):
                    response_message += ' ' + i[j] + ','
                response_message = response_message[:-1] + '.'
            bot.send_message(message.chat.id,response_message, reply_markup=markup)
            bot.register_next_step_handler(message, pairwise)
        else:
            bot.send_message(message.chat.id,"У вас нет внесённых параметров.", reply_markup=markup)
            bot.register_next_step_handler(message, pairwise)
    elif user_message == 'Применить Pairwise':
        if len(pw) < 2:
            bot.send_message(message.chat.id,"Для попарного тестирования необходимо внести хотя бы 2 параметра.", reply_markup=markup)
            bot.register_next_step_handler(message, pairwise)
        else:
            pwt = [] #Сбрасываем добавленные ранее тесты в pwt.
            pairwise_algoritm() #Запускаем алгоритм pairwise.
            #Набираем сообщение со всеми набранными тестами и отправляем в ответ пользователю. 
            response_message = ''
            for line in range(0, len(pwt)):
                response_message += "Тест " + str(line + 1) + " - "
                for j in range(0, len(pwt[line])):
                    response_message += pw[j][0] + ": " + pwt[line][j] + ", "
                response_message = response_message[:-2] + ".\n"
            bot.send_message(message.chat.id,response_message, reply_markup=markup)
            bot.register_next_step_handler(message, pairwise)
    else:
        bot.send_message(message.chat.id,'Для работы с ботом, используйте кнопки ответа.', reply_markup=markup)
        bot.register_next_step_handler(message, pairwise)

#Функция добавления параметра.
def add_parameter(message):
    global pw
    #Добавляем меню добавления параметра и набираем необходимые кнопки ответа.
    global markup_add_parameter
    markup_add_parameter = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Завершить')
    btn2 = types.KeyboardButton('Удалить последнее внесённое состояние')
    btn3 = types.KeyboardButton('Отменить внесение параметра')
    markup_add_parameter.add(btn1)
    markup_add_parameter.add(btn2)
    markup_add_parameter.add(btn3)
    pw.append([]) #Добавляем вложенный список для нового параметра.
    user_message = message.text
    pw[-1].append(user_message) #Добавляем название параметра первым значением вложенного списка.
    bot.send_message(message.chat.id,'Отлично! Отправьте для параметра "' + pw[-1][0] + '" минимум 2 варианта его состояния и напишите "Завершить". Каждое состояние необходимо отправить отдельным сообщением.', reply_markup=markup_add_parameter)
    bot.register_next_step_handler(message, add_variant) #Переходим к добавлению состояний для нового параметра.

#Функция добавления состояний для нового параметра.
def add_variant(message):
    global pw
    user_message = message.text
    #Обрабатываем все возможные варианты ответа пользователя.
    if user_message == 'Завершить' and len(pw[-1]) < 3:
        bot.send_message(message.chat.id,'Параметр не был внесён. Для корректного внесения параметра, отправьте ещё минимум ' + str(3 - len(pw[-1])) + ' его состояния.', reply_markup=markup_add_parameter)
        bot.register_next_step_handler(message, add_variant)
    elif user_message == 'Завершить' and len(pw[-1]) >= 3:
        response_message = 'Параметр: ' + pw[-1][0] + ' и его состояния: '
        for i in range (1, len(pw[-1])):
            response_message += ' ' + pw[-1][i] + ','
        response_message = response_message[:-1] + ' - добавлены.'
        bot.send_message(message.chat.id,response_message, reply_markup=markup)
        bot.register_next_step_handler(message, pairwise)
    elif user_message == 'Удалить последнее внесённое состояние' and len(pw[-1]) > 1:
        last_state = pw[-1][-1]
        pw[-1].pop()
        bot.send_message(message.chat.id,'Состояние "' + last_state + '" удалено.', reply_markup=markup_add_parameter)
        bot.register_next_step_handler(message, add_variant)
    elif user_message == 'Удалить последнее внесённое состояние' and len(pw[-1]) <= 1:
        bot.send_message(message.chat.id,'У параметра "' + str(pw[-1]) + '" нет добавленных состояний.', reply_markup=markup_add_parameter)
        bot.register_next_step_handler(message, add_variant)
    elif user_message == 'Отменить внесение параметра':
        pw.pop()
        bot.send_message(message.chat.id,'Параметр не был внесён.', reply_markup=markup)
        bot.register_next_step_handler(message, pairwise)
    else:
        pw[-1].append(user_message)
        bot.send_message(message.chat.id,'Состояние "' + pw[-1][-1] + '" добавлено к параметру "' + pw[-1][0] + '".', reply_markup=markup_add_parameter)
        bot.register_next_step_handler(message, add_variant)

bot.infinity_polling()