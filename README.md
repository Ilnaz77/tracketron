<a name="">Start</a>
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

<a name="">Ссылки</a>
------------
* Видео: https://drive.google.com/file/d/1ofvCBPVglLBigeoBvGSjKUlX2iqWRaGz/view?usp=sharing
* Веса DeepSort: https://drive.google.com/file/d/11_tw4jj7YtNUCsgwim0Oo-VC3wF4r5jL/view?usp=sharing
* Веса YoloV3: https://drive.google.com/file/d/1cfUKbBtm4IWIsRXedUCfyIai_eP6R-7y/view?usp=sharing
