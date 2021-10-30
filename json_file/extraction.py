# @Time    : 2021/10/25 8:31
# @Author  : Yinkai Yang
# @FileName: extraction.py
# @Software: PyCharm


import json
from bs4 import BeautifulSoup
import requests

# 设置几个全局参数、
teachers = []  # 用来存放老师的姓名
introduction = []  # 用来存放老师的简介
area = []  # 用来存放老师的研究领域
total = []  # 用来存放拼接后的老师数据

# 主函数
def main():
    list = []
    # 获取包含老师间接的网页列表，放入list数组里面（但是这边只是相关的后缀信息，还需要拼接获得完整的网页信息）
    list = openfile(list)
    # 循环调用抽取页面的重要信息
    for i in list:
        # print('https://dsfc.njupt.edu.cn/dsgl/nocontrol/college/dsfcxq.htm?dsJbxxId='+i)
        # 获得完整的url
        url = 'https://dsfc.njupt.edu.cn/dsgl/nocontrol/college/dsfcxq.htm?dsJbxxId=' + i
        # 开始获取数据
        getdata(url)
    datasplice()
    writefile()


# 获取data.txt文件里面的数据信息
def openfile(list):
    with open('data_of_json.txt', 'r', encoding='utf-8') as f:
        list_temp = []
        everyline = f.readlines()

        for line in everyline:
            line = line.rstrip('\n')
            list_temp.append(line)
    return list_temp


# 解析网页，获取数据
def getdata(url):
    i = 0
    content = getpage(url)
    # print(content)
    soup = BeautifulSoup(content, 'html.parser')
    # 用soup来获取相关内容

    # 获得老师的姓名
    teachers.append(soup.find("td", style="width:130px").get_text())

    # 简单的控制，第一次写进introduction里面，第二次写进area里面
    # print(soup.find('div',attrs={'class': 'mb20 editor-area'}).get_text())
    for thing in soup.find_all('div',attrs={'class': 'mb20 editor-area'}):
        # print('-------------------------------------------------------------------------------------------------------------------------------------------------------->')
        if i==1:
            area.append(thing.get_text())
        if i==0:
            introduction.append(thing.get_text())
        i = i + 1
        # print(thing.get_text())



# 使用UA获得网页
def getpage(url):
    # 提供一个可行的用户代理，主要是避免服务器拒绝接入
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'
    }
    page = requests.get(url=url, headers=header)  # 只是响应的结果，我们需要的是响应的内容
    content = page.text
  # 获得网页的内容
    # print(html)  # 获得的是网页
    return content  # 返回网页的内容

# 数据格式修改
def datasplice():
    i = 0
    # 数据循环拼接，形成json格式的数据
    for item in teachers:
        total.append(
            {
                "name": item,
                "introduction": introduction[i],
                "area": area[i]
            }
        )
        # print(total[i])  # 控制台输出打印
        i = i + 1


# 把数据写进result.json文件中
def writefile():
    with open('result.json', 'w+', encoding='utf-8') as f:
        # json.dump(total, f, ensure_ascii=True)
        json_str = json.dumps(total, indent=4, ensure_ascii=False)  # 这就是为什么json文件中的问题，里面不是GBK
        f.write(json_str)
        f.write('\n')
    f.close()
    # with open('result.json', 'r') as rf:
    #     result = json.load(rf)
    #     print(result)
    # rf.close()

# 爬虫启动
if __name__ == "__main__":
    main()
