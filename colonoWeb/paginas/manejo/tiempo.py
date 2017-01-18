import time


def hora():
    return "Hora " + time.strftime("%X")


def dormir(n):
    time.sleep(n)
    return
