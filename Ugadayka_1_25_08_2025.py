from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

BOT_TOKEN = '8445782970:AAE07CH8EuQZ-OOoDUbzfDG07n-FiGrw2Y4'

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

user_data = {'low': 1,
             'high': 100,
             'cur_num': None,
             'status': False}

def return_data():
    user_data = {'low': 1,
                 'high': 100,
                 'cur_num': None,
                 'status': False}

def num():
    user_data['cur_num'] = user_data['low'] + (user_data['high'] - user_data['low']) // 2

async def ask_num(message: Message):
    num()
    await message.answer(f'Ты загадал {user_data['cur_num']}?')

def basic_response():
    return 'Ты в игре! '\
           'Во время игры я распознаю лишь подсказки '\
           '- больше или меньше. Укажи одну из них. '\
           'Или выйди из игры командой /cancel'

def check():
    return user_data['low'] != user_data['high']

def check_error():
    return 'Не получится меня наколоть, друожок! '\
           f'Твое число было = {user_data['cur_num']} '\
           'Текущая игра завершена.'

@dp.message(CommandStart())
async def process_start_command(message: Message):
    user_data['status'] = True
    await message.answer(
        'Привет!\nДавай сыграем в игру?\n\n'
        'Загадай мне число от 1 до 100. '
        'После каждого из предложенных мной вариантов '
        'давай подсказку - больше или меньше.'
        'Если я угадал, ответь - угадал!'
        'Играем?'
    )

@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    user_data['low'] = 1
    user_data['high'] = 100
    await message.answer('Что ж, возвращайся. '
                         'Сыграем по новой!')


@dp.message(F.text.lower().in_(['да', 'давай']))
async def process_positive_answer(message: Message):
    if user_data['status']:
        await message.answer(basic_response())
    else:
        user_data['status'] = True
        await ask_num(message)

@dp.message(F.text.lower().in_(['нет', 'не хочу']))
async def process_positive_answer(message: Message):
    if user_data['status']:
        await message.answer(basic_response())
    else:
        await message.answer('Очень жаль. Заходите, когда решите сыграть партеечку.')

@dp.message(F.text.lower().in_(['больше']))
async def process_positive_num(message: Message):
    if user_data['status']:
        if check():
            user_data['low'] = user_data['cur_num'] + 1
            await ask_num(message)
        else:
            await message.answer(check_error())
            return_data()
    else:
        await message.answer(basic_response())

@dp.message(F.text.lower().in_(['меньше']))
async def process_negative_num(message: Message):
    if user_data['status']:
        if check():
            user_data['high'] = user_data['cur_num'] - 1
            await ask_num(message)
        else:
            await message.answer(check_error())
            return_data()
    else:
        await message.answer(basic_response())

@dp.message(F.text.lower().in_(['угадал']))
async def process_true_num(message: Message):
    return_data()
    await message.answer('Видишь, какой я красавчик!'
                         'Ну заходи еще как-нибудь!')

@dp.message()
async def process_other_answers(message: Message):
    if user_data['status']:
        await message.answer(basic_response())
    else:
        await message.answer('Я бот, который распознает лишь '
                             'определенные ответы. Сыграем?')

if __name__ == '__main__':
    dp.run_polling(bot)