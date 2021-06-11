class Subscribable:

    def __init__(self):
        self._table = {}

    def subscribe(self, topic, func):
        self._table[topic] = func

    def publish(self, topic, message):
        func = self._table.get(topic, None)
        if func:
            func(message)
