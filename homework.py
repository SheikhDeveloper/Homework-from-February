import telebot
import types
import json

bot = telebot.TeleBot('5177849308:AAHl7pBzEbHdq1BEuf3mapu-ZjSUO56xAtY')

def read_json():
  with open('userdata.json') as f:
    data = json.loads(json.load(f))
  return data

def input_json(diction):
  ##try:
  with open('userdata.json','w') as f:
    json.dump(json.dumps(diction), f)
  return True
  ##except BaseException:
    ##return False

def rewrite_json(tag, sth, change, data_of_users):
  data_of_users['Players'] [tag] [sth] = change
  check = input_json(data_of_users)
  if check:
    bot.send_message(int(tag), 'Данные успешно изменены')
  else:
    bot.send_message(int(tag), 'Произошла ошибка при загрузке данных. Снова введите данные и повторите попытку')

def put_name(dannye, tag, message):
  global stage_of_game
  data_of_player = {tag: {}}
  dannye['Players'].update(data_of_player)
  dannye ['Players'] [tag] ['Name'] = message.text
  stage_of_game += 1

def put_password(dannye, message, tag):
  global stage_of_game
  dannye['Players'] [tag] ['Password'] = message.text
  stage_of_game += 1

def nach_game_profile(dannye, tag):
  nach_gamepr = { tag: {}}
  dannye['Game Profile'].update(nach_gamepr)
  dannye['Game Profile'] [tag] ['Strength'] = 1
  dannye['Game Profile'] [tag] ['Endurance'] = 1
  dannye['Game Profile'] [tag] ['Luck'] = 1
  dannye['Game Profile'] [tag] ['Balance'] = 3500

def game_menu(id):
  menu_markup = telebot.types.InlineKeyboardMarkup()
  menu_markup.add(telebot.types.InlineKeyboardButton(
    text = 'Посмотреть данные игрового профиля',
    callback_data = 1
  ))
  menu_markup.add(telebot.types.InlineKeyboardButton(
    text = 'Посмотреть персональные данные',
    callback_data = 2))
  menu_markup.add(telebot.types.InlineKeyboardButton(
    text = 'Изменить персональные данные',
    callback_data = 3))
  greeting = 'Добро пожаловать, ' + dan['Players'] [id] ['Name'] + '\n' + 'Что желаешь сделать ?'
  bot.send_message(int(id), greeting, reply_markup = menu_markup)

def see_gamedata(data, tag, menu_return):
  strength = 'Сила - ' + str(
    data['Game Profile'] [tag] ['Strength']) + '\n'
  endurance = 'Выносливость - ' + str(
    data['Game Profile'] [tag] ['Endurance']) + '\n'
  luck = 'Удача - ' + str(
    data['Game Profile'] [tag] ['Luck']) + '\n'
  balance = 'Баланс: ' + str(
    data['Game Profile'] [tag] ['Balance']
  ) + '$'
  gamedata_message = strength + endurance + luck + balance
  bot.send_message(
    int(tag), 
    gamedata_message, 
    reply_markup = menu_return)

def see_data(data, tag, menu_return):
  name = 'Имя - ' + data['Players'] [tag] ['Name'] + '\n'
  password = 'Пароль - ' + data['Players'] [tag] ['Password']
  data_message = name + password
  bot.send_message(
    int(tag), 
    data_message, 
    reply_markup = menu_return)



stage_of_game = 0
for_change = 0
sam_change = ''
dan = read_json()


@bot.message_handler(commands = ['start'])
def start_message(message):
  global dan
  global stage_of_game
  tag = str(message.chat.id)
  if tag in dan['Players']:
    game_menu(tag)
    stage_of_game = 2
  else:
    newbie_actions = telebot.types.InlineKeyboardMarkup()
    newbie_actions.add(telebot.types.InlineKeyboardButton(
      text = 'Зарегистрироваться',
      callback_data = 4))
    greeting = 'Здравствуй, путник, представься'
    bot.send_message(
      message.chat.id, 
      greeting, 
      reply_markup = newbie_actions)

@bot.callback_query_handler(func = lambda call: True)
def query_handler(call):
  global dan
  global for_change
  global sam_change
  return_to_menu = telebot.types.InlineKeyboardMarkup()
  return_to_menu.add(
    telebot.types.InlineKeyboardButton(
     text = 'Вернуться в меню', 
     callback_data = 7 ))
  tagg = str(call.message.chat.id)
  if call.data ==  '1':
    see_gamedata(dan, tagg, return_to_menu)
  if call.data == '2':
    see_data(dan, tagg, return_to_menu)
  if call.data == '3':
    data_change_keyboard = telebot.types.InlineKeyboardMarkup()
    password_button = telebot.types.InlineKeyboardButton(
      text = 'Пароль',
      callback_data = 5)
    name_button = telebot.types.InlineKeyboardButton(
      text = 'Имя',
      callback_data = 6
    )
    data_change_keyboard.row(
      password_button, 
      name_button)
    bot.send_message(
      call.message.chat.id, 
      'Что желаете изменить ?', 
      reply_markup = data_change_keyboard)
    for_change += 1
  if call.data == '4':
    bot.send_message(
      int(tagg), 
      'Введите свое имя')
  if call.data == '5':
    sam_change = 'password'
    bot.send_message(
      int(tagg),
      'Введите новый пароль')
  if call.data == '6':
    sam_change = 'name'
    bot.send_message(
      int(tagg),
      'Введите ваше новое имя')
  if call.data == '7':
    game_menu(tagg)
      

@bot.message_handler(content_types = ['text'])
def message_handle(message):
  global dan
  global stage_of_game
  global for_change
  global sam_change
  tag = str(message.chat.id)
  if for_change == 0:
    if stage_of_game == 0:
      put_name(dan, tag, message)
      bot.send_message(
        int(tag),
        'Отлично, теперь придумайте пароль')
    elif stage_of_game == 1:
      put_password(dan, message, tag)
      nach_game_profile(dan, tag)
      input_json(dan)
      bot.send_message(
        int(tag),
        'Отлично, вы зарегестрированы')
      game_menu(tag)
      stage_of_game += 1
    elif stage_of_game == 2:
      bot.send_message(
        int(tag),
        'Прости, но я просто бот и пока не умею говорить на человеческом🤖')
  elif for_change == 1:
    if sam_change == 'password':
      needed_change = 'Password'
      rewrite_json(tag, needed_change, message.text, dan)
      game_menu(tag)
      for_change = 0
    elif sam_change == 'name':
      needed_change = 'Name'
      rewrite_json(tag, needed_change, message.text, dan)
      game_menu(tag)
      for_change = 0

bot.infinity_polling()