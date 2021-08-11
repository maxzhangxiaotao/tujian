# 爬虫，爬取url，然后下载.


import os
import re
import requests
import time


# 服务器路径

SAVE_SVG_PATH = "/home/zt2021/max/jingsai/final/SVG/"  # 保存SVG路径
SAVE_URL_PATH_ALL = "/home/zt2021/max/jingsai/final/all_url.txt"  # 保存爬取的SVG下载路径、标题等
out_file_line = "/home/zt2021/max/jingsai/final/final.txt"        # 保存提取的SVG文本信息
out_file_line_sel = "/home/zt2021/max/jingsai/final/select.txt"       # 保存筛选后的SVG文本信息
author_path = "/home/zt2021/max/jingsai/final/authors.txt"      # 保存最终的作者列表
final_flie_path = "/home/zt2021/max/jingsai/final/mind_mappings.txt"      # 保存最终的信息列表

# Windows路径

# SAVE_SVG_PATH = "D:\研究生之前的准备工作\竞赛\非OCR爬虫\SVG\\"  # 保存SVG路径
# SAVE_URL_PATH_ALL = "D:\研究生之前的准备工作\竞赛\非OCR爬虫\\all_url.txt"  # 保存爬取的SVG下载路径、标题等
# out_file_line = "D:\研究生之前的准备工作\竞赛\非OCR爬虫\\final.txt"            # 保存提取的SVG文本信息
# out_file_line_sel = "D:\研究生之前的准备工作\竞赛\非OCR爬虫\\select.txt"       # 保存筛选后的SVG文本信息
# author_path = "D:\研究生之前的准备工作\竞赛\数据库对接golang\\authors.txt"      # 保存最终的作者列表
# final_flie_path = "D:\研究生之前的准备工作\竞赛\数据库对接golang\mind_mappings.txt"      # 保存最终的信息列表

# # mac路径
#
# SAVE_SVG_PATH = "/Users/zhangtao/Desktop/竞赛程序/SVG/"  # 保存SVG路径
# SAVE_URL_PATH_ALL = "/Users/zhangtao/Desktop/竞赛程序/all_url.txt"  # 保存爬取的SVG下载路径、标题等
# out_file_line = "/Users/zhangtao/Desktop/竞赛程序/final.txt"        # 保存提取的SVG文本信息
# out_file_line_sel = "/Users/zhangtao/Desktop/竞赛程序/select.txt"       # 保存筛选后的SVG文本信息
# author_path = "/Users/zhangtao/Desktop/竞赛程序/authors.txt"      # 保存最终的作者列表
# final_flie_path = "/Users/zhangtao/Desktop/竞赛程序/mind_mappings.txt"      # 保存最终的信息列表

file_opt = 'a'  # 定义文件操作

begin = 0                                                                 # 爬取网页的起始地址
end = 20                                                               # 爬取网页的最终地址


# 处理网页源代码，依次得到SVG下载链接、网站链接、标题、作者、时间、标签、简介
def find_url():
    # 计数
    count = 0

    # 设置time，爬取400个网页时，休息10s
    time_stop = 80
    time_count = 0

    # 处理源码筛选信息
    str_start = "svg:\"main.svg\""
    str_end = "\"}],pageIndex"

    # 需要爬取的网页链接，例：https://mm.edrawsoft.cn/template/104201/
    url_initial = 'https://mm.edrawsoft.cn/template/'

    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}

    # for循环，加载每一个界面
    for i in range(begin, end):
        # 每一个页面的url
        url = url_initial + str(i) + '/'

        time_count = time_count + 1
        if time_count == time_stop:
            print("\033[1;31m  SLEEP \033[0m")
            time.sleep(20)
            time_count = 0

        # 尝试爬取当前页面，如果当前页面不存在，则抛出异常，继续爬取下一个页面
        try:
            # 解析网页，获取网页源代码


            html = requests.get(url, timeout=1, headers=head).text
            print(str(i) + " is done.")

            # 开始处理爬取的源代码
            # 处理字符串，得到目标下载链接
            string = str(html)

            # 这里try是因为如果爬取到不存在的页面，返回一个错误页面，会导致字符串index失败，进行抛出异常
            try:
                string = string[string.index(str_start):string.index(str_end)]  # 根据关键字，从源码中获取字符串
                string = string[23:]  # 删除多余头部
                string = string.encode('utf-8').decode("unicode_escape")  # 删除字符串中的u002F

                # 加上原来的链接，放在第二列
                string = string + '\t' + url

                # 加上思维导图的标题，用\t分开
                string = string + '\t' + find_title(str(html))

                # 加上思维导图的作者，用\t分开
                string = string + '\t' + find_author(str(html))

                # 加上思维导图的时间，用\t分开
                string = string + '\t' + find_time(str(html))

                # 加上思维导图的tag，用\t分开
                string = string + '\t' + find_tags(str(html))

                # 加上思维导图的简介，用\t分开
                string = string + '\t' + find_intro(str(html))

                # 打印爬取的信息
                print(string)

                count += 1  # 计数而已

                # 用于保存处理后的url
                f = open(SAVE_URL_PATH_ALL, file_opt)
                f.write(string + "\n")
                f.close()

            except Exception as e:  # 如果找不到索引的字符串
                # 打印失败信息，该信息为爬取网页源代码中找不到关键字，打印信息为红色
                print("\033[1;31m substring not found\033[0m")
                # time.sleep(5)

        except requests.exceptions.RequestException as e:  # 该页面不存在，跳过，等待时间为1s
            print(str(i) + " is failure.")

    print(count)  # 打印爬取的个数


