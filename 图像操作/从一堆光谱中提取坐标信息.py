# 通过搜寻得出的光谱文件名，提取出目标的RA和DEC坐标信息
import os
import numpy as np
from astropy.io import fits


def get_radec(spectra_file_name, output_file):
    with open(spectra_file_name, 'r') as f:
        lines = f.readlines()
    radec = []
    for line in lines:
        filename, proba = line.split(',')
        hdulist = fits.open(os.path.join('E:\LAMOST DR10', filename))
        ra = hdulist[0].header['RA']
        dec = hdulist[0].header['DEC']
        radec.append([filename, ra, dec])
    with open(output_file, 'w') as f:
        for line in radec:
            f.write(line[0] + ',' + str(line[1]) + ',' + str(line[2]) + '\n')


if __name__ == '__main__':
    get_radec('search_result/positive_filenames.txt', 'search_result/positive_radec.txt')
