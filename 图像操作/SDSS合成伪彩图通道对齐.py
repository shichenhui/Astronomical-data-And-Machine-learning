import csv
import cv2
import numpy as np

from PIL import Image

from astropy.wcs import WCS
import bz2
from astropy.io import fits
from astropy.visualization import make_lupton_rgb
import os


class MyData():
    def __init__(self, run, cam, field, ra, dec, fits_path):
        # self.out_path=out_path
        self.run = run
        self.cam = cam
        self.field = field
        self.name_r = fits_path + '/frame-r-%06d-%s-%04d.fits.bz2' % (int(run), int(cam), int(field))
        self.name_g = fits_path + '/frame-g-%06d-%s-%04d.fits.bz2' % (int(run), int(cam), int(field))
        self.name_i = fits_path + '/frame-i-%06d-%s-%04d.fits.bz2' % (int(run), int(cam), int(field))
        self.name_u = fits_path + '/frame-u-%06d-%s-%04d.fits.bz2' % (int(run), int(cam), int(field))
        self.name_z = fits_path + '/frame-z-%06d-%s-%04d.fits.bz2' % (int(run), int(cam), int(field))
        print(self.name_i)
        self.ra = ra
        self.dec = dec

    '''通过赤经赤纬获得像素坐标'''

    def get_pix(self, name=None):
        # print(name)
        W = WCS(name)
        if name == None:
            W = WCS(self.name_r)
        w, h = W.all_world2pix(float(self.ra), float(self.dec), 1)
        return w, h

    '''对齐rgb通道'''

    def get_img(self):
        try:

            hud = fits.open(self.name_r)
            r = hud[0].data
            hud.close()
            hud = fits.open(self.name_g)
            g = hud[0].data
            hud.close()
            # hud = fits.open(self.name_i)
            # hud.close()
            hud = fits.open(self.name_i)
            i = hud[0].data
            hud.close()
            hud = fits.open(self.name_u)
            u = hud[0].data
            hud.close()
            hud = fits.open(self.name_z)
            z = hud[0].data
            hud.close()
            i_new = np.zeros([1489, 2048])
            g_new = np.zeros([1489, 2048])
            u_new = np.zeros([1489, 2048])
            z_new = np.zeros([1489, 2048])
            w_r, h_r = self.get_pix(self.name_r)
            w_g, h_g = self.get_pix(self.name_g)
            w_i, h_i = self.get_pix(self.name_i)
            w_u, h_u = self.get_pix(self.name_u)
            w_z, h_z = self.get_pix(self.name_z)
            gw = int(round(w_r - w_g))
            gh = int(round(h_r - h_g))
            iw = int(round(w_r - w_i))
            ih = int(round(h_r - h_i))
            uw = int(round(w_r - w_u))
            uh = int(round(h_r - h_u))
            zw = int(round(w_r - w_z))
            zh = int(round(h_r - h_z))
        except:
            print('error:not have', self.name_r)
            return None

        # print(w2 - w1, h2 - h1, w2 - w3, h2 - h3)
        try:
            if ih < 0:
                i_new[:ih, :] = i[-ih:, :]
            elif ih > 0:
                i_new[ih:, :] = i[:-ih, :]
            else:
                i_new[:, :] = i[:, :]
            if iw < 0:
                i_new[:, :iw] = i_new[:, -iw:]
            elif iw > 0:
                i_new[:, iw:] = i_new[:, :-iw]
            else:
                i_new[:, :] = i_new[:, :]

            if gh < 0:
                g_new[:gh, :] = g[-gh:, :]
            elif gh > 0:
                g_new[gh:, :] = g[:-gh, :]
            else:
                g_new[:, :] = g[:, :]
            if gw < 0:
                g_new[:, :gw] = g_new[:, -gw:]
            elif gw > 0:
                g_new[:, gw:] = g_new[:, :-gw]
            else:
                g_new[:, :] = g_new[:, :]

            if uh < 0:
                u_new[:uh, :] = u[-uh:, :]
            elif uh > 0:
                u_new[uh:, :] = u[:-uh, :]
            else:
                u_new[:, :] = u[:, :]
            if uw < 0:
                u_new[:, :uw] = u_new[:, -uw:]
            elif uw > 0:
                u_new[:, uw:] = u_new[:, :-uw]
            else:
                u_new[:, :] = u_new[:, :]
            if zh < 0:
                z_new[:zh, :] = z[-zh:, :]
            elif zh > 0:
                z_new[zh:, :] = z[:-zh, :]
            else:
                z_new[:, :] = z[:, :]
            if zw < 0:
                z_new[:, :zw] = z_new[:, -zw:]
            elif zw > 0:
                z_new[:, zw:] = z_new[:, :-zw]
            else:
               z_new[:, :] = z_new[:, :]
            return (g_new, r, i_new,u_new,z_new)
        except:
            print('error:%s,is wrong' % self.name_r)
            return None

    '''获得bmp图像，如果添加路径则保存图像'''

    def get_pic_os(self, out_path=None):
        g_new, r, i_new,_,_ = self.get_img()
        rgb = make_lupton_rgb(g_new, r, i_new, Q=10, stretch=5)

        if out_path:
            if not os.path.exists(out_path + '/image'):
                os.makedirs(out_path + '/image')
            make_lupton_rgb(i_new, r, g_new, Q=10, stretch=5,
                            filename=out_path + '/image/frame-%s-%s-%s.jpg' % (self.run.zfill(6), self.cam, self.field.zfill(4)))
        return rgb
