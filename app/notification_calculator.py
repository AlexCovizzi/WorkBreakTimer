from typing import Optional
import logging
import datetime
from app.timed_queue import TimedQueue
from app.notification import BreakNotification, Notification
from app.presence_detector import DetectionResult

log = logging.getLogger(__name__)


class NotificationCalculator:

    def __init__(self, queue: TimedQueue, config: dict):
        self._queue = queue
        self._config = config
        self._last_break_notification_time = 0

    def calculate(self, current_time: int) -> Optional[Notification]:
        next_notification = None

        should_do_break = self._should_do_break(current_time)
        is_doing_break = self._queue.last_event() == DetectionResult.NOT_PRESENT
        is_not_available = self._queue.last_event() == DetectionResult.NOT_AVAILABLE
        notify_when_camera_occupied = self._config.get('notify_when_camera_occupied')
        if should_do_break:
            next_notification = BreakNotification()
            if is_doing_break:
                next_notification = None
            if is_not_available and not notify_when_camera_occupied:
                next_notification = None

        # do nothing if we already sent a notification and the cooldown
        # time hasn't passed yet
        if next_notification == BreakNotification():
            cooldown = self._config.get('break_notification_cooldown_seconds')
            if current_time - self._last_break_notification_time < cooldown:
                next_notification = None
            else:
                self._last_break_notification_time = current_time

        return next_notification

    # Returns True if the user has done any breaks that lasts
    # more than min_break_time_minutes in the last period
    # specified by max_work_time_seconds
    def _should_do_break(self, current_time):
        max_work_time_seconds = self._config.get('max_work_time_seconds')
        min_break_time_seconds = self._config.get('min_break_time_seconds')

        start_from = current_time - max_work_time_seconds - min_break_time_seconds
        events = self._queue.iterate_from(start_from)

        if len(events) == 0:
            log.debug('No events yet')
            return False

        if events[0]['at'] > start_from + min_break_time_seconds:
            log.debug('Oldest event at {} is more recent than {}'.format(
                datetime.datetime.fromtimestamp(events[0]['at']),
                datetime.datetime.fromtimestamp(start_from)))
            return False

        breaks = self._find_all_breaks(events)
        break_periods = [br['end_at'] - br['start_at'] for br in breaks]
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
            if not is_break and item['item'] == DetectionResult.NOT_PRESENT:
                is_break = True
                break_start_at = item['at']
            if is_break and item['item'] != DetectionResult.NOT_PRESENT:
                breaks.append({'start_at': break_start_at, 'end_at': item['at']})
                is_break = False
                break_start_at = 0
        if is_break:
            breaks.append({'start_at': break_start_at, 'end_at': events[-1]['at']})
        return breaks


if __name__ == '__main__':
    queue = TimedQueue()
    queue.push(0, DetectionResult.NOT_PRESENT)
    queue.push(1, DetectionResult.NOT_AVAILABLE)
    queue.push(2, DetectionResult.PRESENT)
    queue.push(3, DetectionResult.PRESENT)
    queue.push(4, DetectionResult.PRESENT)
    queue.push(5, DetectionResult.NOT_PRESENT)
    queue.push(6, DetectionResult.PRESENT)
    event_processor = NotificationCalculator(queue, {
        'max_work_time_seconds': 6,
        'min_break_time_seconds': 2
    })
    print(
        event_processor._calculate_break_periods([{
            'start_at': 10,
            'end_at': 20
        }, {
            'start_at': 23,
            'end_at': 30
        }, {
            'start_at': 33,
            'end_at': 33
        }]))
