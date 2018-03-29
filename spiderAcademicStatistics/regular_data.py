#!/usr/bin python
# -*- coding:utf-8 -*-

import os

def get_key_from_tuple(tuple_list):
    year,count = zip(*tuple_list)
    return list(year)

def get_key_from_dic(publishDic):
    temp = list(publishDic.keys())
    # for item in temp:
        # if len(item) < 4:
        #     print(temp)
        #     exit(0)
    return list(publishDic.keys())

def get_ordered_right_key(alist):
    rst = []
    alist = list(set(alist))
    for item in alist:
        if len(item) == 4:
            rst.append(item)
    return sorted(list(set(rst)))

def generate_num_str(key_list,dic):
    rst = ''
    for key in key_list:
        if key in dic:
            rst += str(dic[key]) + ','
        else:
            rst += ','
    rst = rst[:-1]
    return rst

if __name__ == '__main__':
    # fname = 'biologyscience.txt'
    # fname = 'economics.txt'
    fname = 'energyandfuels.txt'

    input_dir = './data/output'
    in_fpath = os.path.join(input_dir,fname)
    fr = open(in_fpath,'r',encoding='utf-8')

    info_list = []
    while True:
        line = fr.readline()
        if line:
            line_list = line.strip().split('#DIV#')[:-1]
            info_list.append(line_list)
        else:
            break
    fr.close()
    print('数据总数：',len(info_list))

    citation_key = []
    publish_key = []

    for line_list in info_list:
        # print(line_list)
        if 'chat_tuple_list' in line_list[-2]:
            citationStr = line_list[-2]
            citationTupleList = eval(citationStr.split(':')[-1])
            if citationTupleList:
                citation_key.extend(get_key_from_tuple(citationTupleList))

        if 'year_result_list' in line_list[-1]:
            publishStr = line_list[-1]
            publishStr = publishStr[17:]
            publishDic = eval(publishStr)
            if publishDic:
                publish_key.extend(get_key_from_dic(publishDic))
    citation_key = get_ordered_right_key(citation_key)
    publish_key = get_ordered_right_key(publish_key)
    print('引用年份：',len(citation_key),citation_key)
    print('发表年份：',len(publish_key),publish_key)

    out_dir = './data/final'
    outpath = os.path.join(out_dir,fname)
    fw = open(outpath,'w',encoding='utf-8')

    tags = 'target_name,catched_name,name,homepage,org,keywords,h_idx,i_idx,'
    tags += 'publish,'*len(publish_key)
    tags += 'citation,'*len(citation_key)
    tags = tags[:-1] + '\n'
    tags += ',,,,,,,,'
    tags += ','.join(publish_key) + ','
    tags += ','.join(citation_key)
    tags += '\n'
    fw.write(tags)

    for line_list in info_list:
        target_name = ''
        catched_name = ''
        name = ''
        homepage = ''
        org = ''
        keywords = ''
        h_idx = ''
        i_idx = ''
        publish_str = ','*(len(publish_key)-1)
        citation_str = ','*(len(citation_key)-1)
        for temp in line_list:
            if 'target_name'in temp:
                target_name = temp.split(':')[-1]
            if 'catched_name'in temp:
                catched_name = temp.split(':')[-1]
            if 'name'in temp:
                name = temp.split(':')[-1]
            if 'person_url'in temp:
                homepage = temp[11:]
            if 'intro'in temp:
                org = temp[6:].strip()
            if 'tags'in temp:
                keywords = temp[5:].strip()
            if 'hdx'in temp:
                h_idx = temp[4:].strip()
            if 'idx'in temp:
                i_idx = temp[4:].strip()
            if 'year_result_list'in temp:
                publishStr = temp[17:]
                publishDic = eval(publishStr)
                if publishDic:
                    publish_str = generate_num_str(publish_key,publishDic)
            if 'chat_tuple_list'in temp:
                citationTupleList = eval(temp.split(':')[-1])
                if citationTupleList:
                    r1,r2 = zip(*citationTupleList)
                    citationDic = dict(zip(r1,r2))
                    citation_str = generate_num_str(citation_key,citationDic)
        outline = target_name.replace(',','，') + ',' + catched_name.replace(',','，') + ',' + name.replace(',','，') +  ',' + homepage.replace(',','，') + \
                ',' + org.replace(',',' ') + ',' + keywords.replace(',','，') + ',' + h_idx.replace(',','，') + ',' + i_idx.replace(',','，') + ',' + \
                publish_str + ',' + citation_str +'\n'
        print(outline)
        fw.write(outline)
    fw.close()








