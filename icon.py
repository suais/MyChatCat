#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Jinzhong Xu
# @Contact  : jinzhongxu@csu.ac.cn
# @Time     : 2023/4/12 21:41
# @File     : icon.py
# @Software : PyCharm

"""生成应用程序图标"""
import os
from datetime import datetime

def icons(img_path, icon_name, save_path='.'):
    """
    通过Mac自带命令生成Python程序图标
    :param img_path: PNG图像地址
    :param icon_name: 图标名称
    :param save_path: 图标保存路径
    :return: icns 图标
    """
    # 创建临时目录，存放不同大小的中间图像文件
    tmp_iconset = os.path.join(os.path.dirname(img_path), datetime.now().strftime("%Y%m%d.%H%M%S_") + "tmp.iconset")
    os.makedirs(tmp_iconset)
    # 生成不同尺寸的中间图像
    sizes = [2 ** x for x in range(4, 10)]
    for size in sizes:
        tmp_icon_name = f"icon_{size}x{size}.{os.path.splitext(img_path)[-1][1:]}"
        cmd = f"sips -z {size} {size} {img_path} --out {os.path.join(tmp_iconset, tmp_icon_name)}"
        os.system(cmd)
        tmp_icon_name2 = f"icon_{size}x{size}@2x.{os.path.splitext(img_path)[-1][1:]}"
        cmd2 = f"sips -z {size * 2} {size * 2} {img_path} --out {os.path.join(tmp_iconset, tmp_icon_name2)}"
        os.system(cmd2)
    # 把中间图像生成图标文件
    save_icon = icon_name + '.icns'
    cmd_icns = f"iconutil -c icns {tmp_iconset} -o {os.path.join(save_path, save_icon)}"
    os.system(cmd_icns)


if __name__ == "__main__":
    img_path = './icon.png'
    icons(img_path=img_path, icon_name='Icon', save_path='./resources')