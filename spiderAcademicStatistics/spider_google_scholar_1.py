#!/usr/bin python
# -*- coding:utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
import re
import json
from collections import Counter

def readListFromTxt(filePath):
    infoList = []
    if os.path.exists(filePath):
        f = open(filePath,'r',encoding='utf-8')
        while True:
            line = f.readline()
            if line:
                temp = line.strip()
                infoList.append(temp)
            else:
                break
        f.close()
    return infoList

def washData(string):
    """
        1 去除“<>”内容
        2 去除空格
    """
    if string:
        temp = re.sub('<.*?>',' ',string)
        string = temp.replace('\r','').replace('\n','').replace('\t','')
        return string

def getYearList(spanlistsoup):
    resultList = []
    for spansoup in spanlistsoup:
        resultList.append(spansoup.string.strip())
    return resultList

def getNumList(alistsoup):
    resultList = []
    for asoup in alistsoup:
        if asoup.find('span'):
            resultList.append(asoup.find('span').string.strip())
    return resultList

def getInfoPartOne(soup):
    name = ''
    intro = ''
    tags = ''
    hdx = ''
    idx = ''
    chatTupleList = []

    if soup.find('div',id='gs_bdy').find('div',id='gs_bdy_ccl',role='main'):
        bodysoup = soup.find('div', id='gs_bdy').find('div', id='gs_bdy_ccl', role='main')
        # name,intro,tags
        if bodysoup.find('div',class_='gsc_lcl',role='main',id='gsc_prf_w')\
            .find('div',id='gsc_prf').find('div',id='gsc_prf_i'):
            nameIntroTagsSoup = bodysoup.find('div', class_='gsc_lcl', role='main', id='gsc_prf_w') \
                .find('div', id='gsc_prf').find('div', id='gsc_prf_i')
            if nameIntroTagsSoup.find('div',id='gsc_prf_in'):
                name = nameIntroTagsSoup.find('div', id='gsc_prf_in').string.strip()
            if nameIntroTagsSoup.find('div',class_='gsc_prf_il'):
                introsoup = nameIntroTagsSoup.find('div', class_='gsc_prf_il')
                intro = washData(str(introsoup))
            if nameIntroTagsSoup.find('div',class_='gsc_prf_il',id='gsc_prf_int'):
                tagsoup = nameIntroTagsSoup.find('div', class_='gsc_prf_il', id='gsc_prf_int')
                tags = washData(str(tagsoup))
        # h,i
        if bodysoup.find('div',class_='gsc_rsb',role='navigation').\
            find('div',class_='gsc_rsb_s gsc_prf_pnl',id='gsc_rsb_cit',\
                 role='region').find('table',id='gsc_rsb_st'):
            hisoup = bodysoup.find('div', class_='gsc_rsb', role='navigation'). \
                 find('div', class_='gsc_rsb_s gsc_prf_pnl', id='gsc_rsb_cit', \
                     role='region').find('table', id='gsc_rsb_st').find('tbody')
            if hisoup.find_all('tr') and len(hisoup.find_all('tr'))==3:
                hsoup = hisoup.find_all('tr')[1]
                if hsoup.find_all('td') and len(hsoup.find_all('td'))==3:
                    hdx = hsoup.find_all('td')[1].string.strip()
                isoup = hisoup.find_all('tr')[2]
                if isoup.find_all('td') and len(isoup.find_all('td'))==3:
                    idx = isoup.find_all('td')[1].string.strip()
        # print(hdx,idx)
        # chat
        if bodysoup.find('div', class_='gsc_rsb', role='navigation'). \
                find('div', class_='gsc_rsb_s gsc_prf_pnl', id='gsc_rsb_cit', \
                     role='region').find('div',class_='gsc_g_hist_wrp',dir='rtl').\
                find('div',class_='gsc_md_hist_b'):
            chatsoup = bodysoup.find('div', class_='gsc_rsb', role='navigation'). \
                find('div', class_='gsc_rsb_s gsc_prf_pnl', id='gsc_rsb_cit', \
                     role='region').find('div', class_='gsc_g_hist_wrp', dir='rtl'). \
                find('div', class_='gsc_md_hist_b')
            if chatsoup.find_all('span') and chatsoup.find_all('a'):
                # \ and len(chatsoup.find_all('span'))==len(chatsoup.find_all('a')):
                spanlistsoup = chatsoup.find_all('span')
                yearList = getYearList(spanlistsoup)
                alistsoup = chatsoup.find_all('a')
                numList = getNumList(alistsoup)
                if len(yearList)/2 == len(numList):
                    yearList = yearList[:int(len(yearList)/2)]
                    # print(len(yearList),yearList)
                    # print(len(numList),numList)
                    if len(yearList) == len(numList):
                        chatTupleList = list(zip(yearList,numList))

    return name,intro,tags,hdx,idx,chatTupleList

