# -*- coding:utf-8 -*-
# @Time    : 2021/11/2 8:42
# @Author  : Yinkai Yang
# @FileName: dblp_extration.py
# @Software: PyCharm
# @Description: 通过收集相关老师的信息，转化为外国姓氏格式，通过url的拼接（以及限制条件）来进入相关作者的界面，最终获得相关老师的论文数量（刚开始先不考虑消歧）

# 存放的是老师以及其论文数量构成的三元组
import requests
from bs4 import BeautifulSoup

# 用来存放老师的信息，尝试着去实现以三元组存放
teacher = []

# 用来存放获取到的链接（如果需要的话可以把这个写进text文件中）
strings = []

# 初步想法是存放三元组
result = []


def main():
    list = []

    # 获得老师的姓名（DBPL中的要求是：名 姓，如Yinkai Yang）
    list = openfile(list)

    # 需要提及的是，我这边数据处理是有一点问题的，主要是url拼接时，空格会导致链接断开，上网搜索了相关信息，将空格替换为%20
    # 我现在的设想是建立一个中文和英文的映射（key-value键值对），最终处理数据是将英文映射为中文
    for i in list:
        url = 'https://dblp.uni-trier.de/search?q=' + i
        # print(url)
        # 获取路径
        geturl(url)
    # 循环处理老师的信息
    getinformation()

    # 三元组形式储存
    writefile()


# 数据处理成strings列表
# 根据url找到相关的href
def geturl(url):
    page = requests.get(url=url)
    content = page.text
    # print(content)
    soup = BeautifulSoup(content, 'html.parser', exclude_encodings='utf-8')

    # # 这边可以增加一个控制条件，只有结果是精准匹配的话才进行以下操作
    # for judge in soup.find_all("div", attrs={'class': 'body hide-body'}):
    #     print(judge)
    #     print('-------------------------------->')
    #     print('-------------------------------->')
    #     print('-------------------------------->')
    #     title = judge.select('p')

    for item in soup.find_all('ul', attrs={'class': 'result-list'}):
        # print(item)
        thing = item.select('a')
        # print(thing)
        # print(thing[0].get('href'))
        strings.append(thing[0].get('href'))


# 利用strings列表里面的数据从相应的链接中获取数据
def getinformation():
    i = 0
    for url in strings:
        j = 0
        page = requests.get(url=url+'.html')
        content = page.text
        # print(content)
        soup = BeautifulSoup(content, 'html.parser')

        # 这一步操作（直接获取数据224）是出现了问题，获得的数据是？？，好难受啊
        # for item in soup.find_all('span', attrs={'id': 'max-record-info'}):
        #     print(item)
        #     print(item.get_text())
        #     result.append(str(teacher[i])+str(',论文数量,')+str(item.get_text()))

        # 论文数量
        for item in soup.find_all('nav', attrs={'class': 'publ'}):
            j = j + 1

        # 测试数据的准确性
        # print(j)
        # print(str(teacher[i])+str(',论文数量,')+str(j))

        # 写进result列表
        result.append(str(teacher[i])+str(',论文数量,')+str(j))
        i = i + 1


# 常用的打开文件的方式，获得需要查找的老师的相关信息，以列表的形式返回
def openfile(list):
    with open('teacher.txt', 'r', encoding='utf-8') as f:
        list_temp = []
        everyline = f.readlines()

        for line in everyline:
            line = line.rstrip('\n')
            # print(line)
            teacher.append(line)
            list_temp.append(line)
    return list_temp


# 写文件的常用方式，不再过多赘述
def writefile():
    with open('paper_number.txt', 'w', encoding='utf-8') as f:
        for i in result:
            f.write(i)
            f.write('\n')
    f.close()


if __name__ == "__main__":
    main()