from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

btnMain = KeyboardButton('Главное меню')

btnWeather = KeyboardButton('Погода')
btnYoutube = KeyboardButton('Python')
btnOther = KeyboardButton('Другое')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnWeather, btnYoutube, btnOther)

btnAvatar = KeyboardButton('Аватар')
btnInfo = KeyboardButton('Справочник')
btnGame = KeyboardButton('Игра')
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAvatar, btnInfo, btnGame, btnMain)

mainIn = InlineKeyboardMarkup(row_width=2)
btnUrl = InlineKeyboardButton(text='Chanel', url='https://t.me/zen_of_python')
btnht = InlineKeyboardButton(text='Documentation', url='https://www.python.org/')

mainIn.insert(btnUrl)
mainIn.insert(btnht)
