import torch
import PIL.Image as Image
import numpy as np
import os
import cv2

def pooling(mat, ksize, method='max', pad=False):

    m, n = mat.shape[:2]
    ky, kx = ksize

    _ceil = lambda x, y: int(np.ceil(x / float(y)))

    if pad:
        ny = _ceil(m, ky)
        nx = _ceil(n, kx)
        size = (ny * ky, nx * kx) + mat.shape[2:]
        mat_pad = np.full(size, np.nan)
        mat_pad[:m, :n, ...] = mat
    else:
        ny = m // ky
        nx = n // kx
        mat_pad = mat[:ny * ky, :nx * kx, ...]

    new_shape = (ny, ky, nx, kx) + mat.shape[2:]

    if method == 'max':
        result = np.nanmax(mat_pad.reshape(new_shape), axis=(1, 3))
    else:
        result = np.nanmean(mat_pad.reshape(new_shape), axis=(1, 3))

    return result
def calhis(img):
    ret = np.zeros(256, int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            ret[img[i][j]] += 1
    return ret

def sal(his):
    ret = np.zeros(256, int)
    for i in range(256):
        for j in range(256):
            ret[i] += np.abs(j - i) * his[j]
    return ret

def vsm(img):
    his = np.zeros(256, int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            his[img[i][j]] += 1
    saliency_map = np.zeros_like(img, int)
    for i in range(256):
        saliency_map[np.where(img == i)] = sal(his)[i]
    if saliency_map.max() == 0:
        return np.zeros_like(img, int)
    return saliency_map / (saliency_map.max())

###############

#VSM for segmentation
##############
def map_generate2(map1,map2,c =20):
    map1_ = vsm(map1)
    map2_ = vsm(map2)
    w1 = 0.4+ (map1_*1-map2_*0.4)
    w2 = 1-w1
    return w1,w2

