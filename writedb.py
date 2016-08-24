# -*- coding:utf-8 -*-

import multiprocessing
import re
import urllib
import urllib2
import sys
import sqlite3
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup


__author__ = 'Gai'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0)'
headers = {'User-Agent': user_agent}

store = {}
pages = range(2000, 3000)
p = Pool(multiprocessing.cpu_count())
patternId = re.compile('http://video.fc2.com/en/a/content/(.*?)/')
typeEncode = sys.getfilesystemencoding()

# conn = sqlite3.connect(r'C:\Users\gaieepo\Desktop\mysite\db.sqlite3')
# cur = conn.cursor()

def crawl(page):
    print "start page " + str(page)

    conn = sqlite3.connect(r'C:\Users\gaieepo\Desktop\mysite\db.sqlite3')
    cur = conn.cursor()

    try:
        url = 'http://video.fc2.com/en/a/list.php?page=' + str(page) + '&m=cat_top&sobj_up_mt_code=19'
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        pageCode = response.read().decode('utf-8')
        # .encode('mbcs')
        # .encode(typeEncode)
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print "Connection failed, reason:", e.reason
        return None

    if not pageCode:
        print "Fail to load"

    pageCode = BeautifulSoup(pageCode, 'html.parser')
    columnContent = (pageCode.select('div[id="video_list_1column"]'))[0]
    videos = columnContent.find_all("div", class_="video_list_renew clearfix")

    for video in videos:
        try:
            imgsrc = video.find("img", class_="img").attrs['src']
            # print imgsrc

            durationtag = video.find("span", class_="video_time_renew")
            duration = durationtag.string
            # print duration

            titlelink = video.find("div", class_="video_info_right").h3.a
            title = titlelink.string
            # print title
            videoId = re.findall(patternId, titlelink.attrs['href'])[0]
            # print videoId

            auth = video.find("li", class_="member_icon").string
            # print auth.encode('mbcs')

            comment = video.find("img", class_="icon_comments").parent.a.string
            comment = int(comment)
            # print comment

            star = video.find("li", class_="recommend")
            full_star_count = len(star.find_all("img", class_="icon_star"))
            half_star_count = len(star.find_all("img", class_="icon_star_half"))
            star_count = full_star_count * 1.0 + half_star_count * 0.5
            # print star_count

            if star_count and comment and auth != "Premium":
                # print videoId
                videoInfo = (videoId, title, imgsrc, duration, comment, star_count)
                cur.execute('insert into fc2_video (videoid, title, imgsrc, duration, comment, star) values (?, ?, ?, ?, ?, ?)', videoInfo)
        except:
            pass

    cur.close()
    conn.commit()
    conn.close()

    print "end page " + str(page)


    # for i in range(len(titles)):
    #     if auths[i] != 'Premium' and stars != 0 and comments != '0':
    #         cursor.execute('insert into video (id, title) values ("%s", "%s")' % (ids[i], titles[i]))


    # patternUserName = re.compile('user_name.*?<a.*?>(.*?)</a>', re.S)
    # names = re.findall(patternUserName, pageCode)
    # for name in names:
    #     print name
    #
    # patternUserLink = re.compile('user_name.*?<a.*?href="(.*?)"', re.S)
    # links = re.findall(patternUserLink, pageCode)
    # for link in links:
    #     print link
    # cursor.close()
    # conn.commit()
    # conn.close()

# crawl(1)
p.map(crawl, pages)


# pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</div>(.*?)<div class="stats.*?number">(.*?)</', re.S)
# items = re.findall(pattern, pageCode)
# pageStories = []
# for item in items:
#     haveImg = re.search("img", item[2])
#     if not haveImg:
#         replaceBR = re.compile('<br/>')
#         text = re.sub(replaceBR, "\n", item[1])
#         pageStories.append([item[0].strip(), text.strip(), item[3].strip()])
