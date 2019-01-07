from kulka import Kulka
from itertools import repeat
from random import randint
import time


def main():
    with open('mykulka.txt') as file_:
        addr = file_.readline().strip()

    with Kulka(addr) as kulka:
        kulka.set_inactivity_timeout(3600)

        for _ in repeat(None, 600):
            kulka.roll(randint(30, 100), randint(0, 359))
            time.sleep(1)

        kulka.sleep()


if __name__ == '__main__':
    main()
