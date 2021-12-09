import time
import random
import threading

import requests

endpoints = ('', 'message1', 'message2', 'message3', 'movies')


def run():
    while True:
        try:
            target = random.choice(endpoints)
            requests.get("http://10.104.135.34/%s" % target, timeout=1)

        except:
            pass


if __name__ == '__main__':
    for _ in range(4):
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    while True:
        time.sleep(1)