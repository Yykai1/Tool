# -*- coding:utf-8 -*-
# @Time    : 2021/10/28 8:35
# @Author  : Yinkai Yang
# @FileName: easy_regex.py
# @Software: PyCharm
# @Description:
import csv
import json
import re


# 数据处理
list = []

def main():
    print('---------------------start---------------------')
    temp = openfile()
    extraction(temp)
    wirtefile()
    print('----------------------end----------------------')



def openfile():
    with open('test.json','r') as f:
        temp = json.load(f)
    return temp


def extraction(temp):
    for catagory in temp:
        for key, value in catagory.items():
            if key == 'introduction':
                pat = re.compile(r'[^(\uff0c|\u3002|\uff1b|,|．|，|；|，|。|；)]*?\u6bd5\u4e1a.[^(\uff0c|\u3002|\uff1b|,|．|，|；|，|。|；)]*?[(\uff0c|\u3002|\uff1b|,|．)]')
                patt = pat.findall(value)
                if len(patt) != 0:
                    for item in range(len(patt)):
                        list_temp = []
                        str = patt[item][2:-1]
                        list_temp.append(catagory['name'])
                        list_temp.append('毕业于')
                        list_temp.append(str)
                        print(list_temp)
                        list.append(list_temp)
                else:
                    continue


def wirtefile():
    with open('test.csv', 'w', encoding='utf-8') as cf:
        writer = csv.writer(cf)
        for row in list:
            writer.writerow(row)


if __name__ == "__main__":
    main()