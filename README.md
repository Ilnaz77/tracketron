<a name="">Start</a>
Start
------------
```shell
$ conda create --deepsort py38 python=3.8
$ conda activate deepsort
$ pip3 install -r requirements
$ python3 main.py
```

* Есть параметры, которые можно менять в args.py. 
* Есть гиперпаметры, которые можно менять в configs/deep_sort.yaml && configs/yolov3.yaml
* Веса и папку с видео надо будет догрузить.

```shell
$ mv videos/ ./
$ mv ckpt.t7 ./deep_sort/deep/checkpoint
$ mv yolov4.weights ./detector/YOLOv3/weight
```

* Видео в папке переименовать в 0.avi, 1.avi, 2.avi.
