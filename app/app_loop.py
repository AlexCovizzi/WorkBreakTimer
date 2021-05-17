import schedule
import time
from app.presence_detector import PresenceDetector
from app.event_queue import EventQueue
from app.event_processor import EventProcessor


class AppLoop:

    def __init__(self, kwargs):
        self._kwargs = kwargs
        self._is_running = False
        self._scheduler = schedule.Scheduler()
        self._presence_detector = PresenceDetector(kwargs)
        self._event_queue = EventQueue()
        self._event_processor = EventProcessor(self._event_queue, kwargs)

        self._on_next_action = None
        self._presence_detection_job = None
        self._determine_next_action_job = None

    def init(self):
        self._schedule_presence_detection()
        self._schedule_determine_next_action()

    def stop(self):
        self._is_running = False

    def runloop(self):
        self._is_running = True
        while self._is_running:
            self._scheduler.run_pending()
            if not self._is_running:
                return
            time.sleep(1)

    def on_next_action(self, func):
        self._on_next_action = func

    def _schedule_presence_detection(self):
        if not self._presence_detection_job:
            self._scheduler.cancel_job(self._presence_detection_job)
        seconds_between_detect = self._kwargs.get('check_presence_every_seconds')
        self._presence_detection_job = self._scheduler.every(
            seconds_between_detect).seconds.do(self._run_presence_detection)

    def _schedule_determine_next_action(self):
        if not self._determine_next_action_job:
            self._scheduler.cancel_job(self._determine_next_action_job)
        tick_seconds = self._kwargs.get('tick_seconds')
        self._determine_next_action_job = self._scheduler.every(
            tick_seconds).seconds.do(self._run_determine_next_action)

    def _run_presence_detection(self):
        presence_event = self._presence_detector.detect()
        print(presence_event)
        current_time = time.time()
        self._event_queue.push(current_time, presence_event)

    def _run_determine_next_action(self):
        current_time = time.time()
        next_action = self._event_processor.determine_next_action(current_time)
        if self._on_next_action:
            self._on_next_action(next_action)


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
