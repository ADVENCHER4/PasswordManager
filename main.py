import aiogram

import execute

MY_ID =
bot = aiogram.Bot(token=TOKEN)
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def send_welcome(message: aiogram.types.Message):
    await bot.send_message(message.from_user.id, '/services - все сервисы в базе данных\n'
                                                 '/logins "сервис" - логины для указанного сервиса\n'
                                                 '/write "ключ" - создание нового пароля\n'
                                                 '/read "ключ" - чтение пароля\n'
                                                 '/rewrite "ключ" - изменение пароля у существующей записи\n')


aiogram.executor.start_polling(dp, skip_updates=True)

