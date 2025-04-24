from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

from sqlquery import check_employees, update_status_order

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN: str = '5055705391:AAG3vFzypYSJlDo5Q4yAV4g0gPzmS-rf2u8'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer('для изменения статуса заказа отправь сообщение вида:\n'
                         '{номер заказа} статус\n'
                         'например: 12314 В ожидании\n'
                         'Возможные статусы: В ожидании/Доставлено/В процессе')


# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    user_id = message.from_user.id
    text = message.text
    if check_employees(user_id):
        # print(f"Пользователь {user_id} отправил сообщение: {text}")
        # print(text.strip()[0], ' '.join(text.split()[1:]))
        update_status_order(status = ' '.join(text.split()[1:]),order_id = text.strip()[0])
        await message.reply(text='Сообщение принято')
    else:
        await message.reply(text='Вы не зарегистрированы в системе')

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
