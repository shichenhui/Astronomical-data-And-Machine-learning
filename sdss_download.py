import os
import sys
import requests
import numpy as np
import pandas as pd


proxies = {
  "http": "http://127.0.0.1:10809",
  "https": "http://127.0.0.1:10809",
}
def download_cut_img(ra, dec, scale=0.2, width=128, height=128, filename='cutout.jpg'):
    header = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
    }
    # https://skyserver.sdss.org/dr18/SkyServerWS/ImgCutout/zgetjpeg?TaskName=SkyServer.Chart.List&ra=198.87867&dec=8.5984359&scale=0.15&width=120&height=120&opt=
    url = 'https://skyserver.sdss.org/dr18/SkyServerWS/ImgCutout/getjpeg?TaskName=SkyServer.Chart.List&ra={}&dec={}&scale={}&width={}&height={}&opt='.format(ra, dec, scale, width, height)
    if os.path.exists(filename):
        print('file exists:', filename)
        return filename

    # get请求返回图片
    r = requests.get(url, headers=header, proxies=proxies, timeout=50)
    # 保存图片
    with open(filename, 'wb') as f:
        f.write(r.content)
    return filename

def download_spec(plateid, mjd, fiberid, filename):
    header = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
    }
    # http://dr17.sdss.org/optical/spectrum/view/data/format=fits/spec=lite?plateid=4055&mjd=55359&fiberid=596
    if os.path.exists(filename):
        print('file exists:', filename)
        return filename

    url = 'http://dr17.sdss.org/optical/spectrum/view/data/format=fits/spec=lite?plateid={}&mjd={}&fiberid={}'.format(plateid,
                                                                                                                mjd,
                                                                                                                fiberid)
    # 超时时间设置为20s
    r = requests.get(url, headers=header, proxies=proxies, timeout=50)
    # spec-4055-55359-0596.fits
    # filename = os.path.join(folder, r.headers['Content-Disposition'].split('=')[-1])
    with open(filename, 'wb') as f:
        f.write(r.content)
    return filename

if __name__=='__main__':


    img_folder = 'img'
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)
    spec_folder = 'spec'
    if not os.path.exists(spec_folder):
        os.mkdir(spec_folder)

    table = pd.read_csv('E:\data\sdss_image\confirm_true_pairs\sdss_galaxy_spectra.csv', dtype=str)
    # for i, row in table.iterrows()[:4000]:
    # 遍历前4000行
    for i, row in table.iterrows():
        print(i)
        file = row['bestObjID']
        img_filename = os.path.join(img_folder, file+'.jpg')
        spec_filename = os.path.join(spec_folder, file+'.fits')
        try:
            download_cut_img(row['ra'], row['dec'], filename=img_filename)
        except Exception as e:
            print(e)
            print('error:', img_filename)
        try:
            download_spec(row['plate'], row['mjd'], row['fiberid'], filename=spec_filename)
        except Exception as e:
            print(e)
            print('error:', spec_filename)
    # download_cut_img(198.87867, 8.5984359, filename='cutout.jpg')
    # download_spec(4055, 55359, 596, filename='xx.fits')