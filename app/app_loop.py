from app.subscribable import Subscribable
import time
import datetime
import schedule
from app.presence_detector import PresenceDetector
from app.timed_queue import TimedQueue
from app.notification_calculator import NotificationCalculator


class AppLoop(Subscribable):

    def __init__(self, config: dict):
        super().__init__()
        self._config = config
        self._is_running = False
        self._scheduler = schedule.Scheduler()
        self._presence_detector = PresenceDetector(self._config)
        self._queue = TimedQueue()
        self._notification_calculator = NotificationCalculator(
            self._queue, self._config)

        self._presence_detection_job = None
        self._next_notification_job = None

        self._check_presence_every_seconds_cached = None
        self._calculate_notification_every_seconds_cached = None

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

    def _is_enabled(self):
        return self._config.get('enabled')

    def _is_in_active_hour(self):
        active_from_hour = self._config.get('activate_from_hour')
        active_until_hour = self._config.get('activate_until_hour')
        local_date_time = time.localtime()
        local_time = datetime.time(local_date_time.tm_hour, local_date_time.tm_min)
        return local_time >= active_from_hour and local_time <= active_until_hour

    def _schedule_presence_detection(self):
        if self._presence_detection_job:
            self._scheduler.cancel_job(self._presence_detection_job)
        seconds = self._config.get('check_presence_every_seconds')
        self._check_presence_every_seconds_cached = seconds
        self._presence_detection_job = self._scheduler.every(seconds).seconds.do(
            self._run_presence_detection)

    def _schedule_next_notification(self):
        if self._next_notification_job:
            self._scheduler.cancel_job(self._next_notification_job)
        seconds = self._config.get('calculate_notification_every_seconds')
        self._calculate_notification_every_seconds_cached = seconds
        self._next_notification_job = self._scheduler.every(seconds).seconds.do(
            self._run_next_notification)

    def _reschedule_if_needed(self):
        if (self._config.get('check_presence_every_seconds') !=
                self._check_presence_every_seconds_cached):
            self._schedule_presence_detection()
        if (self._config.get('calculate_notification_every_seconds') !=
                self._calculate_notification_every_seconds_cached):
            self._schedule_next_notification()

    def _run_presence_detection(self):
        presence_event = self._presence_detector.detect()
        current_time = time.time()
        self._queue.push(current_time, presence_event)

    def _run_next_notification(self):
        current_time = time.time()

        # calculate next notification
        notification = self._notification_calculator.calculate(current_time)
        if notification:
            self.publish('notification', notification)


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
