from app.presence_event import PresenceEvent


class EventQueue:

    def __init__(self):
        self._queue = list()
        self._time_between_events = 0

    @property
    def time_between_events(self):
        return self._time_between_events

    def push(self, epoch_seconds, event: PresenceEvent):
        if len(self._queue) > 0:
            assert epoch_seconds > self.last()['at']
            self._time_between_events = epoch_seconds - self.last()['at']
        self._queue.append({'at': epoch_seconds, 'event': event})

    def clear_until(self, epoch_seconds):
        self._queue = [item for item in self._queue if item['at'] < epoch_seconds]

    def iterate_until(self, epoch_seconds):
        return [item for item in self._queue if item['at'] >= epoch_seconds]

    def last(self):
        return self._queue[-1]

    def last_event(self):
        return self.last()['event']

    def first(self):
        return self._queue[0]