def getPaperNumMap(quotesoup):
    resultList = []
    if quotesoup.find_all('span',class_='gsc_a_h gsc_a_hc gs_ibl'):
        allspansoup = quotesoup.find_all('span', class_='gsc_a_h gsc_a_hc gs_ibl')
        for spansoup in allspansoup:
            if spansoup.string:
                resultList.append(spansoup.string.strip())
    return dict(Counter(resultList))

if __name__ == '__main__':
    # urlhead = 'https://scholar.google.com.hk'
    urlhead = 'https://scholar.google.com'
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
               'x-chrome-uma-enabled': '1',
               'x-client-data': 'CKi1yQEIhrbJAQijtskBCMG2yQEI+pzKAQipncoB'}

    # fnameList = os.listdir('./data/targetName/')
    fnameList = ['biologyscience.txt']
    outputDir = './data/output'
    for fname in fnameList:
        print('---------file name:',fname)
        fpath = os.path.join('./data/targetName',fname)
        targetNameList = readListFromTxt(fpath)
        # fw = open(os.path.join(outputDir,fname),'aw',encoding='utf-8')

        # print(len(targetNameList))
        # print(targetNameList)
        # searchAuthorLeft = 'https://scholar.google.com.hk/citations?view_op=search_authors&mauthors='
        searchAuthorLeft = 'https://scholar.google.com/citations?view_op=search_authors&mauthors='
        # searchAuthorRight = '&hl=zh-CN&oi=ao'
        searchAuthorRight = '&hl=en&oi=ao'
        for i in range(len(targetNameList)):
            targetName = targetNameList[i]
            print('file name:',fname,i+1,'【'+ targetName +'】')

            searchAuthorMiddle = '+'.join(targetName.strip().replace('\'','%27').split(' '))
            searchUrl = searchAuthorLeft + searchAuthorMiddle + searchAuthorRight
            # searchUrl = 'https://scholar.google.com.hk/citations?view_op=search_authors&mauthors=Antonios+G.+Mikos&hl=zh-CN&oi=ao'
            # searchUrl = 'https://scholar.google.com.hk/citations?view_op=search_authors&mauthors=Craig+B.+Thompson&hl=zh-CN&oi=ao'
            # searchUrl = 'https://scholar.google.com/citations?view_op=search_authors&mauthors=Thomas+A.+Moore&hl=zh-CN&oi=ao'
            # print(searchUrl)

            r = requests.get(url=searchUrl,headers=headers)
            html = r.content.decode('utf-8')
            soup = BeautifulSoup(html,'lxml')
            # print(soup)
            if soup.find('div',id='gs_top').find('div',id='gs_bdy'):
                onesoup = soup.find('div',id='gs_top').find('div',id='gs_bdy')
                if onesoup.find('div',id='gs_bdy_ccl',role='main').find('div',id='gsc_sa_ccl'):
                    twosoup = onesoup.find('div',id='gs_bdy_ccl',role='main').find('div',id='gsc_sa_ccl')
                    if twosoup.find('div',class_='gsc_1usr gs_scl'):
                        threesoup = twosoup.find('div', class_='gsc_1usr gs_scl')
                        # print(threesoup)
                        catched_name = ''
                        if threesoup.find('div',class_='gsc_oai').find('h3',class_='gsc_oai_name').find('a'):
                            urltail = threesoup.find('div', class_='gsc_oai').\
                                find('h3', class_='gsc_oai_name').find('a').get('href')
                        if threesoup.find('div', class_='gsc_oai'). find('h3', class_='gsc_oai_name').find('a').find('span'):
                            catched_name = threesoup.find('div', class_='gsc_oai'). \
                                find('h3', class_='gsc_oai_name').find('a').find('span').string
                            # print(urltail)
                            # print(catched_name)

                            # 获取到person homepage url link（个人主页）
                            personUrl = urlhead + urltail   #https://scholar.google.com/citations?user=wVOesBEAAAAJ&hl=zh-CN
                            print('个人主页：',personUrl)
                            session = requests.Session()

                            # 获取第一部分信息
                            reget = session.get(url=personUrl, headers=headers)
                            html = reget.content.decode('utf-8')
                            soup = BeautifulSoup(html,'lxml')
                            name, intro, tags, hdx, idx, chatTupleList = getInfoPartOne(soup)
                            # print(name,intro,tags,hdx,idx)
                            # print(chatTupleList)

                            # 获取第二部分信息
                            quoteListStr = ''
                            # 初始化数据
                            cstartNum = 0
                            data = {'cstart': cstartNum, 'pagesize': 100, 'json': 1}
                            # url = 'https://scholar.google.com/citations?user=WXQ7lBQAAAAJ&hl=zh-CN&cstart=0&pagesize=100'
                            postUrl = personUrl + '&cstart=' + str(cstartNum) + '&pagesize=100'
                            # print(data)
                            # print(postUrl)
                            # 发送post请求
                            repost = session.post(url=postUrl,data=data,headers=headers)
                            rejson = json.loads(repost.text)
                            while repost.status_code==200 and rejson['B']:
                                quoteitemsoup = rejson['B']
                                # print(quoteitemsoup)
                                quoteListStr = quoteListStr + quoteitemsoup
                                cstartNum = cstartNum + 100
                                data['cstart'] = cstartNum
                                postUrl = personUrl + '&cstart=' + str(cstartNum) + '&pagesize=100'
                                repost = session.post(url=postUrl, data=data, headers=headers)
                                rejson = json.loads(repost.text)
                            quotesoup = BeautifulSoup(quoteListStr)
                            # print(type(quotesoup))
                            # print(quotesoup)
                            paperNumMap = getPaperNumMap(quotesoup)
                            # print(paperNumMap)

                            # final 整合数据
                            # paperNum = ''
                            # for k,v in paperNumMap.items():
                            #     paperNum =  paperNum + str(k) + ':' + str(v) + ' '
                            # chatStr = ''
                            # for chatTuple in chatTupleList:
                            #     chatStr = chatStr + chatTuple[0] + ':' + chatTuple[1] + ' '

                            # outputLine = name.replace(',','，') + ',' + str(personUrl) + ',' + intro.replace(',','，') + ',' \
                            #              + tags.replace(',',',') + ',' + hdx + ',' \
                            #              + idx + ',' + chatStr.strip()\
                            #                 + ',' + paperNum.strip()
                            # print(outputLine)
                            # fw = open(os.path.join(outputDir, fname), 'a', encoding='utf-8')
                            # fw.write(outputLine + '\n')
                            # fw.close()

                            # 为了统一数据格式，这里缓存原始数据
                            div = '#DIV#'
                            outputLine = 'target_name:' + targetName + div +\
                                         'catched_name:' + catched_name + div + \
                                         'person_url:' + personUrl + div + \
                                         'name:' + name + div + \
                                         'intro:' + intro + div + \
                                          'tags:' + tags + div + \
                                         'hdx:' + str(hdx) + div + \
                                         'idx:' + str(idx) + div + \
                                         'chat_tuple_list:' + str(chatTupleList) + div + \
                                         'year_result_list:' + str(paperNumMap) + div
                            print(outputLine)

                            fw = open(os.path.join(outputDir, fname), 'a', encoding='utf-8')
                            fw.write(outputLine + '\n')
                            fw.close()
