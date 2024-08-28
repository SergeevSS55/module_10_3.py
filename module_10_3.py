import threading
from time import sleep
from random import randint


# Цель: освоить блокировки потоков, используя объекты класса Lock и его методы

class Bank:
    def __init__(self):
        self.balance: int = 0  # баланс банка
        self.lock = threading.Lock()  # объект класса Lock для блокировки потоков

    def deposit(self):  # метод совершает 100 циклов "пополнения" баланса
        for i in range(100):
            rep = randint(50, 500)  # случайное число от 50 до 500
            self.balance += rep  # пополнение баланса на случайное число
            if self.balance >= 500 and self.lock.locked():  # условия пополнения баланса
                self.lock.release()  # разблокирование баланса при соблюдении условий
            print(f'Пополнение: {rep}. Баланс: {self.balance}')
            sleep(0.001)

    def take(self):  # метод совершает сто циклов по уменьшению баланса
        for i in range(100):
            wit = randint(50, 500)  # случайное число от 50 до 500
            print(f'Запрос на {wit}')
            if wit <= self.balance:  # если случайное число меньше баланса, то происходит списание средств
                self.balance -= wit
                print(f"Снятие: {wit}. Баланс: {self.balance}")
                sleep(0.001)
            if wit > self.balance:  # если запрос на снятие больше, чем баланс, то происходит блокировка
                print(f'Запрос отклонён, недостаточно средств')
                self.lock.acquire()
            sleep(0.001)


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
