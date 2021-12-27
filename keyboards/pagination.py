from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

import config

pagination_callback = CallbackData('pagination', 'current_index')


def get_like_pages(content, get_after_index=0, limit=10):
    data = []
    get_after_index *= limit
    content_count = len(content)
    iterator = 0

    is_limit_correct_val = content_count - get_after_index
    if is_limit_correct_val < limit:
        limit = is_limit_correct_val - 1

    if get_after_index is not 0:
        for i in range(get_after_index, content_count):
            data.append(content[i])
            if iterator is limit:
                return data
            else:
                iterator += 1
    else:
        for i in range(0, content_count):
            data.append(content[i])
            if iterator is limit:
                return data
            else:
                iterator += 1


def get_prev_next_index(index):
    if index == config.min_index:
        previous_index = index
    else:
        previous_index = index - 1

    if index == config.max_index:
        next_index = index
    else:
        next_index = index + 1

    return previous_index, next_index


def get_prev_next_buttons(previous_index, next_index, callback_factory):
    return [
        InlineKeyboardButton(
            text='⬅',
            callback_data=callback_factory.new(current_index=previous_index)
        ),
        InlineKeyboardButton(
            text='➡',
            callback_data=callback_factory.new(current_index=next_index)
        )
    ]


def pagination_keyboard(index, content):
    previous_buttons = [
        InlineKeyboardButton(
            text=f"{i + 1}",
            callback_data=pagination_callback.new(current_index=i)
        )
        for i in range(index - 2, index)
        if 0 <= i <= len(content)
    ]

    previous_buttons.append(InlineKeyboardButton(
        text=f'|{index + 1}|',
        callback_data='current'
    ))

    # ИНИЦИАЛИЗАЦИЯ КОНТЕНТА НА СТРАНИЦУ
    limit_on_page_item = 10
    page_of_content = get_like_pages(content, index, limit_on_page_item)

    next_buttons = [
        InlineKeyboardButton(
            text=f"{i + 1}",
            callback_data=pagination_callback.new(current_index=i)
        )
        for i in range(index + 1, index + 3)
        if i <= len(content)
    ]

    buttons = previous_buttons + next_buttons
    keyboard = InlineKeyboardMarkup(row_width=5)

    for cont in page_of_content:
        keyboard.row(InlineKeyboardButton(text=str(cont), callback_data=f"{cont}"))
    keyboard.add(*buttons)

    previous_index, next_index = get_prev_next_index(index)
    buttons = get_prev_next_buttons(previous_index=previous_index, next_index=next_index,
                                    callback_factory=pagination_callback)
    keyboard.add(*buttons)

    return keyboard
