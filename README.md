# Defector3D
__Defector3D is a defect detection system for 3D printing process. People experienced with 3D Printing know that your printer will fail from time to time for no reason at all and if you don't realize it in time, you may get into situations like the following:__

![wrong_print3](https://github.com/musafurkanzenbilci/Defector3D/assets/123447782/f42c3eee-5f14-4d9f-ad19-ac724811177a)
![wrong_print2](https://github.com/musafurkanzenbilci/Defector3D/assets/123447782/f10ab483-60e8-4186-8441-04ec6bb862ce)

## Getting Started

## Building the Defector3D

This part is to show how you can build the same step by step.

### Training Your Model

The first thing needed is a model to detect defects on the print and for a model, you need a dataset.

I found several datasets and decided to go with this [one](https://universe.roboflow.com/biplob004-hdmnz/3d-printer-fail-detection/dataset/4).

Since the dataset is found, it is time to train the model. This project uses YOLOv5 for training because it has a pretty easy-to-use repository and lots of community. The training will progress on a `Jetson Orin Nano Developer Kit 8GB` so this training will be as lightweight as possible.

The YOLOv5 repository is not included in this repository but you can find it in [here](https://github.com/ultralytics/yolov5).

To train the model, first, we needed the dataset to be in the YOLO format and split into train, test, and validation parts. The Roboflow dataset can be downloaded in YOLO format but it was not split so the `dataset_splitter.py` script is created. Basically, it chooses random images and labels from the `train` folder and moves them into the newly created `test` and `val` folders. __NOTE: Back up your dataset folder before testing it.__

After splitting the dataset, you can start the training with the following command in the `yolov5` repo.

```python3
python3 train.py --data ../3d-dataset/data.yaml --name print-defects --batch-size 4 --patience 50
```

**Flags and their meanings**
- `data`: This is to specify the dataset.yaml path. It is required for the training script to understand where to obtain your dataset and other pieces of information about it. You can find the sample yaml files under the `yolov5/data` folder.
- `name`: It is to specify the name of your project. During and after training, results will be saved under a folder with your project name in the `yolov5/runs/train`. It is not mandatory.
- `batch-size`: The number of samples used in one pass through the network. `16` and `8` values are experimented with but rejected by the memory size of Jetson Orin Nano.
- `patience`: To kill the training process early if no improvements are seen in the last specified number of epochs. The default value is 100.

***Default Flags***

These flags are not in the command because their default values are used.
- `weights`: By default, yolov5 uses the `yolov5s` model for training. You can specify the yolo model you want from `yolov5n`, `yolov5m`, `yolov5l`, and `yolov5x`.
- `epochs`: By default, 100 epochs will be run. Since the dataset is not very large, it is enough. Remember to set the `patience` flag if you are planning to use higher numbers of epochs.

In around 4-5 hours, the training process is completed. It can vary based on the dataset, model, and the parameters used.

### Octoprint API

Octoprint is an open-source tool that provides you with the control of consumer 3D printers both over a web interface and an API.

The requirements from the Octoprint for this project are:
- Cancel printing
- Reset print head to a safe space

These can be done via the related endpoints or by sending related GCODES over the Octoprint API. GCODES are common to different 3D Printers and can be understood by them at a lower level.

Example scripts using the API can be found under the `octo_api` folder.

[Full Octoprint API documentation here](https://docs.octoprint.org/en/master/)


### Combining YOLOv5 with Octoprint
