import time

import logging

import telebot

import config as cfg

import dbmanager as db

bot = telebot.TeleBot(cfg.token)

picsdir = cfg.picsdir


def goodbye(message):
    bot.send_message(message.chat.id, 'Эх, как жаль… Придется подарить стикеры кому-нибудь другому. До встречи! '
                                      'Если передумаешь, просто напиши "Да"',
                     reply_markup=cfg.default_markup)
    #db.set_state(message.chat.id, cfg.States.ITS_ALL_OVER.value)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Я - бот, и я помогаю своей подруге в исследовании, поэтому я буду очень рад, если '
                                      'ты заполнишь анкеты из нашего диалога.\nО технических неполадках можно сообщить ему: '
                                      '@vysokov_maksim\nА можно просто нажать /start и начать с начала (заполнять одну '
                                      'и ту же анкету несколько раз не нужно: можно использовать старые кодовые слова).')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, r'Привет! Я Веселый Зуб. Больше всего на свете люблю, когда обо мне заботятся. 😊 '
                                      r'Сегодня у меня отличное настроение, и поэтому хочу сделать тебе подарок – крутые стикеры! '
                                      r'Хочешь их получить?', reply_markup=cfg.binary_markup)
    db.set_state(message.chat.id, cfg.States.AGE_REQUEST.value)


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.ITS_ALL_OVER.value)
def restart(message):
    bot.send_message(message.chat.id, 'Если ты передумал, нажми на /start и мы все начнем сначала.')


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.AGE_REQUEST.value)
def age_request(message):
    if message.text in cfg.yes:
        bot.send_message(message.chat.id, 'А сколько тебе лет? У меня нет ограничений по возрасту - просто так спрашиваю.',
                         reply_markup=cfg.default_markup)
        db.set_state(message.chat.id, cfg.States.OFFERING.value)
    elif message.text in cfg.no:
        goodbye(message)
    else:
        # ioerr_pic = open(picsdir + 'cannot_understand.jpg', 'rb')
        # bot.send_photo(message.chat.id, ioerr_pic, caption='Скажи "Да" или "Нет"')
        bot.send_photo(message.chat.id, 'AgADAgADMakxG0zj8Usu-WtxZFlrmXEFMw4ABAn9j-uT1tUBtNMDAAEC',
                       caption='Скажи "Да" или "Нет"') # cannot_understand.jpg


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.OFFERING.value)
def offer(message):
    try:
        age = int(message.text)
        if age in range(1, 100):
            db.set_age(message.chat.id, str(age))
            bot.send_message(message.chat.id, 'Отлично! Ты получишь целый набор стикеров со мной после того, как '
                                              'уделишь мне немного внимания. Хочу поделиться с тобой секретами здоровой и '
                                              'красивой улыбки. Но сначала я должен узнать, что ты знаешь об уходе за '
                                              'зубами сейчас. Заполняй анкету по ссылке, возвращайся ко мне и напиши кодовое слово!\n'
                                              'https://goo.gl/forms/MqPupXSFYP0NVGuK2')
            db.set_state(message.chat.id, cfg.States.KEYWORD_REQUEST.value)
        else:
            bot.send_document(message.chat.id, 'CgADAgAD7AADTOPxS0NyRNWjbziQAg',
                              caption='А если честно?')
    except ValueError:
        bot.send_document(message.chat.id, 'CgADAgAD7AADTOPxS0NyRNWjbziQAg',
                          caption='Не понимаю, напиши целое число.')


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.KEYWORD_REQUEST.value)
def keyword_request(message):
    # if message.text == '/set_age_1':
    #     db.set_age(message.chat.id, '1')
    #     bot.send_message(message.chat.id, 'Кодовое слово для первой анкеты: Кариес;\nдля второй: Микробы.')
    # else:
        keyword = cfg.keyword(int(db.get_age(message.chat.id)))[0]
        if message.text in {keyword, '/let_me_in'}:
            bot.send_message(message.chat.id, r'Мы, зубы, очень важны! Благодаря нам ты откусываешь и жуешь '
                                              r'все самое вкусное и полезное, правильно произносишь звуки, когда разговариваешь, '
                                              r'и обаятельно улыбаешься. Теперь я расскажу тебе 10 главных '
                                              r'правил по уходу за зубами, внимательно читай и запоминай, я все проверю! Ты готов?',
                             reply_markup=cfg.binary_markup)
            db.set_state(message.chat.id, cfg.States.READINESS_ACCEPTANCE.value)
        else:
            bot.send_message(message.chat.id, 'Хм... Попробуй-ка еще раз. Все мои кодовые слова начинаются с заглавной буквы!') # Если ты указал в анкете не тот возраст, который '
                                          # 'написал мне раньше, то напиши сейчас, какой возраст ты выбрал в анкете - '
                                          # 'тогда твое кодовое слово подойдет!')
            # db.set_state(message.chat.id, cfg.States.OFFERING.value)


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.READINESS_ACCEPTANCE.value)
def lets_begin(message):
    try:
        if message.text in cfg.yes:
            bot.send_message(message.chat.id, 'Поехали!\n✓Правило №1\nКариес – самое распространенное в мире заболевание. '
                                              r'Ученые доказали, что причиной кариеса являются микробы. '
                                              r'Когда ты ешь сладкое, на зубах образуется '
                                              r'липкий налет, который помогает микробам закрепиться на поверхности, '
                                              r'активно размножаться и выделять кислоту. Эта кислота разрушает твердые '
                                              r'ткани зубов и приводит к появлению дефектов («дырочек»), '
                                              r'что и называется кариесом. Вот почему так важно ограничить сладкое и '
                                              r'следить за чистотой зубов!')
            db.set_state(message.chat.id, cfg.States.SLACK.value)
            bot.send_photo(message.chat.id, 'AgADAgADMqkxG0zj8Uvvuw4uq88BGrWgmg4ABFmifWBx9jUD8ScBAAEC',
                           caption='Я тут с тобой заболтался и забыл все на свете. Помоги мне, '
                                   'пожалуйста, вспомнить имя любимого футболиста.',
                           reply_markup=cfg.puyol_markup, disable_notification=True)
            db.set_state(message.chat.id, cfg.States.RULE1.value)
        elif message.text in cfg.no:
            goodbye(message)
        else:
            bot.send_photo(message.chat.id, 'AgADAgADMakxG0zj8Usu-WtxZFlrmXEFMw4ABAn9j-uT1tUBtNMDAAEC',
                           caption='Скажи "Да" или "Нет"')  # cannot_understand.jpg
    except:
        db.set_state(message.chat.id, cfg.States.READINESS_ACCEPTANCE.value)
        bot.send_message(message.chat.id, 'Что-то пошло не так. Пожалуйста, повтори свое предыдущее сообщение.')


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.RULE1.value)
def rule_1_answer(message):
    try:
        if message.text in {'Пуйоль Карлес', 'Карлес Пуйоль', 'пуйоль карлес', 'карлес пуйоль'}:
            bot.send_message(message.chat.id, 'Точно, спасибо!', reply_markup=cfg.default_markup)
            db.set_state(message.chat.id, cfg.States.SLACK.value)
            bot.send_message(message.chat.id, '✓Правило №2\nТщательная гигиена полости рта - залог здоровых зубов и свежего '
                                              'дыхания. Очень важно чистить зубы дважды в день – с утра после еды и вечером '
                                              'перед сном. Также после каждого приема пищи следует промывать полость рта '
                                              'теплой водой или использовать жевательную резинку. Начинать чистку нужно с '
                                              'верхней челюсти, а затем - переходить на нижнюю, а затем не забыть почистить язык. '
                                              'Зубы следует чистить изнутри и снаружи выметающими движениями от десны '
                                              'к режущему краю, а жевательные поверхности зубов – движениями вперед-назад. '
                                              'Смотри на картинки, все просто!', disable_notification=True)
        # gif1 = open(picsdir + 'rule2_1.gif', 'rb')
        # gif2 = open(picsdir + 'rule2_2.gif', 'rb')
            bot.send_document(message.chat.id, 'CgADAgAD7QADTOPxS3rjM6hZAAGIpwI', disable_notification=True)
        # print('rule2_1.gif  ' + tmp.document.file_id)
            bot.send_document(message.chat.id, 'CgADAgAD7gADTOPxSyWL8zZhYUdjAg', disable_notification=True)
        # print('rule2_2.gif  ' + tmp.document.file_id)
            bot.send_message(message.chat.id, 'Чистка должна занимать 3 минуты. Чтобы не стоять с секундомером, включай '
                                              'трехминутную песню и наслаждайся полезным делом, пока она играет.\n'
                                              'Я, например, обычно включаю свою любимую песню. Угадай которую: 1, 2, 3, или 4?',
                            disable_notification=True)
        # track1 = open(picsdir + 'track1.mp3', 'rb')
        # track2 = open(picsdir + 'track2.mp3', 'rb')
        # track3 = open(picsdir + 'track3.mp3', 'rb')
        # track4 = open(picsdir + 'track4.mp3', 'rb')
            bot.send_audio(message.chat.id, 'CQADAgAD8QADTOPxS3OsLsyi-pNHAg', title='1', disable_notification=True)
           # print('tr1  ' + tmp.audio.file_id)
            bot.send_audio(message.chat.id, 'CQADAgAD8gADTOPxS1iwGMrUelB1Ag', title='2', disable_notification=True)
            # print('tr2  ' + tmp.audio.file_id)
            bot.send_audio(message.chat.id, 'CQADAgAD8wADTOPxSyO8lNZy7g_fAg', title='3', disable_notification=True)
            # print('tr3  ' + tmp.audio.file_id)
            bot.send_audio(message.chat.id, 'CQADAgAD9AADTOPxS0wZn1aNH7UIAg', title='4', disable_notification=True)
           # print('tr4  ' + tmp.audio.file_id)
            db.set_state(message.chat.id, cfg.States.RULE2.value)
        else:
            bot.send_message(message.chat.id, 'Нет, точно не так. Надо подумать еще...')
    except:
        db.set_state(message.chat.id, cfg.States.RULE1.value)
        bot.send_message(message.chat.id, 'Что-то пошло не так. Пожалуйста, повтори свое предыдущее сообщение.')


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.RULE2.value)
def rule_2_answer(message):
    try:
        # fave = open(picsdir + 'favorite.mp3', 'rb')
        bot.send_audio(message.chat.id, 'CQADAgADBgEAAi4U8UsPqcPHYss8mQI',
                       disable_notification=True, title='Любимая песня Зуба',
                       caption='Не угадал! Потому что тут нет моей любимой песни. Эта моя любимая ☝')
        # print('trfave  ' + tmp.audio.file_id)
        db.set_state(message.chat.id, cfg.States.SLACK.value)
        bot.send_message(message.chat.id, '✓Правило №3\nОдинаково эффективна как электрическая, так и обычная (мануальная) '
                                          'зубная щетка! Главное - пользоваться ими правильно. Выбирай зубную щетку строго по '
                                          'возрасту. Используй зубную щетку средней жесткости (medium), если стоматолог по '
                                          'показаниям не назначит тебе другую. Для удобства можно выбирать с щеточкой для языка '
                                          '(с резиновыми шипиками) на обратной стороне. Обязательно меняй зубную щетку '
                                          'каждые 2-3 месяца. Щетка с цветными щетинками сама подскажет тебе, '
                                          'когда ее пора заменить – ее цветные щетинки поменяют цвет.')
        bot.send_message(message.chat.id, 'А теперь попробуй разгадать самую сложную в мире загадку:\nМои зубы все белей,\n'
                                          'Раз за разом веселей -\nОна чистит зубы чётко\nУ меня ...')
        db.set_state(message.chat.id, cfg.States.RULE3.value)
    except:
        db.set_state(message.chat.id, cfg.States.RULE2.value)
        bot.send_message(message.chat.id, 'Что-то пошло не так. Пожалуйста, повтори свое предыдущее сообщение.')


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.RULE3.value)
def rule3_answer(message):
    try:
        if message.text in {'зубная щетка', 'Зубная щетка', 'Зубная Щетка', 'зубная щётка', 'Зубная щётка', 'Зубная Щётка'}:
            bot.send_message(message.chat.id, 'Молодец ✌')
            db.set_state(message.chat.id, cfg.States.SLACK.value)
            bot.send_message(message.chat.id, '✓Правило №4\nОчень важно подобрать подходящую именно тебе зубную пасту. '
                                              'Она должна соответствовать твоему возрасту и потребностям. Выбирай противокариозные '
                                              'зубные пасты. Они эффективны на начальной стадии кариеса, а также для его '
                                              'профилактики. С этой целью в пасту добавляют фтор, кальций, ксилит.',
                             disable_notification=True)
            # pic = open(picsdir + 'tasty_paste.jpg', 'rb')
            bot.send_photo(message.chat.id, 'AgADAgADNqkxG0zj8UtdSozLc0CYOE2lmg4ABM7QmYtiUH3mPCYBAAEC',
                           caption='Ну и конечно, выбирай пасту, подходящую по вкусу, чтобы потом '
                                   'не было ко мне претензий! Договорились?', disable_notification=True)
            # print('tasty_paste.jpg  ' + tmp.photo[0].file_id)
            db.set_state(message.chat.id, cfg.States.RULE4.value)
        else:
            bot.send_message(message.chat.id, 'Подумай еще, я уверен, что ты отгадаешь! Ищи подсказку в правиле №3.')
    except:
        db.set_state(message.chat.id, cfg.States.RULE3.value)
        bot.send_message(message.chat.id, 'Что-то пошло не так. Пожалуйста, повтори свое предыдущее сообщение.')


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.RULE4.value)
def rule4_answer(message):
    if message.text not in cfg.yes:
        bot.send_message(message.chat.id, 'Договорились вообще-то! ☝')
        #db.set_state(message.chat.id, cfg.States.SLACK.value)
    bot.send_message(message.chat.id, '✓Правило №5\nКроме зубной щетки и зубной пасты важно применять дополнительные '
                                      'средства гигиены. Зубные нити – флоссы – помогают очистить промежутки между '
                                      'зубами, куда не могут проникнуть щетинки зубной щетки. Ополаскиватели освежают '
                                      'дыхание. А тем, кто носит брекеты, показаны специальные ершики и ирригатор – '
                                      'устройство для очищения зубов в труднодоступных местах струей воды. После еды '
                                      'стоит полоскать рот простой водой или использовать жевательные резинки, но обязательно '
                                      'без сахара (с ксилитом) и не дольше 10-15 минут. Это поможет быстро смыть с '
                                      'поверхности зубов вредные кислоты.')
    bot.send_message(message.chat.id, 'А как ты думаешь, какой из этих фактов (только один) про жевательную резинку – ложь?\n'
                                      '1. Существуют законы, запрещающие жевательную резинку.\n'
                                      '2. На аукционе за использованную жевательную резинку знаменитости было предложено 14000$.\n'
                                      '3. В состав жевательной резинки добавляют рыбий жир.\n'
                                      '4. Пентагон разрабатывает жевательную резинку.')
    db.set_state(message.chat.id, cfg.States.RULE5.value)


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.RULE5.value)
def rule5_answer(message):
    try:
        if message.text in {'1', '2', '3', '4'}:
            if message.text == '3':
                bot.send_message(message.chat.id, 'Молодец, правильно!')
            elif message.text in {'1', '2', '4'}:
                bot.send_message(message.chat.id,
                                 'Нет, на самом деле, в состав жевательной резинки не добавляют рыбий жир, '
                                 'а все остальные факты верны.')
            db.set_state(message.chat.id, cfg.States.SLACK.value)
            bot.send_message(message.chat.id, '✓Правило № 6\nОдним из главных секретов крепких зубов и всего организма '
                                              'является правильное питание. Запомни список самых вредных для зубов продуктов: '
                                              'сладости, сладкие газированные напитки, жареные семечки и орехи, большое '
                                              'количество мягких продуктов, кофе, алкоголь. Негативное влияние на эмаль '
                                              'зубов оказывают сильные перепады температуры, поэтому не стоит употреблять '
                                              'одновременно очень горячие и холодные блюда и напитки (например, запивать '
                                              'мороженное горячим чаем). Ешь те продукты, где больше всего кальция, фтора, '
                                              'фосфора. Поэтому смело налегай на молочные продукты, рыбу, фрукты, овощи и '
                                              'ягоды. Вот я их очень люблю!', disable_notification=True)
            bot.send_photo(message.chat.id, 'AgADAgAD76gxGy4U8Uu3-fULE7GzFNYOnA4ABPsWaHUylBOZ-y0BAAEC',
                           caption='Кажется, мне снова не справиться без твоей помощи. Что лежит на столе на первой картинке, '
                                   'но не лежит на столе на второй?', disable_notification=True)
            db.set_state(message.chat.id, cfg.States.RULE6.value)
        else:
            bot.send_photo(message.chat.id, 'AgADAgADMakxG0zj8Usu-WtxZFlrmXEFMw4ABAn9j-uT1tUBtNMDAAEC',
                           caption='Не понимаю... 1, 2, 3, или 4?')  # cannot_understand.jpg
    except:
        db.set_state(message.chat.id, cfg.States.RULE5.value)
        bot.send_message(message.chat.id, 'Что-то пошло не так. Пожалуйста, повтори свое предыдущее сообщение.')


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.RULE6.value)
def rule6_answer(message):
    try:
        if message.text in {'чеснок', 'Чеснок'}:
            bot.send_message(message.chat.id, 'Какой ты наблюдательный!')
            db.set_state(message.chat.id, cfg.States.SLACK.value)
            bot.send_message(message.chat.id, '✓Правило №7\nРаз в полгода нужно делать профилактический осмотр у врача-стоматолога. '
                                              'Он проверит зубы на наличие кариеса. Начальный кариес лечится быстрее и проще. '
                                              'К доктору стоит немедленно обращаться при появлении любых неприятных или болезненных '
                                              'ощущений, потому что заболевания зубов не проходят сами по себе. Стоматолог '
                                              'определит возникшую проблему, решит ее и даст рекомендации.',
                             disable_notification=True)
            bot.send_photo(message.chat.id, 'AgADAgAD8qgxGy4U8Uvd1xUU-Rp_c9ydmg4ABARo1pmgubre1ikBAAEC',
                           caption='Как считаешь, девушке нужно к стоматологу?', disable_notification=True)
            db.set_state(message.chat.id, cfg.States.RULE7.value)
        else:
            bot.send_message(message.chat.id, 'Смотри внимательнее, в верхней части картинки, белый такой.')
    except:
        db.set_state(message.chat.id, cfg.States.RULE6.value)
        bot.send_message(message.chat.id, 'Что-то пошло не так. Пожалуйста, повтори свое предыдущее сообщение.')


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.RULE7.value)
def rule7_answer(message):
    try:
        bot.send_message(message.chat.id, '✓Правило №8\nК сожалению, домашней чистки недостаточно для полного удаления '
                                          'налета с зубов и эффективной профилактики заболеваний полости рта. Каждые полгода '
                                          'необходимо проводить профессиональную гигиену в кабинете у стоматолога. Такая '
                                          'процедура включает в себя чистку зубов специальными устройствами и инструментами '
                                          'для удаления мягкого и пигментированного налета, полировку поверхностей зубов, а '
                                          'также фторирование - покрытие зубов защищающим от кариеса лаком.')
        db.set_state(message.chat.id, cfg.States.SLACK.value)
        bot.send_photo(message.chat.id, 'AgADAgAD8KgxGy4U-UuQRsVzbE7yyJwKMw4ABPmjW2g9GKZ0Fs8DAAEC',
                       caption='А что бы ты посоветовал этому пациенту?')
        db.set_state(message.chat.id, cfg.States.RULE8.value)
    except:
        db.set_state(message.chat.id, cfg.States.RULE7.value)
        bot.send_message(message.chat.id, 'Что-то пошло не так. Пожалуйста, повтори свое предыдущее сообщение.')


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.RULE8.value)
def rule8_answer(message):
    try:
        bot.send_message(message.chat.id, '✓Правило №9\nОткажись от вредных привычек! Если ты кусаешь ручки и карандаши, '
                                      'грызешь ногти, перекусываешь нитки или открываешь зубами упаковки и крышки, '
                                      'это может стать причиной появления дефектов эмали зубов. А самая пагубная '
                                      'привычка - курение, поскольку сказывается на состоянии не только зубов и десен, '
                                      'но и всего организма. Процесс разрушения зубов у курильщика ускоряется в несколько '
                                      'раз. Под воздействием горячего дыма сигареты в эмали зубов появляются микротрещины, '
                                      'туда проникают никотиновые смолы коричневого цвета. Вычистить их невозможно даже '
                                      'с помощью профессиональной чистки в кабинете стоматолога У заядлых курильщиков '
                                      'темнеют зубы и плохо пахнет изо рта.')
        db.set_state(message.chat.id, cfg.States.SLACK.value)
        bot.send_photo(message.chat.id, 'AgADAgAD8agxGy4U-UudkVVodJunkDukmg4ABCrtyU1efsS8kywBAAEC',
                       caption='Как ты думаешь, Джейсон Стейтем это говорил?', disable_notification=True)
        db.set_state(message.chat.id, cfg.States.RULE9.value)
    except:
        db.set_state(message.chat.id, cfg.States.RULE8.value)
        bot.send_message(message.chat.id, 'Что-то пошло не так. Пожалуйста, повтори свое предыдущее сообщение.')


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.RULE9.value)
def rule9_answer(message):
    try:
        bot.send_message(message.chat.id, 'А я не знаю! В любом случае, эти слова – чистая правда!')
        db.set_state(message.chat.id, cfg.States.SLACK.value)
        bot.send_message(message.chat.id, '✓Правило №10\nДля здоровья зубов очень важно, чтоб они находились в правильном '
                                      'положении. Если это не так, то при жевании нагрузка на зубы распределяется '
                                      'неравномерно и некоторые из них оказываются перегружены, что в дальнейшем '
                                      'приведет к их расшатыванию и выпадению. Оказавшись в желудке, недостаточно '
                                      'пережеванная пища будет плохо усваиваться, следовательно, страдать будет '
                                      'весь организм. Поэтому мы с тобой так часто можем встретить людей с брекетами '
                                      'на зубах. Это значит, что они проходят лечение у стоматолога-ортодонта и приводят '
                                      'свои зубы в правильное положение, ведь теперь мы понимаем, что ровная улыбка - '
                                      'это не только красота, но и здоровье зубов и организма в целом.',
                     disable_notification=True)
        bot.send_photo(message.chat.id, 'AgADAgAD86gxGy4U-UsLzd4R7T1k_y30Aw4ABPPs3tAjL1Xzaw0DAAEC', disable_notification=True)
        bot.send_photo(message.chat.id, 'AgADAgAD8qgxGy4U-UtL443pcou00W7qAw4ABOpliQuxSXjC5QkDAAEC',
                       caption='Теперь ты знаешь, зачем нужны брекеты?', disable_notification=True)
        db.set_state(message.chat.id, cfg.States.RULE10.value)
    except:
        db.set_state(message.chat.id, cfg.States.RULE9.value)
        bot.send_message(message.chat.id, 'Что-то пошло не так. Пожалуйста, повтори свое предыдущее сообщение.')


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.RULE10.value)
def rule10_answer(message):
    bot.send_message(message.chat.id, 'Вот это да! Ты терпеливо выслушал меня до самого конца, ты в шаге от получения '
                                      'заветных стикеров! Проверим твои знания теперь. Скорее проходи анкету еще раз и '
                                      'присылай мне оттуда твое индивидуальное кодовое слово! Удачи!\n'
                                      'https://goo.gl/forms/fG2i6rmwPKgtJqtt1')
    db.set_state(message.chat.id, cfg.States.FINISH_HIM.value)


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.FINISH_HIM.value)
def stickersgiving(message):
    bot.send_message(message.chat.id, 'Я тобой горжусь! Держи заслуженный подарок!')
    db.set_state(message.chat.id, cfg.States.THE_END.value)


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == cfg.States.THE_END.value)
def paschalochki(message):
    bot.send_message(message.chat.id, 'Ты же уже все прошел, нет? Хочешь еще разок попробовать? Ну тогда нажми /start')


while 1 < 2:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(e)
        time.sleep(5)
