import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
from photutils.segmentation import detect_threshold
from astropy.convolution import Gaussian2DKernel
from astropy.stats import gaussian_fwhm_to_sigma
from photutils.segmentation import detect_sources, deblend_sources, SourceCatalog, source_properties
import warnings
from astropy.visualization import simple_norm

warnings.filterwarnings("ignore")


def plot_circle(img_rgb, img_w):
    """
    将图像中的物体用椭圆圈出来
    :param img_rgb: 伪彩图
    :param img_w: 单通道图
    :return: 圈出来的
    """
    img_rgb = cv2.imread(img_rgb)[:, :, ::-1]
    # cv2.imshow('w',img_rgb)
    # cv2.waitKey(0)
    hdu = fits.open(img_w)
    data = hdu[0].data
    data = data[::-1, :]
    data = np.array(data)

    # nsigma越大，越能忽略掉小物体
    threshold = detect_threshold(data, nsigma=5.)
    sigma = 3.0 * gaussian_fwhm_to_sigma
    # print(sigma)
    kernal = Gaussian2DKernel(sigma, x_size=5, y_size=5)
    kernal.normalize()
    npixels = 5  # 最小物体的像素数
    # 检测物体
    segm = detect_sources(data, threshold, npixels=5, filter_kernel=kernal, connectivity=4)
    # 将两个连一块被判成一个的物体分割开
    segm_deblend = deblend_sources(data, segm, npixels=npixels, filter_kernel=kernal, nlevels=1,
                                   contrast=0.001)

    # cmap = segm_deblend.make_cmap(seed=123)

    # 用椭圆圈
    cat = source_properties(data, segm)
    a = cat.kron_aperture  # 圈出的椭圆
    # tbl = cat.to_table()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12.5))
    norm = simple_norm(data, 'sqrt')
    ax1.imshow(img_rgb)
    ax1.set_title('Data')
    ax2.imshow(img_rgb, )

    for aperture in a:
        # 里面会有一些None
        print((aperture.a-aperture.b)/(aperture.a+aperture.b))
        if aperture.area > 400:
            aperture.plot(axes=ax2, color='grey', lw=0.6)

        # try:
        #     # 画出椭圆
        #     # if (aperture.a-aperture.b)/(aperture.a+aperture.b)>0.2:
        #     if aperture.area > 400:
        #         aperture.plot(axes=ax2, color='black', lw=0.6)
        #
        #         plt.show()
        # except Exception as e:
        #     print(e)
        #     pass
    # ax2.set_title('Segmentation Image')
    plt.show()


# 要用r波段的，其他波段会有偏差，因为伪彩图十一r波段为基准的
plot_circle(r'D:\shichenhui\GalaxyPair\galaxies_pair\data\img\1237648705133805706.jpg',
            r'D:\shichenhui\GalaxyPair\galaxies_pair\data\img\1237648705133805706-r.fits.bz2', )
