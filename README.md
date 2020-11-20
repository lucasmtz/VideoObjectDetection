# Video Object Detection using YOLOv2 and Seq-NMS 
 
## Introduction

![](img/index.jpg) 

This project is a re-implementation of the project **seq_nms_yolo**([reference](https://github.com/melodiepupu/seq_nms_yolo)) for object detection in videos. It combines **YOLOv2**([reference](https://arxiv.org/abs/1506.02640)) and **seq-nms**([reference](https://arxiv.org/abs/1602.08465)) to realise **real time video detection**.

## Installation 

In a Linux machine with conda installed and access to GPU, execute the commands in the following order:

1. `git clone https://github.com/lucasmtz/VideoObjectDetection.git`
1. `cd VideoObjectDetection/`
1. `conda create -y --prefix ./env python=3.8`
1. `conda activate ./env`
1. `conda install -y -c anaconda cudatoolkit=10.1`
1. `pip install -r requirements.txt`
1. `make`
1. `mv libdarknet.so libdarknet.a env/lib/`
1. `wget https://pjreddie.com/media/files/yolo.weights`
1. `wget https://pjreddie.com/media/files/yolov2-tiny-voc.weights`

Commands 9 and 10 can be executed in different terminals (from the same directory VideoObjectDetection/) for faster download.


## Testing it out
#### Generate input data
The **first thing** needed to do is to copy a video file in the video folder. A video example is included in this repository (`v_BalanceBeam_g18_c01.avi`). 
Then, run the following commands (the example video can be changed to any other video): 
```
cd video
python video2img.py -i v_BalanceBeam_g18_c01.avi
```
This step will generate an **input** folder with the image frames of the selected video and a text file called **pkllist.txt** with the paths for each frame. 
#### Generate predictions
**After having the input data**, the video object detection can be performed. To do this, execute the **yolo_seqnms.py** module from the root directory:
```
cd ..
python yolo_seqnms.py
```
It  will generate two folders inside the video folder called **output_no_seqnms** and **output_seqnms**, with the detections frame a frame. The first do not use any kind of post-processing while **the second uses the Seq-NMS technique**. 
#### Reconstruct the videos
The videos can be reconstructed from the output folders generated with the predictions by running:

```
cd video
python img2video.py -i output_seqnms
python img2video.py -i output_no_seqnms
```
From these commands two video files are created inside de video folder: **output_seqnms.mp4** and **output_no_seqnms.mp4**.

#### Evaluate Seq-NMS method 
The Seq-NMS post-processing can be evaluated by executing the commands:
```
cd video
python compare_nms.py
```
It generates a folder called **SeqNMS_comparison** inside the video folder with images of stacked frames from both methods, without post processing in the left side and with Seq-NMS in the right side.

![](results/SeqNMS_comparison/YoloV2&#32;vs&#32;YoloV2+SeqNMS_0.png) 

##### Notes
1. The **results folder** contains outputs for all methods described above for the video example video.

1. This project was tested in the following environment: 
- **Linux Distribution**: Ubuntu, version: 18.04.4 LTS (Bionic Beaver)
- **GPU**: RTX2080ti
- **Conda version**: 4.8.1
## Reference

This project copies lots of code from [darknet](https://github.com/pjreddie/darknet) , [Seq-NMS](https://github.com/lrghust/Seq-NMS) and  [models](https://github.com/tensorflow/models).