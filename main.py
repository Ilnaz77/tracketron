from detector import build_detector
from deep_sort import build_tracker
from utils.camera import Camera
from utils.outwriter import Outwrite
from utils.draw import draw_boxes
from utils.parser import YamlParser
from utils.logger import get_logger
from utils.sort import Sort
from args import Args
from time import time
import cv2
import numpy as np


def prepare_to_sort(boxes, confs, classes):
    detect_counts = len(boxes)
    if detect_counts != 0:
        detects = np.zeros((detect_counts, 5))
        for i, (box, conf, cl) in enumerate(zip(boxes, confs, classes)):
            confidence = float(conf / 100)  # [0;1]
            x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
            detects[i, :] = np.array([x1, y1, x2, y2, confidence])
    else:
        detects = np.empty((0, 5))
    return detects


def xywh_to_xyxy(bbox_xywh, width, height):
    x, y, w, h = bbox_xywh
    x1 = max(int(x - w / 2), 0)
    x2 = min(int(x + w / 2), width - 1)
    y1 = max(int(y - h / 2), 0)
    y2 = min(int(y + h / 2), height - 1)
    return x1, y1, x2, y2


class Starter(object):
    def __init__(self, cfg, args):
        self.args = args
        self.logger = get_logger("root")
        self.detector = build_detector(cfg, use_cuda=args.use_cuda)
        if self.args.deepsort:
            self.deepsort = build_tracker(cfg, use_cuda=args.use_cuda)
        else:
            self.sort = Sort(70)

        self.camera = Camera(str(args.video_name))
        self.logger = get_logger("root")

    def window(self):
        if self.args.display_image:
            cv2.namedWindow("tracking", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("tracking", (self.camera.width, self.camera.height))

    def __call__(self):
        cap = self.camera()
        out = Outwrite(str(self.args.video_name), self.camera.width, self.camera.height, self.camera.fps)
        self.window()

        fps = 0.0
        tic = time()

        while cap.isOpened():
            ret, frame_bgr = cap.read()
            if not ret:
                print("Some error... ret is False ... Camera out of reach ... go avoid ...")
                break
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

            bbox_xywh, cls_conf, cls_ids = self.detector(frame_rgb)

            # only person
            bbox_xywh = bbox_xywh[cls_ids == 0]
            cls_conf = cls_conf[cls_ids == 0]
            cls_ids = cls_ids[cls_ids == 0]

            bbox_xyxy = [[*xywh_to_xyxy(box, self.camera.width, self.camera.height)] for box in bbox_xywh]

            if self.args.deepsort:
                outputs = self.deepsort.update(bbox_xywh, cls_conf, frame_rgb)
            else:
                detects = prepare_to_sort(bbox_xyxy, cls_conf, cls_ids)
                outputs = self.sort.update(detects)

            if len(outputs) > 0:
                bbox_xyxy = outputs[:, :4]
                identities = outputs[:, -1]
                frame_bgr = draw_boxes(frame_bgr, bbox_xyxy, identities)
            elif bbox_xywh.shape[0]:
                frame_bgr = draw_boxes(frame_bgr, bbox_xyxy)

            if self.args.display_image:
                cv2.imshow("tracking", frame_bgr)
                cv2.waitKey(1)

            toc = time()
            curr_fps = 1.0 / (toc - tic)
            fps = curr_fps if fps == 0.0 else (fps * 0.95 + curr_fps * 0.05)
            tic = toc

            self.logger.info("fps: {:.03f}, detection numbers: {}, tracking numbers: {}".format(fps, bbox_xywh.shape[0], len(outputs)))

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        out.release()


if __name__ == "__main__":
    args = Args()

    cfg = YamlParser()
    cfg.merge_from_file(args.cfg_detection)
    cfg.merge_from_file(args.cfg_deepsort)

    start = Starter(cfg, args)
    start()
