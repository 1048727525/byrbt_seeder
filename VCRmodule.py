#!/usr/bin/env python
# encoding: utf-8
'''
@author: yidian
@license: (C) Copyright 2013-2019.
@contact: hellosw@bupt.edu.cn
@software: pycharm
@file: VCRmodule.py
@time: 2019/10/8 22:51
@desc:
'''

import cv2 as cv
import os

def prepare_pic(pth):#根据路径读取图片并处理成二值图片
    im = cv.imread(pth)

    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

    kernel = cv.getStructuringElement(cv.MORPH_OPEN, (1, 1))
    bin = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)

    return bin

def compare(pic):
    result=''#保存当前字符匹配结果
    err_points=0#保存当前字符差错像素点数目

    path = './words_model'
    for root, dirs, files in os.walk(path):#遍历所有匹配目标字符
        for file in files:
            tmp=0#当前字符差错像素点数目

            pth = os.path.join(root, file)#组合待比较字符图像路径

            bin = prepare_pic(pth)#变为二值图像

            for i in range(10):#迭代求差错像素累计
                for j in range(8):
                    tmp+=abs(int(pic[i, j])-int(bin[i,j]))

            tmp=tmp/255#计算差异像素点数目

            if(tmp>err_points):#求得最小差错即为最相似字符
                err_points=tmp
                (filename, extension) = os.path.splitext(file)
                result=filename

    return result

def main(pth):
    bin1 = prepare_pic(pth)#处理待比较验证码

    sp = bin1.shape#验证码图像像素尺寸

    #截取一张验证码中的待比较字符并得到最相似字符
    part1 = compare(bin1[15:25, 25:33])
    part2 = compare(bin1[15:25, 43:51])
    part3 = compare(bin1[15:25, 61:69])
    part4 = compare(bin1[15:25, 79:87])
    part5 = compare(bin1[15:25, 97:105])
    part6 = compare(bin1[15:25, 115:123])

    return(part1+part2+part3+part4+part5+part6)

if __name__ == '__main__':
    result=main("./000dd67fbde65ac6343970c2ba3a3131.jpg")#运行示例
    print("匹配结果为：", result)

