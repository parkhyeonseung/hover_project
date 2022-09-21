#!/usr/bin/env python3
# encoding: utf-8

import rospy
from hover_joy.msg import arraymsg
import argparse
import os
import sys
from pathlib import Path
import numpy as np
import torch
import torch.backends.cudnn as cudnn
import platform
import tensorrt as trt
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync

@torch.no_grad()
def run(
        weights='yolov5s.pt',  # model.pt path(s)
        source='0',  # file/dir/URL/glob, 0 for webcam
):
    data=ROOT / 'data/coco128.yaml'  # dataset.yaml path
    imgsz=(320, 320)  # inference size (height, width)
    conf_thres=0.25  # confidence threshold
    iou_thres=0.45  # NMS IOU threshold
    max_det=1000  # maximum detections per image
    #device='cuda:0'
    device=''# cuda device, i.e. 0 or 0,1,2,3 or cpu
    view_img=False # show results
    save_crop=False # save cropped prediction boxes
    classes=None  # filter by class: --class 0, or --class 0 2 3
    agnostic_nms=False  # class-agnostic NMS
    augment=False  # augmented inference
    visualize=False  # visualize features
    line_thickness=3  # bounding box thickness (pixels)
    hide_labels=False  # hide labels
    hide_conf=False  # hide confidences
    half=False  # use FP16 half-precision inference
    dnn=False 
    weights = ROOT / weights
    source = source
    source = str(source)
    webcam = source.isnumeric()
    pub_yolo = rospy.Publisher('yolo',arraymsg,queue_size=1)
    yolo_data = arraymsg()
    counts_no_cup = 0
    # Directories
    # Load model
    print(weights)
    device = select_device(device)
    trt.init_libnvinfer_plugins(None,'')
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    print(imgsz)
    # Dataloader
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
        bs = len(dataset)  # batch_size
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
        bs = 1 
    vid_path, vid_writer = [None] * bs, [None] * bs

    
    # Run inference
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], [0.0, 0.0, 0.0]
    target = input('target : ')
    for path, im, im0s, vid_cap, s in dataset:
        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        pred = model(im, augment=augment, visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        dt[2] += time_sync() - t3

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame',0)

            p = Path(p)  # to Path
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            labels = ''
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                
                for *xyxy, conf, cls in reversed(det):
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                    c = int(cls)  # integer class
                    label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                    labels+=label
                    if counts_no_cup >= 15:
                        # print('no')
                        yolo_data.data = [10.,0.,0.,0.]
                        pub_yolo.publish(yolo_data)
                        counts_no_cup =0
                    else:
                        if target in label:
                            yolo_data.data = xywh
                            pub_yolo.publish(yolo_data)
                            counts_no_cup = 0
                        
                            if save_crop or view_img:  # Add bbox to image
                                c = int(cls)  # integer class
                                label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                                annotator.box_label(xyxy, label, color=colors(c, True))
                    ### cup in if end
                # print(labels)
                if target not in labels:
                    counts_no_cup+=1
                    # print(counts_no_cup)

            im0 = annotator.result()
            if view_img:
                if platform.system() == 'Linux' and p not in windows:
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                cv2.imshow(str(p), im0)
                cv2.waitKey(1) 

def main(weights,source):
    check_requirements(exclude=('tensorboard', 'thop'))
    try:
        run(weights,source)
    except KeyboardInterrupt:
        # print('main')
        raise StopIteration

if __name__ == "__main__":
    rospy.init_node('yolo_detect')
    weights = rospy.get_param('weights','yolov5s.pt')
    source = rospy.get_param('source','0')
    if not rospy.is_shutdown():
        try :
            main(weights,source)
        except KeyboardInterrupt:
            # print('name')
            raise StopIteration
