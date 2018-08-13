import json
import requests
import pymongo
from config import *
import multiprocessing
from urllib.parse import urlencode
from requests.exceptions import RequestException

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_page_index(subject, offset):
    baseurl = 'https://www.guokr.com/apis/minisite/article.json?'
    data = {
        'retrieve_type': 'by_channel',
        'channel_key': subject,
        'limit': 20,
        'offset': offset
    }
    url = baseurl + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except RequestException:
        print("请求索引页错误！")
        return None


def get_subjectpage_index(subject, offset):
    baseurl = 'https://www.guokr.com/apis/minisite/article.json?'
    data = {
        'retrieve_type': 'by_subject',
        'subject_key': subject,
        'limit': 20,
        'offset': offset
    }
    url = baseurl + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except RequestException:
        print("请求索引页错误！")
        return None


def parse_title_index(html):
    data = json.loads(html)
    if data and 'result' in data.keys():
        transit = data.get('result', {})
        li = []
        for i in range(20):
            result = transit[i]
            title = result.get('title')
            li.append(title)
        return li
    else:
        return False


def parse_url_index(html):
        data = json.loads(html)
        if data and 'result' in data.keys():
            transit = data.get('result', {})
            li = []
            for i in range(20):
                result = transit[i]
                url = result.get('url')
                li.append(url)
            return li
        else:
            return False


def parse_nickname_index(html):
    data = json.loads(html)
    if data and 'result' in data.keys():
        transit = data.get('result', {})
        li = []
        for i in range(20):
            author = transit[i].get('author', {})
            nickname = author.get('nickname', {})
            li.append(nickname)
        return li
    else:
        return False


def parse_time_index(html):
    data = json.loads(html)
    if data and 'result' in data.keys():
        transit = data.get('result', {})
        li = []
        for i in range(20):
            result = transit[i]
            date_created = result.get('date_created')
            time = date_created.replace('T', ' ')
            time = time[0:16]
            li.append(time)
        return li
    else:
        return False


def find_retrieve(num):
    dict_retrieve = {1: 'hot', 2: 'frontier', 3: 'viewpoint', 4: 'visual',
                     5: 'fact', 6: 'lifestyle', 7: 'grzd', 8: 'by_subject'}
    return dict_retrieve.get(int(num))


def find_subject(num):
    dict_type = {1: 'physics', 2: 'biology', 3: 'environment', 4: 'astronomy',
                 5: 'medicine', 6: 'food', 7: 'forensic', 8: 'sex', 9: 'earth',
                 10: 'psychology', 11: 'chemistry', 12: 'sci', 13: 'math',
                 14: 'diy', 15: 'agronomy', 16: 'engineering', 17: 'electronics',
                 18: 'atmosphere', 19: 'education', 20: 'communication', 21: 'society',
                 22: 'internet', 23: 'aerospace', 24: 'others'}
    return dict_type.get(int(num))


def parse_all_index(html):
    li_url = parse_url_index(html)
    li_title = parse_title_index(html)
    li_nickname = parse_nickname_index(html)
    li_time = parse_time_index(html)
    for i in range(1, 20):
        print(li_title[i], " ", li_url[i], " ",
              li_nickname[i], " ", li_time[i])
        save_to_mongo(li_title[i], li_url[i], li_nickname[i], li_time[i])


def output_select():
    print("1.热点 2.前沿 3.观点 4.视觉 5.谣言粉碎机 6.生活方式 7.果然知道 8.学科")


def output_subject():
    print("1.物理 2.生物 3.环境 4.天文 5.医学 6.食物 7.法证 8.性情 9.地学 10.心理"
          "11.化学 12.科幻 13.数学 14.DIY 15.农学 16.工程 17.电子 18.天气 19.教育"
          "20.传播 21.社会 22.互联网 23.航空航天 24.其他")


def save_to_mongo(title, url, name, time):
    if db[MONGO_TABLE].insert({"title": title,
                               "url": url,
                               "name": name,
                               "time": time}):
        return True
    else:
        return False


def main():
    output_select()
    title_num = input("Please enter the number corresponding to the content：")
    if int(title_num) == 8:
        output_subject()
        subject_num = input("Please enter the number corresponding to the subject:")
    page_num = input("Please enter the number of pages：")

    if int(title_num) == 8:
        subject = find_subject(subject_num)
    else:
        subject = find_retrieve(title_num)

    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    for page in range(int(page_num)):
        print("page：", page+1)
        if int(title_num) == 8:
            html = get_subjectpage_index(subject, (18 + page * 20))
        else:
            html = get_page_index(subject, (18 + page * 20))

        pool.apply_async(parse_all_index(html))
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
