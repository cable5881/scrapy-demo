import csv
import random
from tutorial.pyspider_script.myProxy import *


def fetch_movies(tag, pages, proxys):
    # os.chdir(r'/Users/apple888/PycharmProjects/proxy IP/豆瓣电影')
    url = 'https://movie.douban.com/tag/爱情?start={}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}

    # 用csv文件保存数据
    csvFile = open("{}.csv".format(tag), 'a+', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    writer.writerow(('name', 'score', 'peoples', 'date', 'nation', 'actor'))

    for page in range(0, pages):
        url = url.format(tag, page)
        try:
            respones = requests.get(url, headers=headers, proxies=random.choice(proxys))
            while respones.status_code != 200:
                respones = requests.get(url, headers=headers, proxies=random.choice(proxys))
            soup = BeautifulSoup(respones.text, 'lxml')
            movies = soup.find_all(name='div', attrs={'class': 'pl2'})
            for movie in movies:
                movie = BeautifulSoup(str(movie), 'lxml')
                movname = movie.find(name='a')
                # 影片名
                movname = movname.contents[0].replace(' ', '').strip('\n').strip('/').strip('\n')
                movInfo = movie.find(name='p').contents[0].split('/')
                # 上映日期
                date = movInfo[0][0:10]
                # 国家
                nation = movInfo[0][11:-2]
                actor_list = [act.strip(' ').replace('...', '') for act in movInfo[1:-1]]
                # 演员
                actors = '\t'.join(actor_list)
                # 评分
                score = movie.find('span', {'class': 'rating_nums'}).string
                # 评论人数
                peopleNum = movie.find('span', {'class': 'pl'}).string[1:-4]
                writer.writerow((movname, score, peopleNum, date, nation, actors))
        except:
            continue
        print('共有{}页，已爬{}页'.format(pages, page))


start = time.time()
proxyPool = proxypool(50)
fetch_movies('烂片', 100, proxyPool)
end = time.time()
lastT = int(end - start)
print('耗时{}s'.format(lastT))
