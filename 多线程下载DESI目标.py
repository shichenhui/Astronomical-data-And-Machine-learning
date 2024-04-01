# 参考https://www.legacysurvey.org/dr9/description/
# https://www.legacysurvey.org/viewer/

import wget
import os
import threading
import concurrent.futures
import pandas as pd
from decimal import Decimal

completed_downloads = set()
lock = threading.Lock()


def download_file(url, save_path):
    if url in completed_downloads:
        # print(f"{url} 已经下载过了，跳过下载。")
        return
    if os.path.exists(save_path):
        # print(f"{save_path} 已经存在，跳过下载。")
        with lock:
            completed_downloads.add(url)
        return
    try:
        # print(f"正在下载 {url}")
        wget.download(url, save_path)
        # print(f"\n{url} 下载完成")
        with lock:
            completed_downloads.add(url)
    except Exception as e:
        print(f"下载 {url} 时出错：{e}")

def convert_to_rgb(fits_path, save_path):
    pass
def main(cord_file_path, save_dir, num_threads=10):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # coordinate = pd.read_csv(cord_file_path)
    # ra = coordinate['ra']
    # dec = coordinate['dec']
    with open(cord_file_path, 'r') as f:
        lines = f.readlines()
    ra = []
    dec = []
    filename = []
    for line in lines:
        line = line.strip('\n')
        temp = line.split(',')
        filename.append(temp[0].split('.')[0] + '.jpg')
        ra.append(temp[1])
        dec.append(temp[2])
    url_all = []
    name_all = []

    for i in range(len(ra)):
        '''这里原来是要根据desi图像的命名规则，四舍五入，后来直接在csv文件里设置一下格式就行了'''
        # temp_ra = Decimal(temp_ra).quantize(Decimal("0.0001"), rounding="ROUND_HALF_UP")
        # temp_dec = Decimal(temp_dec).quantize(Decimal("0.0001"), rounding="ROUND_HALF_UP")
        width = 320
        height = 320
        pixscale = 0.262
        url = ('https://www.legacysurvey.org/viewer/jpeg-cutout?ra=' + str(ra[i]) + '&dec=' + str(dec[i]) +
               '&width=' + str(width) + '&height=' + str(height) + '&layer=ls-dr9&pixscale=' + str(pixscale))
        # name = 'cutout_' + str(ra[i]) + '_' + str(dec[i]) + '.jpg'

        url_all.append(url)
        name_all.append(os.path.join(save_dir, filename[i]))

    # 限制线程数
    max_threads = num_threads

    # 创建ThreadPoolExecutor，并设置线程数
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        # 启动下载任务
        futures = {executor.submit(download_file, url, save_path): url for url, save_path in zip(url_all, name_all)}
        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                future.result()  # 获取下载结果，这里不会有实际的返回值，因此主要是为了捕获异常
                print("下载完成", url)
            except Exception as e:
                print(f"下载 {url} 时出现错误：{e}")
    print("所有下载任务已完成！")


if __name__ == "__main__":
    main(r'D:\shichenhui\others\qucaixia\New\search_result\positive_radec.txt', r'D:\shichenhui\others\qucaixia\New\search_result\img', )
