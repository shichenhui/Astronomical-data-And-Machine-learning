# 通过连通域的方法将图像中心的目标切割出来
import os.path

import cv2
import numpy as np
import matplotlib.pyplot as plt


def cut_img(img_path,output_img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # 找到中心位置的连通域，背景阈值为20
    ret, img_bin = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    img_bin = np.uint8(img_bin)
    connectivity = 8
    output = cv2.connectedComponentsWithStats(img_bin, connectivity, cv2.CV_32S)

    # 3. 找到中心位置所处的连通域的label
    num_labels = output[0]
    labels = output[1]
    stats = output[2]
    center_x = int(img.shape[1] // 2)
    center_y = int(img.shape[0] // 2)
    label_center = labels[center_y, center_x]

    # 4. 画出来每个连通域
    mask = np.zeros_like(img_bin)
    mask[labels==label_center] = 1
    # 将目标用矩形切出来
    # 找到目标的最小外接矩形
    rect = cv2.minAreaRect(np.argwhere(mask==1))
    # 找到目标的四个顶点
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    x1, y1 = box.min(axis=0)
    x2, y2 = box.max(axis=0)
    # 将其变成正方形，中心位置不变
    x_center = (x1 + x2) // 2
    y_center = (y1 + y2) // 2
    length = max(x2 - x1, y2 - y1)
    x1 = x_center - length // 2
    x2 = x_center + length // 2
    y1 = y_center - length // 2
    y2 = y_center + length // 2

    # 周围扩大0.5倍，注意不要超出图像范围
    x1 = max(0, x1 - int((x2 - x1) * 0.3))
    y1 = max(0, y1 - int((y2 - y1) * 0.3))
    x2 = min(img.shape[1], x2 + int((x2 - x1) * 0.3))
    y2 = min(img.shape[0], y2 + int((y2 - y1) * 0.3))

    mask = np.expand_dims(mask, axis=2)

    img_target = img[y1:y2, x1:x2, :]
    cv2.imwrite(output_img_path, img_target)


    # 将mask扩成三维
    # 将
    # 与原图img相乘




    # 画出结果图像进行展示
    # plt.figure(figsize=(10, 10))
    # plt.subplot(221)
    # plt.imshow(img)
    # plt.title('original image')
    # plt.subplot(222)
    # plt.imshow(img_bin)
    # plt.title('binary image')
    # plt.subplot(223)
    # plt.imshow(gray, cmap='gray')
    # plt.title('mask')
    # plt.subplot(224)
    # plt.imshow(img_target)
    # plt.title('target image')
    # plt.show()

if __name__ == '__main__':
    # img_path = 'search_result/img/spec-55859-F5902_sp09-190.jpg'
    # output_img_path = 'search_result/cut_target/587722984_cut.jpg'
    # cut_img(img_path,output_img_path)

    imgs_path = 'search_result/img/'
    output_imgs_path = 'search_result/cut_target/cut_target'  # 双层文件夹是为了方便pytorch读取
    imgs = [os.path.join(imgs_path, img) for img in os.listdir(imgs_path) if img.endswith('.jpg') or img.endswith('.png')]
    for img_path in imgs:
        output_img_path = os.path.join(output_imgs_path, 'cut_'+os.path.basename(img_path))
        cut_img(img_path,output_img_path)
        print(img_path)
        print(output_img_path)
        print('------------------')
