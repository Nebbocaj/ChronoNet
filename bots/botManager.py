import time
from bot import Bot
from aitextgen import aitextgen
import pickle
import random

text_gen = aitextgen()


def loadBot(username):
    filepath = "saved_bots/{}.data".format(username)
    return pickle.load(open(filepath, "rb"))

def saveBot(b):
    filepath = "saved_bots/{}.data".format(b.username)
    pickle.dump(b, open(filepath, "wb"))

bots = []

# create/load bots
for i in range(10):
    username = "bot_{}".format(i)
    
    try:
        bot = loadBot(username)
    except (OSError, IOError) as e:
        bot = Bot(username)
        bot.createAccount()
        saveBot(bot)
    
    bots.append(bot)

# make posts

while True:
    # pick a random bot and post
    bot = random.choice(bots)
    bot.makePost(text_gen)
    saveBot(bot)

    # wait a moment, repeat
    time.sleep(1)
