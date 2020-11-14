import argparse
import sys
# from telegram.ext import Updater, CommandHandler
# import requests
# import re


DEBUG = False  # Variabile globale per abilitare i messaggi di debug


# Legge il token dal file passato come parametro
def get_token(path):
    if DEBUG:
        print("TOKEN PATH: %s" % path)

    try:
        with open(path, 'r') as token_file:
            token = token_file.read()
    except Exception as e:
        if DEBUG:
            print(e)
        print("PICCHE!")
        sys.exit()
    return token


# Funzione principale, il bot gira qui
def main(token_path):
    token = get_token(token_path)
    if DEBUG:
        print("TOKEN")
        # print("TOKEN: %s" % token)   # Non far vedere il tuo token quando sei in live


# Setup delle opzioni, comincia tutto da qui
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", default=False)
    parser.add_argument("-t", "--token", action="store")
    args = parser.parse_args()

    if args.debug:
        DEBUG = True
        print("DEBUG ATTIVO")

    if not args.token:
        print("Hey pirletto, devi darmi un token senno\' non funziono!")
        sys.exit()

    main(args.token)
