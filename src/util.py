import logging
from functools import wraps

from bs4 import BeautifulSoup
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

# Require x non-command messages between each /rules etc.
RATE_LIMIT_SPACING = 5


def get_reply_id(update):
    if update.message and update.message.reply_to_message:
        return update.message.reply_to_message.message_id
    return None


def reply_or_edit(update, context, text):
    chat_data = context.chat_data
    if update.edited_message:
        chat_data[update.edited_message.message_id].edit_text(text,
                                                              parse_mode=ParseMode.HTML,
                                                              disable_web_page_preview=True)
    else:
        issued_reply = get_reply_id(update)
        if issued_reply:
            chat_data[update.message.message_id] = context.bot.sendMessage(update.message.chat_id, text,
                                                                           reply_to_message_id=issued_reply,
                                                                           parse_mode=ParseMode.HTML,
                                                                           disable_web_page_preview=True)
        else:
            chat_data[update.message.message_id] = update.message.reply_text(text,
                                                                             parse_mode=ParseMode.HTML,
                                                                             disable_web_page_preview=True)


def get_text_not_in_entities(html):
    soup = BeautifulSoup(html, 'html.parser')
    return ' '.join(soup.find_all(text=True, recursive=False))


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def rate_limit_tracker(update: Update, context: CallbackContext):
    data = context.chat_data.get('rate_limit', {})

    for key in data.keys():
        data[key] += 1


def rate_limit(f):
    """
    Rate limit command so that RATE_LIMIT_SPACING non-command messages are
    required between invocations.
    """

    @wraps(f)
    def wrapper(update, context, *args, **kwargs):
        # Get rate limit data
        try:
            data = context.chat_data['rate_limit']
        except KeyError:
            data = context.chat_data['rate_limit'] = {}

        # If we have not seen two non-command messages since last of type `f`
        if data.get(f, RATE_LIMIT_SPACING) < RATE_LIMIT_SPACING:
            logging.debug('Ignoring due to rate limit!')
            return

        data[f] = 0

        return f(update, context, *args, **kwargs)

    return wrapper
