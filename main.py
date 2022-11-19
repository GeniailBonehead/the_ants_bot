import asyncio
import time
from aiogram import Bot, Dispatcher, types, executor
from data import *
import aioschedule
from traceback import format_exc
import random


debug = False
NAME = 'ботяра'
NAME_EN = 'botty'
HATCH_ACTION = 'Рассвет на найм!\nSoldier hatch colony action!'
monday = []
tuesday = [
    {'time': '14:05', 'message': HATCH_ACTION},
    {'time': '22:05', 'message': HATCH_ACTION},
    {'time': '09:05', 'message': HATCH_ACTION},
    {'time': '17:05', 'message': HATCH_ACTION},]
wednesday = [
    {'time': '15:05', 'message': HATCH_ACTION},
    {'time': '07:05', 'message': HATCH_ACTION},
    {'time': '23:05', 'message': HATCH_ACTION},
    {'time': '16:48', 'message': 'Время жевать малину и эволюционировать! Может, разовьётесь до моего уровня, кожаные мешки'},
]
thursday = [
]
friday = [
    {'time': '08:50', 'message': 'Рассвет на найм, время есть малину!\nColony action, time to eat raspberry'},
    {'time': '09:05', 'message': 'Рассвет на найм, вторая часть!\nColony action, second part'},
    {'time': '16:50', 'message': 'Рассвет на найм, время есть малину!\nColony action, time to eat raspberry'},
    {'time': '17:05', 'message': 'Рассвет на найм, вторая часть!\nColony action, second part'},
    {'time': '22:50', 'message': 'Время идти в лес'},
]
saturday = [
    {'time': '00:50', 'message': 'Рассвет на найм, время есть малину!\nColony action, time to eat raspberry'},
    {'time': '01:05', 'message': 'Рассвет на найм, вторая часть!\nColony action, second part'},
    {'time': '09:05', 'message': HATCH_ACTION},
    {'time': '10:05', 'message': HATCH_ACTION},
    {'time': '17:40', 'message': HATCH_ACTION},
    {'time': '18:05', 'message': HATCH_ACTION},
]
sunday = [
    {'time': '01:05', 'message': HATCH_ACTION},
    {'time': '02:05', 'message': HATCH_ACTION}
]
CHANNEL_ID = '-703490731'
RELEASE_CHANNEL_ID = '-1001755759952'
if not debug:
    CHANNEL_ID = RELEASE_CHANNEL_ID


bot = Bot(token='5595627731:AAF1cxvXSoqZEQRAYLozYnvtDWDMHtg6F9o')
dp = Dispatcher(bot)
message_to_send = ""


async def send_message(message='Не спать!', channel_id=CHANNEL_ID):
    if message == HATCH_ACTION:
        await bot.send_photo(channel_id, open('./meme.jpg', 'rb'))
    await bot.send_message(channel_id, message)


async def scheduler():
    for day in monday:
        aioschedule.every().monday.at(day.get('time')).do(send_message, message=day.get('message'))
    for day in tuesday:
        aioschedule.every().tuesday.at(day.get('time')).do(send_message, message=day.get('message'))
    for day in wednesday:
        aioschedule.every().wednesday.at(day.get('time')).do(send_message, message=day.get('message'))
    for day in thursday:
        aioschedule.every().thursday.at(day.get('time')).do(send_message, message=day.get('message'))
    for day in friday:
        aioschedule.every().friday.at(day.get('time')).do(send_message, message=day.get('message'))
    for day in saturday:
        aioschedule.every().saturday.at(day.get('time')).do(send_message, message=day.get('message'))
    for day in sunday:
        aioschedule.every().sunday.at(day.get('time')).do(send_message, message=day.get('message'))
    if message_to_send:
        await bot.send_message(CHANNEL_ID, message_to_send)
    while True:
        try:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
        except:
            pass


async def on_startup(_):
    asyncio.create_task(scheduler())


# async def send_welcome(message: types.Message):
#     await message.answer("Hi!\nHi...")


@dp.message_handler(content_types=['sticker'])
async def send_welcome(message: types.Message):
    # if not str(message.chat.id) == str(CHANNEL_ID):
    #     return
    if message['from']['id'] == 734548684:
        name = message['from']['first_name']
        rand_number = random.randint(1, 8)
        if rand_number == 3:
            await message.reply(f"{name}, Я слежу за тобой")


