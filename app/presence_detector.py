import logging
import time
import cv2
from app.resources import get_resource_path
from app.presence_event import PresenceEvent

log = logging.getLogger(__name__)

frontal_face_cascade = cv2.CascadeClassifier(
    get_resource_path('haarcascade_frontalface_default.xml'))
profile_face_cascade = cv2.CascadeClassifier(
    get_resource_path('haarcascade_profileface.xml'))


class PresenceDetector:

    def __init__(self, kwargs: dict):
        self._kwargs = kwargs

    def detect(self) -> PresenceEvent:
        camera = self._kwargs.get('camera')
        video_capture = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
        if not video_capture.isOpened():
            log.info('Unable to open video device {}'.format(camera))
            return PresenceEvent.NOT_AVAILABLE, {}
        frames = self._capture_frames(video_capture)
        video_capture.release()

        start_detect = time.time()
        for frame in frames:
            frame = self._preprocess_frame(frame)
            has_face, detect_info = self._detect_face(frame)
            if has_face:
                log.debug('Face detected in {} seconds: {}'.format(
                    time.time() - start_detect, {
                        'type': detect_info['type'],
                        'boxes': detect_info['boxes']
                    }))
                return PresenceEvent.PRESENT, detect_info
        log.debug('No face detected in {} seconds'.format(time.time() - start_detect))
        return PresenceEvent.NOT_PRESENT, {'type': 'none', 'boxes': [], 'img': frame}

    def _capture_frames(self, video_capture):
        start_at = time.time()
        num_of_snapshots = self._kwargs.get('num_of_snapshots')
        time_between_snapshots = self._kwargs.get('time_between_snapshots_millis')
        frames = []
        for i in range(num_of_snapshots):
            retval, frame = video_capture.read()
            if retval:
                frames.append(frame)
            if i < num_of_snapshots - 1:
                time.sleep(time_between_snapshots / 1000)
        duration = time.time() - start_at
        log.debug('Captured {} snapshots in {} seconds'.format(len(frames), duration))
        return frames

    def _preprocess_frame(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def _detect_face(self, frame):
        has_frontal, frontal = self._detect_frontal(frame)
        if has_frontal:
            return True, frontal
        has_profile, profile = self._detect_profile(frame)
        if has_profile:
            return True, profile
        return False, {}

    def _detect_profile(self, frame):
        profile_1 = profile_face_cascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)
        if len(profile_1) > 0:
            return True, {'type': 'profile', 'boxes': profile_1, 'img': frame}

        frame_flipped = cv2.flip(frame, 1)
        profile_2 = profile_face_cascade.detectMultiScale(
            frame_flipped,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)
        if len(profile_2) > 0:
            return True, {'type': 'profile', 'boxes': profile_2, 'img': frame_flipped}

        return False, {'type': 'profile', 'boxes': [], 'img': frame}

    def _detect_frontal(self, frame):
        frontal = frontal_face_cascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)
        return len(frontal) > 0, {'type': 'frontal', 'boxes': frontal, 'img': frame}

    def _debug(self, frame, boxes):
        frame_with_boxes = frame.copy()
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('PresenceDetector[Debug]', frame_with_boxes)
        cv2.waitKey(delay=60)


if __name__ == '__main__':
    args = {'camera': 0}
    presence_detector = PresenceDetector({'camera': 0})
    while True:
        event, info = presence_detector.detect()
        img_with_boxes = info['img'].copy()
        for (x, y, w, h) in info['boxes']:
            cv2.rectangle(img_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('PresenceDetector[Debug]', img_with_boxes)
        cv2.waitKey(delay=60)
