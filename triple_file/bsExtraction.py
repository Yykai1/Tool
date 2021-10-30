# @Time    : 2021/10/23 17:02
# @Author  : Yinkai Yang
# @FileName: extraction.py
# @Software: PyCharm

import json

from bs4 import BeautifulSoup
import requests

# 设置几个全局参数、
teachers = []  # 用来存放老师的姓名
sex = []
type = []  # 类型
position = []  # 技术职称
mails = []  # 电子邮箱
doc_dis = []  # 博士招生学科
aca_dis = []  # 学硕学科
pro_dis = []  # 专硕类别
# introduction = []  # 用来存放老师的简介
area = []  # 用来存放老师的研究领域
other = []
strings = []
# total = []  # 用来存放拼接后的老师数据

# 主函数
def main():
    list = []
    index = 0
    number = 0
    # 获取包含老师间接的网页列表，放入list数组里面（但是这边只是相关的后缀信息，还需要拼接获得完整的网页信息）
    list = openfile(list)
    # 循环调用抽取页面的重要信息
    for i in list:
        # print('https://dsfc.njupt.edu.cn/dsgl/nocontrol/college/dsfcxq.htm?dsJbxxId='+i)
        # 获得完整的url
        url = 'https://dsfc.njupt.edu.cn/dsgl/nocontrol/college/dsfcxq.htm?dsJbxxId=' + i
        # 开始获取数据
        number = number + 1
        getdata(url, number)
    # print(teachers)
    print(strings)
    parpareforother()
    # 拼接所有老师的数据
    for tea in teachers:
        strsplice(index)
        index = index + 1
    # 写进文件
    writedata()

    # datasplice()
    # writefile()






# 获取data.txt文件里面的数据信息
def openfile(list):
    with open('data_part.txt', 'r', encoding='utf-8') as f:
        list_temp = []
        everyline = f.readlines()

        for line in everyline:
            line = line.rstrip('\n')
            list_temp.append(line)
    return list_temp


# 解析网页，获取数据
def getdata(url, number):
    i = 0
    content = getpage(url)
    # print(content)
    soup = BeautifulSoup(content, 'html.parser')
    # 用soup来获取相关内容

    # 获得老师的信息
    for thing in soup.find_all('span', attrs={'class': 'ml10'}):
        if i == 0:
            print(number)
            teachers.append(thing.get_text())
            print(thing.get_text())
        if i == 1:
            sex.append(thing.get_text())
        if i == 2:
            type.append(thing.get_text())
        if i == 3:
            position.append(thing.get_text())
        if i == 4:
            mails.append(thing.get_text())
        if i == 5:
            doc_dis.append(thing.get_text())
            # print(thing.get_text())
        if i == 6:
            aca_dis.append(thing.get_text())
        if i == 7:
            pro_dis.append(thing.get_text())
            print(thing.get_text())
        i = i + 1
        # print(thing.get_text())


# 使用UA获得网页
def getpage(url):
    # 提供一个可行的用户代理，主要是避免服务器拒绝接入
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'
    }
    page = requests.get(url=url, headers=header)  # 只是响应的结果，我们需要的是响应的内容
    content = page.text  # 获得网页的内容
    # print(html)  # 获得的是网页
    return content  # 返回网页的内容


# 为other数组简单准备一下
def parpareforother():
    with open('prepare.txt', 'r', encoding='utf-8') as f:
        everyline = f.readlines()

        for line in everyline:
            line = line.rstrip('\n')
            other.append(line)


# 一个老师所有数据的拼接
def strsplice(index):
    strings.append(str(teachers[index])+',' + str(other[0]) + ',' + str(sex[index]))
    strings.append(str(teachers[index])+',' + str(other[1]) + ',' + str(type[index]))
    strings.append(str(teachers[index])+',' + str(other[2]) + ',' + str(position[index]))
    strings.append(str(teachers[index])+',' + str(other[3]) + ',' + str(mails[index]))
    strings.append(str(teachers[index])+',' + str(other[4]) + ',' + str(doc_dis[index]))
    strings.append(str(teachers[index])+',' + str(other[5]) + ',' + str(aca_dis[index]))
    strings.append(str(teachers[index])+',' + str(other[6]) + ',' + str(pro_dis[index]))

# 把数据写进txt文件中
def writedata():
    # j = 0
    with open('result_of_part.txt', 'w', encoding='utf-8') as f:
        for i in strings:
            f.write(i)
            f.write('\n')
    f.close()


# 爬虫启动
if __name__ == "__main__":
    main()