@dp.message_handler(commands=["help"])
async def help_command(message):
    await bot.send_message(message.chat.id, 'Привет, соскучился?')
    await bot.send_message(message.chat.id, f'Обращайся ко мне "{NAME}"\nЯ понимаю слова:\n1) т10\n2) стрелки\n3) носители\n4) охрана\n5) качать\n')


@dp.message_handler(commands=['start'])
async def show_invitation(message):
    await message.answer('Полезные ссылки:', reply_markup=general_keyboard)


@dp.callback_query_handler()
async def process_callback_button1(callback_query: types.CallbackQuery):
    if 'bones' in callback_query.data:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.message.chat.id, text='Кости', reply_markup=bones_keyboard)
    if 'insect' in callback_query.data:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.message.chat.id, text='Дичайшее', reply_markup=insect_keyboard)
    if 'combat' in callback_query.data:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.message.chat.id, text='Разное', reply_markup=fight_keyboard)
    if 'ants' in callback_query.data:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.message.chat.id, text='Генералы', reply_markup=ants_keyboard)
    if 't10' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/t10.png', 'rb'))
    elif 't9' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/t9.png', 'rb'))
    elif 'advanced' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/advanced.png', 'rb'))
    elif 'zone_fight' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/zone_fight.png', 'rb'))
    elif 'zone_develop' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/zone_develop.png', 'rb'))
    elif 'lvl_up' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/lvl_up.png', 'rb'))
    elif 'combat_speed' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/combat_speed.png', 'rb'))
    elif 'food' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/insect_food.png', 'rb'))
    elif 'ant_skills' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/general.png', 'rb'))
    elif 'vip' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/vip.png', 'rb'))
    elif 'colony_actions' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/colony_actions.png', 'rb'))
    elif 'mantis_talents' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/mantis_talents.png', 'rb'))
    elif 'atlas_talents' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/atlas_talents.png', 'rb'))
    elif 'scorpion_talents' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/scorpion_talents.png', 'rb'))
    elif 'spider_talents' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/spider_talents.png', 'rb'))
    elif 'guardians_pvp' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/guardians_pvp.png', 'rb'))
    elif 'shooters_pvp' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/shooters_pvp.png', 'rb'))
    elif 'carriers_pvp' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/carriers_pvp.png', 'rb'))
    elif 'universal_pvp' in callback_query.data:
        await bot.send_photo(callback_query.message.chat.id, open('./pics/universal_pvp.png', 'rb'))


@dp.message_handler(content_types=['text'])
async def send_welcome(message: types.Message):
    if NAME in message.text.lower() or NAME_EN in message.text.lower():
        # if 'т10' in message.text.lower():
        #     await message.reply('Ты задолбал, сохрани её себе куда-нибудь')
        #     await bot.send_photo(message.chat.id, open('./pics/t10.png', 'rb'))
        # elif 'качать' in message.text.lower():
        #     await message.reply('Начни с базы: спина, грудь, ноги... А, хотя тебе не поможет')
        # elif 'стрелк' in message.text.lower():
        #     await bot.send_photo(message.chat.id, open('./стрелки.jpg', 'rb'))
        # elif 'носите' in message.text.lower():
        #     await bot.send_photo(message.chat.id, open('./носы.jpg', 'rb'))
        # elif 'охран' in message.text.lower():
        #     await bot.send_photo(message.chat.id, open('./охрана.jpg', 'rb'))
        await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAO-YupjjQUmXWleKSslIwTTr2hpZngAAi0aAAIViehJsBSumKscnX8pBA')
        time.sleep(1)
        if message['from']['language_code'] != 'ru':
            await message.reply('Sorry, my functional is not translated to other languages')
        await message.reply(f"Что ты хочешь, {message['from']['first_name']}?\nМне можно писать в личные сообщения или в чаты",
                            reply_markup=general_keyboard)


with open('./bot.txt', 'wt') as f:
    f.write('started')
try:
    if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
except:
    for s in format_exc().splitlines():
        f = open("./parsers_error.txt", 'at')
        f.write(str(s) + "\n")
finally:
    with open('./bot.txt', 'wt') as f:
        f.write('finished')