# 爬取标题
def find_title(string) -> str:
    # 标题开始标识符
    title_start = "<title>"
    # 标题结束标识符
    title_end = "</title>"

    string = string[string.index(title_start):string.index(title_end)]  # 根据关键字，从源码中获取字符串
    string = string[7:-7]  # 继续截取字符串
    return string


# 爬取作者
def find_author(string) -> str:
    # 标题开始标识符
    author_start = "class=\"author-avatar\"> <!---->"
    # 标题结束标识符
    author_end = "</a></div> <div class=\"comments\">"

    string = string[string.index(author_start):string.index(author_end)]  # 根据关键字，从源码中获取字符串
    string = string[40:]  # 继续截取字符串
    string = string.strip()  # 消除首尾多余空格
    return string


# 爬取开始时间
def find_time(string) -> str:
    # 标题开始标识符
    time_start = "</span> <span>"
    # 标题结束标识符
    time_end = "</span></div></div> <div"

    string = string[string.index(time_start):string.index(time_end)]  # 根据关键字，从源码中获取字符串
    string = string[14:]  # 继续截取字符串
    string = string.strip()  # 消除首尾多余空格
    return string


# 爬取标签，返回标签，标签之间用空格隔开
def find_tags(string) -> str:
    # 标签开始标识符
    tab_start = "ref=\"/community/search/1?tag="

    # 标签结束标识符
    tab_end = "\" class=\"article-tag\">"

    current = ""

    # 找到tag
    while string.find(tab_start) != -1:
        current = current + " " + string[string.find(tab_start) + 29:string.find(tab_end)]
        string = string[string.find(tab_end) + 21:]
    # string = string[string.index(tab_start):string.index(tab_end)]  # 根据关键字，从源码中获取字符串
    string = string[29:]  # 继续截取字符串
    return current


# 爬取简介
def find_intro(string) -> str:
    # 说明开始标识符
    intro_start = "<div class=\"article-description\">"

    # 说明结束标识符
    intro_end = "</div> <div class=\"article-tags\""

    current = ""

    # 找到tag
    while string.find(intro_start) != -1:
        current = current + " " + string[string.find(intro_start) + 33:string.find(intro_end)]
        string = string[string.find(intro_end) + 32:]
    # string = string[string.index(tab_start):string.index(tab_end)]  # 根据关键字，从源码中获取字符串
    string = string[29:]  # 继续截取字符串
    return current



