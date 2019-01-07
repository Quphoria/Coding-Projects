from kulka import Kulka
import time


def main():
    with open('mykulka.txt') as file_:
        addr = file_.readline().strip()

    with Kulka(addr) as kulka:
        kulka.set_inactivity_timeout(3600)

        for _ in xrange(10):
            kulka.set_rgb(0xFF, 0, 0)
            time.sleep(0.1)
            kulka.set_rgb(0, 0, 0)
            time.sleep(0.1)

        kulka.sleep()


if __name__ == '__main__':
    main()
