from app.event_queue import EventQueue
from enum import Enum
from app.presence_event import PresenceEvent


class NextAction(Enum):
    DO_NOTHING = 'DO_NOTHING'
    DO_BREAK = 'DO_BREAK'


class EventProcessor:

    def __init__(self, queue: EventQueue, kwargs: dict):
        self._queue = queue
        self._kwargs = kwargs

    def determine_next_action(self, current_time):
        next_action = NextAction.DO_NOTHING
        should_do_break = self._should_do_break(current_time)
        is_doing_break = self._queue.last_event() == PresenceEvent.NOT_PRESENT
        is_not_available = self._queue.last_event() == PresenceEvent.NOT_AVAILABLE
        if should_do_break and not is_doing_break and not is_not_available:
            next_action = NextAction.DO_BREAK
        return next_action

    # Returns True if the user has done any breaks that lasts
    # more than min_break_time_minutes in the last period
    # specified by max_work_time_seconds
    def _should_do_break(self, current_time):
        max_work_time_seconds = self._kwargs['max_work_time_seconds']
        min_break_time_seconds = self._kwargs['min_break_time_seconds']

        if self._queue.first()['at'] > current_time - max_work_time_seconds:
            # it hasn't passed enough time
            return False

        breaks = self._find_all_breaks(
            self._queue.iterate_until(current_time - max_work_time_seconds))
        break_periods = self._calculate_break_periods(breaks)
        has_done_any_breaks = max(break_periods, default=0) >= min_break_time_seconds

        return not has_done_any_breaks

    def _find_all_breaks(self, events):
        print(events)
        breaks = []
        break_start_at = 0
        is_break = False
        for item in events:
            if not is_break and item['event'] == PresenceEvent.NOT_PRESENT:
                is_break = True
                break_start_at = item['at']
            if is_break and item['event'] != PresenceEvent.NOT_PRESENT:
                breaks.append({'start_at': break_start_at, 'end_at': item['at']})
                is_break = False
                break_start_at = 0
        if is_break:
            breaks.append({'start_at': break_start_at, 'end_at': events[-1]['at']})
        print(breaks)
        return breaks

    def _calculate_break_periods(self, breaks):
        period_start = 0
        period_end = 0
        break_periods = []
        for _break in breaks:
            if _break['start_at'] - period_end <= self._queue.time_between_events * 2:
                period_end = _break['end_at']
            else:
                if period_start > 0 and period_end > 0:
                    break_periods.append(period_end - period_start)
                period_start = _break['start_at']
                period_end = _break['end_at']
        if period_start > 0 and period_end > 0:
            break_periods.append(period_end - period_start)
        print(break_periods)
        return break_periods


if __name__ == '__main__':
    queue = EventQueue()
    queue.push(0, PresenceEvent.NOT_PRESENT)
    queue.push(1, PresenceEvent.NOT_AVAILABLE)
    queue.push(2, PresenceEvent.PRESENT)
    queue.push(3, PresenceEvent.PRESENT)
    queue.push(4, PresenceEvent.PRESENT)
    queue.push(5, PresenceEvent.PRESENT)
    queue.push(6, PresenceEvent.PRESENT)
    queue.push(7, PresenceEvent.PRESENT)
    queue.push(8, PresenceEvent.NOT_PRESENT)
    queue.push(9, PresenceEvent.PRESENT)
    event_processor = EventProcessor(queue, {
        'max_work_time_seconds': 6,
        'min_break_time_seconds': 2
    })
    print(event_processor.determine_next_action(10))
