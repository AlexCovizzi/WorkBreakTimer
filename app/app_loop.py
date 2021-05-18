import schedule
import time
import datetime
from app.presence_detector import PresenceDetector
from app.timed_event_queue import TimedEventQueue
from app.event_processor import EventProcessor


class AppLoop:

    def __init__(self, kwargs):
        self._kwargs = kwargs
        self._is_running = False
        self._scheduler = schedule.Scheduler()
        self._presence_detector = PresenceDetector(kwargs)
        self._event_queue = TimedEventQueue()
        self._event_processor = EventProcessor(self._event_queue, kwargs)

        self._on_notification = None
        self._presence_detection_job = None
        self._next_notification_job = None

        self._check_presence_every_seconds_cached = None
        self._calculate_notification_every_seconds_cached = None

    def init(self):
        self._schedule_presence_detection()
        self._schedule_next_notification()

    def stop(self):
        self._is_running = False

    def runloop(self):
        self._is_running = True
        while self._is_running:
            if self._is_enabled() and self._is_in_active_hour():
                self._scheduler.run_pending()
                self._reschedule_if_needed()

            if not self._is_running:
                return
            time.sleep(1)

    def on_notification(self, func):
        self._on_notification = func

    def _is_enabled(self):
        return self._kwargs.get('enabled')

    def _is_in_active_hour(self):
        active_from_hour = self._kwargs.get('activate_from_hour')
        active_until_hour = self._kwargs.get('activate_until_hour')
        local_date_time = time.localtime()
        local_time = datetime.time(local_date_time.tm_hour, local_date_time.tm_min)
        return local_time >= active_from_hour and local_time <= active_until_hour

    def _schedule_presence_detection(self):
        if self._presence_detection_job:
            self._scheduler.cancel_job(self._presence_detection_job)
        seconds = self._kwargs.get('check_presence_every_seconds')
        self._check_presence_every_seconds_cached = seconds
        self._presence_detection_job = self._scheduler.every(seconds).seconds.do(
            self._run_presence_detection)

    def _schedule_next_notification(self):
        if self._next_notification_job:
            self._scheduler.cancel_job(self._next_notification_job)
        seconds = self._kwargs.get('calculate_notification_every_seconds')
        self._calculate_notification_every_seconds_cached = seconds
        self._next_notification_job = self._scheduler.every(seconds).seconds.do(
            self._run_next_notification)

    def _reschedule_if_needed(self):
        if (self._kwargs.get('check_presence_every_seconds') !=
                self._check_presence_every_seconds_cached):
            self._schedule_presence_detection()
        if (self._kwargs.get('calculate_notification_every_seconds') !=
                self._calculate_notification_every_seconds_cached):
            self._schedule_next_notification()

    def _run_presence_detection(self):
        presence_event, _ = self._presence_detector.detect()
        current_time = time.time()
        self._event_queue.push(current_time, presence_event)

    def _run_next_notification(self):
        current_time = time.time()
        # clear old events
        max_work_time_seconds = self._kwargs.get('max_work_time_seconds')
        min_break_time_seconds = self._kwargs.get('min_break_time_seconds')
        self._event_queue.clear_until(current_time - max_work_time_seconds -
                                      min_break_time_seconds)
        # calculate next notification
        notification = self._event_processor.next_notification(current_time)
        if self._on_notification:
            self._on_notification(notification)


if __name__ == '__main__':
    kwargs = {
        'camera': 0,
        'tick_seconds': 2,
        'check_presence_every_seconds': 2,
        'max_work_time_seconds': 10,
        'min_break_time_seconds': 4
    }
    loop = AppLoop(kwargs)
    loop.init()
    try:
        loop.runloop()
    except KeyboardInterrupt:
        pass
