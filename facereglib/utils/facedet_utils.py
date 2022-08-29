import numpy as np
import cv2 
import tensorflow as tf

def xywh_to_tlbr(boxes, y_first=False):
    final_boxes = boxes.copy()
    if not y_first:
        final_boxes[:, 0:2] = np.clip(boxes[:, 0:2] - (boxes[:, 2:4]/2), 0, None)
        final_boxes[:, 2:4] = boxes[:, 0:2] + (boxes[:, 2:4]/2)
    else:
        final_boxes[:, 0:2] = np.clip(boxes[:, [1,0]] - (boxes[:, [3,2]]/2), 0, None)
        final_boxes[:, 2:4] = boxes[:, [1,0]] + (boxes[:, [3,2]]/2)
    return final_boxes
    

def create_letterbox_image(frame, dim):
    h, w = frame.shape[0:2]
    scale = min(dim / h, dim / w)
    nh, nw = int(scale * h), int(scale * w)
    resized = cv2.resize(frame, (nw, nh))
    new_image = np.zeros((dim, dim, 3), np.uint8) 
    new_image.fill(256)
    dx = (dim - nw) // 2
    dy = (dim - nh) // 2
    new_image[dy:dy + nh, dx:dx + nw, :] = resized
    return new_image


def convert_to_orig_points(results, orig_dim, letter_dim):
    if results.ndim == 1: 
        np.expand_dims(results, 0)

    inter_scale = min(letter_dim / orig_dim[0], letter_dim / orig_dim[1])
    inter_h, inter_w = int(inter_scale * orig_dim[0]), int(inter_scale * orig_dim[1])
    offset_x, offset_y = (letter_dim - inter_w)/2.0/letter_dim, (letter_dim - inter_h)/2.0/letter_dim
    scale_x, scale_y = letter_dim / inter_w, letter_dim / inter_h
    results[:, 0:2] = (results[:, 0:2] - [offset_x, offset_y]) * [scale_x, scale_y]
    results[:, 2:4] =  results[:, 2:4] * [scale_x, scale_y]
    results[:, 4:16:2] = (results[:, 4:16:2] - offset_x) * scale_x
    results[:, 5:17:2] = (results[:, 5:17:2] - offset_y) * scale_y

    # Converting from 0-1 range to (orign_dim) range
    results[:, 0:16:2] *= orig_dim[1]
    results[:, 1:17:2] *= orig_dim[0]
    
    return results.astype(np.int32)

def process_detections(results, orig_dim, max_boxes=5, score_threshold=0.75, iou_threshold=0.5, pad_ratio=0.5):
    box_tlbr = xywh_to_tlbr(results[:, 0:4], y_first=True)
    out_boxes = tf.image.non_max_suppression(box_tlbr, results[:, -1], max_boxes,
                                             score_threshold=score_threshold, iou_threshold=iou_threshold)
    filter_boxes = results[out_boxes.numpy(), :-1]
    orig_points = convert_to_orig_points(filter_boxes, orig_dim, 128)
    landmarks_xywh = orig_points.copy()
    landmarks_xywh[:, 2:4] += (landmarks_xywh[:, 2:4] * pad_ratio).astype(np.int32)
    landmarks_xywh[:, 1:2] -= (landmarks_xywh[:, 3:4] * 0.08).astype(np.int32)
    final_boxes = xywh_to_tlbr(orig_points).astype(np.int32)
    return final_boxes, landmarks_xywh


def get_keypoints(landmarks):
    return [dict({
        'left_eye': (landmark[6], landmark[7]),
        'right_eye': (landmark[4], landmark[5]),
        'nose': (landmark[8], landmark[9]),
        'mouth': (landmark[10], landmark[11])
    }) for landmark in landmarks]