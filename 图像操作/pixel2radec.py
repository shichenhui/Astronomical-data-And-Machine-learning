"""
    time: 2023/8/12
    function: 利用jpg伪彩图和r波段fits图，将像素坐标转换为赤经赤伟
"""

from astropy.io import fits
import numpy as np
from astropy.wcs import WCS
import json

class Pixel2RaDec:
    """
        jpg_path: 伪彩图路径
        fits_path: r波段fits图路径
    """

    def __init__(self, jpg_path=None, fits_path=None):

        self.jpg_path = jpg_path
        self.fits_path = fits_path
        self.W = WCS(fits_path)

    def pixel2radec(self, x, y):
        ra, dec = self.W.all_pix2world(float(x), float(y), 1)
        return float(ra), float(dec)

if __name__ == '__main__':
    jpg_path = r'D:\shichenhui\GalaxyPair\galaxies_pair\data\img\1237648702968299615.jpg'
    fits_path = r'D:\shichenhui\GalaxyPair\galaxies_pair\data\img\1237648702968299615-r.fits.bz2'
    header = fits.open(fits_path)[0].header
    # 保存成json
    header_json = {}
    for key in header.keys():
        if key != 'COMMENT' and key != 'HISTORY':
            header_json[key] = header[key]
    print(header_json)
    with open('header.json', 'w') as f:
        json.dump(header_json, f)

    p2r = Pixel2RaDec(jpg_path, fits_path)

    print(p2r.pixel2radec(400, 100))
