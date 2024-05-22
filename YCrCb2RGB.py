import cv2
import torch
from torchvision import transforms
from test import *
args = None

def YCrCb2RGB(input_im):
    im_flat = input_im.transpose(1, 3).transpose(1, 2).reshape(-1, 3)
    mat = torch.tensor(
        [[1.0, 1.0, 1.0], [1.403, -0.714, 0.0], [0.0, -0.344, 1.773]]
    ).cuda()
    bias = torch.tensor([0.0 / 255, -0.5, -0.5]).cuda()
    temp = (im_flat + bias).mm(mat).cuda()
    out = (
        temp.reshape(
            list(input_im.size())[0],
            list(input_im.size())[2],
            list(input_im.size())[3],
            3,
        )
        .transpose(1, 3)
        .transpose(2, 3)
    )
    return out
def RGB2YCrCb(input_im):
    im_flat = input_im.transpose(1, 3).transpose(
        1, 2).reshape(-1, 3)  # (nhw,c)
    R = im_flat[:, 0]
    G = im_flat[:, 1]
    B = im_flat[:, 2]
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    Cr = (R - Y) * 0.713 + 0.5
    Cb = (B - Y) * 0.564 + 0.5
    Y = torch.unsqueeze(Y, 1)
    Cr = torch.unsqueeze(Cr, 1)
    Cb = torch.unsqueeze(Cb, 1)
    temp = torch.cat((Y, Cr, Cb), dim=1).cuda()
    out = (
        temp.reshape(
            list(input_im.size())[0],
            list(input_im.size())[2],
            list(input_im.size())[3],
            3,
        )
        .transpose(1, 3)
        .transpose(2, 3)
    )
    return out
# 加载图片
vis = cv2.imread('test_imgs/Visible/01952.png')
vis = cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)

# 将图片转换为PyTorch tensor格式
tensor_image = transforms.ToTensor()(vis).unsqueeze(0)

# 运行RGB2YCrCb函数进行颜色空间转换
vis = RGB2YCrCb(tensor_image)
#加载图片
ir = cv2.imread('test_imgs/Visible/01952.png')
ir = cv2.cvtColor(ir, cv2.COLOR_BGR2RGB)

# 将图片转换为PyTorch tensor格式
tensor_ir = transforms.ToTensor()(ir).unsqueeze(0)
Fusion_Network_IJ()

# 将转换后的结果转换为图片格式并保存
result_image = transforms.ToPILImage()(result.squeeze(0))
result_image.save('b.png')
