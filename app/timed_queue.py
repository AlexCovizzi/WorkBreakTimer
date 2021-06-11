class TimedQueue:

    def __init__(self):
        self._queue = list()
        self._max_age_seconds = 86400  # 24 Hours
        self._time_between_items = 0

    @property
    def time_between_items(self):
        return self._time_between_items

    def push(self, epoch_seconds, item):
        if len(self._queue) > 0:
            assert epoch_seconds > self.last()['at']
            self._time_between_items = epoch_seconds - self.last()['at']
        self._queue.append({'at': epoch_seconds, 'item': item})
        self.clear_until(epoch_seconds - self._max_age_seconds)

    def clear_until(self, epoch_seconds):
        while len(self._queue) > 0 and self.first()['at'] < epoch_seconds:
            self._queue.pop(0)

    def iterate_from(self, epoch_seconds):
        return [item for item in self._queue if item['at'] >= epoch_seconds]

    def last(self):
        return self._queue[-1] if len(self._queue) > 0 else None

    def last_event(self):
        return self._queue[-1]['item'] if len(self._queue) > 0 else None

    def first(self):
        return self._queue[0]
