from telegram.ext import Updater, CommandHandler
import requests
import re
import sys
import argparse

DEBUG = False


def get_token(path):
    if DEBUG:
        print(path)
    try:
        with open(path, "r") as token_file:
            token = token_file.read()
    except Exception as e:
        if DEBUG:
            print(e)
        print("PICCHE!")
        sys.exit()

    return token


def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def bop(update, context):
    url = get_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


def main(token_path):
    token = get_token(token_path)

    if DEBUG:
        pass
        # print(token)

    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--azz", action="store_true", default=False)
    parser.add_argument("-d", "--debug", action="store_true", default=False)
    parser.add_argument("-t", "--token", action="store", default=False)
    args = parser.parse_args()

    if args.azz:
        print("AZZ")
    if args.debug:
        DEBUG = True
    if not args.token:
        print("We pirletto! Devi darmi il token!")
        sys.exit()

    main(args.token)
