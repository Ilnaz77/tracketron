import cv2
import os


class Camera(object):
    def __init__(self, video_name, format=".avi"):
        self.video_name = os.path.join("./videos/", str(video_name) + format)
        assert os.path.isfile(self.video_name), "Video path error"
        self.width = None
        self.height = None

    def __call__(self):
        print("Open video ...")
        try:
            self.cap = cv2.VideoCapture(self.video_name)
        except Exception as e:
            print(e)
            raise
        self.width = int(self.cap.get(3))  # float `width`
        self.height = int(self.cap.get(4))  # float `height`
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        return self.cap

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()