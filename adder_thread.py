import threading


class AdderThread(threading.Thread):
    stopSignal = False

    def __init__(self):