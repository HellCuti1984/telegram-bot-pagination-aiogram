from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.exceptions import MessageNotModified

import config
from keyboards.pagination import pagination_callback, pagination_keyboard


async def pagination(call: CallbackQuery, callback_data: dict):
    current_index = int(callback_data.get('current_index'))

    await call.answer()
    try:
        await call.message.edit_text(text='КОНТЕНТ',
                                     reply_markup=pagination_keyboard(current_index, config.CONTENT))
    except MessageNotModified:
        return


async def bot_start(message: Message):
    markup = InlineKeyboardMarkup()
    markup.insert(*[
        InlineKeyboardButton(text='Пагинация', callback_data='pagination')
    ])

    await message.answer(text='ТЕСТ ПАГИНАЦИИ', reply_markup=markup)


async def pagination_start(call: CallbackQuery):
    # ЗАДАЕМ НАЧАЛЬНЫЙ ИНДЕКС
    current_index = 0

    # НЕОБХОДИМЫЙ КОНТЕНТ НА ВЫВОД
    config.CONTENT = [{'Тест': 'Тест'}]

    # СОЗДАНИЕ КЛАВИАТУРЫ С КОНТЕНТОМ И СТРОКОЙ ПАГИНАЦИИ
    keyboard = pagination_keyboard(index=current_index, content=config.CONTENT)

    # ВЫВОД КЛАВИАТУРЫ ПОЛЬЗОВАТЕЛЮ
    await call.message.edit_text(text='ТЕСТ',
                                 reply_markup=keyboard)


async def current_index_handler(call: CallbackQuery):
    await call.answer(':)')


def register_pagination_handler(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands='start')
    dp.register_callback_query_handler(pagination_start, text='pagination')
    dp.register_callback_query_handler(current_index_handler, text='current')
    dp.register_callback_query_handler(pagination, pagination_callback.filter())
