from pymongo import MongoClient
from urllib.request import urlopen
from bs4 import BeautifulSoup

# 运行此文件前应先在MongoDB数据库创建一个新的数据库douban，用来保存爬取的数据
# 连接该数据库
client = MongoClient()
db = client.douban

# 获取HTML页面
html = urlopen("https://book.douban.com/top250?icn=index-book250-all")

# 对获取到的页面进行解析 和 有用信息内容提取
bsObj = BeautifulSoup(html, 'lxml')
div = bsObj.find("div", {"class": "indent"})
rows = div.findAll("table")

for table in rows:
    csvRow = []

    div = table.findAll("div")

    bookname = div[0].get_text().strip().split('\n')[0]
    csvRow.append(bookname)

    ratingNum = div[1].get_text().strip().split('\n')[0]
    csvRow.append(ratingNum)

    commentsNum = div[1].get_text().strip().split('\n')[2].strip()
    csvRow.append(commentsNum)

    book_info = table.find("p", {"class": "pl"}).get_text().strip().split('/')

    price = book_info[-1].strip()
    csvRow.append(price)

    publish_date = book_info[-2].strip()
    csvRow.append(publish_date)

    publisher = book_info[-3].strip()
    csvRow.append(publisher)

    if len(book_info) == 4:
        author = book_info[-4]
    if len(book_info) == 5:
        author = book_info[-5] + '/' + book_info[-4]
    csvRow.append(author)

    book_brief = table.find("span", {"class": "inq"}).get_text().strip()
    csvRow.append(book_brief)

    if len(csvRow) != 0:
        book = {'bookname': csvRow[0],
                'ratingNum': csvRow[1],
                'commentsNum': csvRow[2],
                'price': csvRow[3],
                'publish_date': csvRow[4],
                'publisher': csvRow[5],
                'author': csvRow[6],
                'briefInfo': csvRow[7]
                }
        # print(book)
        # 将提取出的有用信息存入douban数据库
        db.book_top250.insert_one(book)

print("Done!")
