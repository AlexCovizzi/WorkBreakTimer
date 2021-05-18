import logging
import datetime
from app.timed_event_queue import TimedEventQueue
from app.notification_event import NotificationEvent
from app.presence_event import PresenceEvent

log = logging.getLogger(__name__)


class EventProcessor:

    def __init__(self, queue: TimedEventQueue, kwargs: dict):
        self._queue = queue
        self._kwargs = kwargs
        self._last_break_notification_time = 0

    def next_notification(self, current_time):
        next_notification = NotificationEvent.NOTHING

        should_do_break = self._should_do_break(current_time)
        is_doing_break = self._queue.last_event() == PresenceEvent.NOT_PRESENT
        is_not_available = self._queue.last_event() == PresenceEvent.NOT_AVAILABLE
        notify_when_camera_occupied = self._kwargs.get('notify_when_camera_occupied')
        if should_do_break:
            next_notification = NotificationEvent.BREAK
            if is_doing_break:
                next_notification = NotificationEvent.NOTHING
            if is_not_available and not notify_when_camera_occupied:
                next_notification = NotificationEvent.NOTHING

        # do nothing if we already sent a notification and the cooldown
        # time hasn't passed yet
        if next_notification == NotificationEvent.BREAK:
            cooldown = self._kwargs.get('break_notification_cooldown_seconds')
            if current_time - self._last_break_notification_time < cooldown:
                next_notification = NotificationEvent.NOTHING
            else:
                self._last_break_notification_time = current_time

        return next_notification

    # Returns True if the user has done any breaks that lasts
    # more than min_break_time_minutes in the last period
    # specified by max_work_time_seconds
    def _should_do_break(self, current_time):
        max_work_time_seconds = self._kwargs.get('max_work_time_seconds')
        min_break_time_seconds = self._kwargs.get('min_break_time_seconds')

        start_from = current_time - max_work_time_seconds - min_break_time_seconds
        events = self._queue.iterate_from(start_from)
        while len(events) > 0 and events[0]['event'] == PresenceEvent.NOT_PRESENT:
            events.pop(0)

        if len(events) == 0 or events[0]['at'] > current_time - max_work_time_seconds:
            # it hasn't passed enough time
            return False

        breaks = self._find_all_breaks(events)
        break_periods = self._calculate_break_periods(breaks)
        longest_break = max(break_periods, default=0)
        has_done_any_breaks = longest_break >= min_break_time_seconds

        log.debug(
            'Found {} breaks starting from {} and the longest break lasted {} seconds'
            .format(
                len(breaks), datetime.datetime.fromtimestamp(start_from),
                longest_break))

        return not has_done_any_breaks

    def _find_all_breaks(self, events):
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
        return break_periods


if __name__ == '__main__':
    queue = TimedEventQueue()
    queue.push(0, PresenceEvent.NOT_PRESENT)
    queue.push(1, PresenceEvent.NOT_AVAILABLE)
    queue.push(2, PresenceEvent.PRESENT)
    queue.push(3, PresenceEvent.PRESENT)
    queue.push(4, PresenceEvent.PRESENT)
    queue.push(5, PresenceEvent.NOT_PRESENT)
    queue.push(6, PresenceEvent.PRESENT)
    event_processor = EventProcessor(queue, {
        'max_work_time_seconds': 6,
        'min_break_time_seconds': 2
    })
    print(event_processor.next_notification(7))
