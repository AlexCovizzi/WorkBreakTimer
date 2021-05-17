import logging
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
            return PresenceEvent.MAYBE_PRESENT
        frame = self._capture_frames(video_capture)
        video_capture.release()
        frame = self._preprocess_frame(frame)
        has_face = self._detect_face(frame)
        return PresenceEvent.PRESENT if has_face else PresenceEvent.NOT_PRESENT

    def _capture_frames(self, video_capture):
        retval, frame = video_capture.read()
        return frame

    def _preprocess_frame(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def _detect_face(self, frame):
        has_face = self._detect_frontal(frame)
        return has_face

    def _detect_frontal(self, frame):
        frontal_faces = frontal_face_cascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)
        return len(frontal_faces) > 0

    def _debug(self, frame, boxes):
        frame_with_boxes = frame.copy()
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('PresenceDetector[Debug]', frame_with_boxes)
        cv2.waitKey()


if __name__ == '__main__':
    presence_detector = PresenceDetector({'camera': 0})
    while True:
        event = presence_detector.detect()
        print(event)

        c = input('Repeat? (q to exit)')
        if c == 'q':
            break