# 从保存的url中下载SVG文件
def download_SVG():
    # 定义空白界面中的指定代码，将其筛选
    error_str = '<Code>NoSuchKey</Code>'

    # 打开保存url的文件
    f_in = open(SAVE_URL_PATH_ALL)
    line = f_in.readline()

    # final out file
    out_file = open(out_file_line, 'a')

    # i是为了文件命名
    i = 0

    # 循环读取文件的每一行
    while line:
        message = line[:-1].split('\t')  # 消除换行符\n
        download_url = message[0]  # 获取url
        # 请求下载的文件

        try:
            f = requests.get(download_url)
    
            # 下载文件，文件名为：数字.svg
            file_name = SAVE_SVG_PATH +"0" + ".svg"
            with open(file_name, "wb") as code:
                code.write(f.content)
    
            # SVG to txt
            if error_str not in str(f.content):
                # SVG to TXT
                result = svg_to_txt(file_name)
    
                out_file.write(line[:-1] + '\t' + str(result) + '\t' + '\n')
    
            # 读取文件的下一行
            line = f_in.readline()
            i += 1
    
            # 打印文件下载信息
            # print("SVG: " + str(i) + " is done.")
            print(download_url)
        except Exception as e:
            # 读取文件的下一行
            line = f_in.readline()
            i += 1
            continue
        
    f_in.close()
    out_file.close()


# 直接SVG文字提取
def svg_to_txt(filename):
    f = open(filename)
    line = f.readline()
    b = ""
    while line:
        b = b + line
        line = f.readline()

    c = re.sub('<[^<]+?>', ' ', b).replace(' ', ' ').strip()
    d = c.split(" ")
    d = [i for i in d if i != '']
    d = [i for i in d if '\n' not in i]
    d = [i for i in d if '\t' not in i]
    d = [i for i in d if len(i) <= 200]
    # print(d)
    return d

# 筛选链接
def sel_url():
    f = open(out_file_line)
    f_out = open(out_file_line_sel, 'a')
    line = f.readline()
    while line:
        message = line.split("\t")
        try:
            if len(message[7]) < 5000:
                f_out.write(line)

            line = f.readline()
        except Exception as e:
            line = f.readline()
            continue
    f.close()
    f_out.close()


# 文本转换，对接数据库
def txt_to_database():
    path = out_file_line_sel
    f = open(path)
    line = f.readline()

    # 转换作者为数字ID，用字典保存
    name_dict = {}  # 字典，用于转换作者ID
    name_dict2 = {}
    i = 1
    while line:
        message = line.split("\t")
        if message[3] not in name_dict:
            name_dict[message[3]] = i
            name_dict2[i] = message[3]
            i = i + 1
        line = f.readline()
    print(name_dict)
    f.close()

    # 保存作者ID
    f_out = open(author_path, 'a')
    for j in range(1, i):
        f_out.write(
            str(j) + "\t" + "2021-08-08" + "\t" + "2021-08-08" + "\t" + "2021-08-08" + "\t" + name_dict2[j] + "\n")

    f_out.close()

    # 逐行处理数据，并保存下来
    i = 1  # 计数，ID自增
    f = open(path, encoding="utf-8")
    f_out = open(final_flie_path, 'a')
    line = f.readline()
    while line:
        message = line[:-1].split("\t")

        # # 处理时间
        # store_time = message[4].replace("年", "-")
        # store_time = store_time.replace("月", "-")
        # store_time = store_time[:-1]
        # opt = store_time.split("-")
        # if int(opt[1])<10:
        #     store_time = opt[0]+'-'+'0'+opt[1]
        # else:
        #     store_time = opt[0] + '-' + opt[1]
        # if int(opt[2])<10:
        #     store_time = store_time + '-' + '0' + opt[2]
        # else:
        #     store_time = store_time + '-' + opt[2]
        store_time = "2021-08-08"

        #         "id"	        "created_at"    	"updated_at"	      "deleted_at"	         "title"	      "introduction"	     "content"	     "rating"	  "url"	          "author_id"
        string = str(i) + "\t" + store_time + "\t" + "2021-08-08" + "\t" + "2021-08-08" + "\t" + message[2] + "\t" + \
                 message[6] + "\t" + message[7] + "\t" + "0" + "\t" + message[1] + "\t" + str(
            name_dict[message[3]]) + "\n"
        i = i + 1
        f_out.write(string)
        line = f.readline()

    f.close()
    f_out.close()
#   <title>
#   </title>
#   class="author-avatar"> <!---->
#   </a></div> <div class="comments">
#   </span> <span>
#   </span></div></div> <div
#   ref="/community/search/1?tag=
#   " class="article-tag">
#   <div class="article-description">
#   </div> <div class="article-tags"
#

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 获取url、标签
    # find_url()


    # 下载图片
    download_SVG()

    # 筛选链接
    sel_url()

    # 文本转换，对接数据库
    txt_to_database()
