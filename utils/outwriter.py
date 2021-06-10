from random import getrandbits
from cv2 import VideoWriter, VideoWriter_fourcc
from datetime import datetime
from pytz import timezone
import os


class Outwrite(object):
    def __init__(self, path_to_output, width, height, fps):
        self.width = width
        self.height = height
        self.path_to_output = path_to_output

        self.fourcc = VideoWriter_fourcc(*"XVID")
        self.fps_to_write = fps
        self.path_to_output_video = self.__create(self.path_to_output)
        print("Исходный ФПС видео: ", self.fps_to_write)
        print("Размер изображения: ", self.width, self.height)
        self.out = VideoWriter(self.path_to_output_video, self.fourcc, self.fps_to_write, (self.width, self.height))

    def __call__(self, frame):
        self.out.write(frame)

    def __create(self, path_to_output):
        time = datetime.now(tz=timezone("Europe/Moscow")).strftime("%Y-%m-%d %H:%M:%S").replace(" ", "_")
        filename = time + "_" + path_to_output + ".avi"
        path = "./result_videos/"

        if not os.path.isdir(path):
            os.mkdir(path)

        while os.path.isfile(os.path.join(path, filename)):
            filename = path_to_output + "_" + time + ".avi"

        return os.path.join(path, filename)

    def release(self):
        self.out.release()
