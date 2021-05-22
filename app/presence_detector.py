import logging
import time
import cv2
from mtcnn_cv2 import MTCNN
from app.presence_event import PresenceEvent

log = logging.getLogger(__name__)


class PresenceDetector:

    def __init__(self, kwargs: dict):
        self._kwargs = kwargs
        self._face_detector = MTCNN()

    def detect(self) -> PresenceEvent:
        camera = self._kwargs.get('camera')
        video_capture = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
        if not video_capture.isOpened():
            log.info('Unable to open video device {}'.format(camera))
            return PresenceEvent.NOT_AVAILABLE

        frames = self._capture_frames(video_capture)
        video_capture.release()

        start_detect = time.time()
        for image in frames:
            prep_image = self._preprocess_image(image)
            results = self._face_detector.detect_faces(prep_image)
            has_face = len([result['confidence'] > 0.9 for result in results]) > 0
            if has_face:
                log.debug('Face detected in {} seconds: {}'.format(
                    time.time() - start_detect, results))
                return PresenceEvent.PRESENT
        log.debug('No face detected in {} seconds'.format(time.time() - start_detect))
        return PresenceEvent.NOT_PRESENT

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

    def _preprocess_image(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


if __name__ == '__main__':
    """
    presence_detector = PresenceDetector({
        'camera': 0,
        'num_of_snapshots': 3,
        'time_between_snapshots_millis': 200
    })
    while True:
        event, results = presence_detector.detect()
        for result in results:
            src = result['src'].copy()
            detected = result['detected']
            for key, boxes in detected.items():
                for (x, y, w, h) in boxes:
                    cv2.rectangle(src, (x, y), (x + w, y + h), (255, 255, 0), 2)
        cv2.imshow('PresenceDetector[Debug]', src)
        cv2.waitKey(delay=100)
    """
    detector = MTCNN()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = detector.detect_faces(image)
        if len(result) > 0:
            print(result)
            keypoints = result[0]['keypoints']
            bounding_box = result[0]['box']

            cv2.rectangle(
                image, (bounding_box[0], bounding_box[1]),
                (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                (0, 155, 255), 2)

            cv2.circle(image, (keypoints['left_eye']), 2, (0, 155, 255), 2)
            cv2.circle(image, (keypoints['right_eye']), 2, (0, 155, 255), 2)
            cv2.circle(image, (keypoints['nose']), 2, (0, 155, 255), 2)
            cv2.circle(image, (keypoints['mouth_left']), 2, (0, 155, 255), 2)
            cv2.circle(image, (keypoints['mouth_right']), 2, (0, 155, 255), 2)
        cv2.imshow('frame', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        ret = cv2.waitKey(0)
        if ret == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
