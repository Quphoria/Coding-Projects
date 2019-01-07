from kulka import Kulka


def main():
    with open('mykulka.txt') as file_:
        addr = file_.readline().strip()

    with Kulka(addr) as kulka:
        kulka.sleep()




if __name__ == '__main__':
    main()
