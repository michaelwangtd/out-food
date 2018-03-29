###数据分析-从爬取到可视化###
![https://github.com/michaelwangtd](http://p3yz9xz5w.bkt.clouddn.com/image/blog/google_scholar/001.png)
![https://github.com/michaelwangtd](http://p3yz9xz5w.bkt.clouddn.com/image/blog/google_scholar/002.png)
![https://github.com/michaelwangtd](http://p3yz9xz5w.bkt.clouddn.com/image/blog/google_scholar/003.png)

* 寻找并分析干扰数据
```
H. V. Jagadish

Zhu M-J
Li Gui-Mei
Wolff-Michael Roth

D'Alessandro Angelo

Pearson, R.J.
Turner, J.W.G.
Edwards, Peter P.

Pahnke J枚rg 
L茅vy R
Andr茅s Rodr铆guez-Pose
```

* 验证searchUrl是否有效
```
# 1 名字中间有‘.’ 
H. V. Jagadish
https://scholar.google.com/citations?view_op=search_authors&mauthors=H.+V.+Jagadish&hl=en&oi=ao

# 2 名字中间有‘-’
Wolff-Michael Roth
https://scholar.google.com/citations?view_op=search_authors&mauthors=Wolff-Michael+Roth&hl=en&oi=ao

# 3 名字有‘'’
D'Alessandro Angelo
https://scholar.google.com/citations?view_op=search_authors&mauthors=D%27Alessandro+Angelo&hl=en&oi=ao

# 4 名字中间有‘,’
Agelidis, V.G.
https://scholar.google.com/citations?view_op=search_authors&mauthors=Agelidis,+V.G.&hl=en&oi=ao
# 5 名字中有‘汉字’
无有效url
```

* 生成人名搜索替换规则
```python
"""
' - %27
"""
searchAuthorMiddle = '+'.join(targetName.strip().replace('\'','%27').split(' '))
```

* 爬虫核心步骤
```
"""
1 经分析，利用人名，直接构造searchUrl:
searchUrl = 'https://scholar.google.com/citations?view_op=search_authors&mauthors=Thomas+A.+Moore&hl=zh-CN&oi=ao

2 如果有该人名searchUrl对应搜索列表，获取人名1：搜索到的人名，2：主页url地址
（搜索到的列表按照搜索相似度降序排序，故取第一个人名）
HV Jagadish
citations?user=SKVnHakAAAAJ&hl=en

3 构建该人名对应主页url：personUrl（该url作为爬取数据的主题url）
https://scholar.google.com/citations?user=SKVnHakAAAAJ&hl=en

4 使用request get方式，抓取除TITLE之外其他信息

5 使用request post循环请求方式，获取post返回的所有title的html内容，生成quoteListStr字符串变量，将quoteListStr转变为soup方便后续处理

6 从title列表的soup中提取year年份数据，利用Counter+dict转换为年份权重字典

7 （爬取的主要工作已经完成）
缓存原始数据
（以后统一用json缓存数据）

8 生成csv格式数据
"""
```

* 变量抓取示例：
![https://github.com/michaelwangtd](http://p3yz9xz5w.bkt.clouddn.com/image/blog/google_scholar/004.png)


* 爬取变量记录
```python
1 targetName：H. V. Jagadish
2 urltail：citations?user=SKVnHakAAAAJ&hl=en
3 catched_name：HV Jagadish
4 personUrl：https://scholar.google.com/citations?user=SKVnHakAAAAJ&hl=en

5 name：David Vallenet
6 intro：CEA  - Genoscope - UMR8030
7 tags：bioinformatics  genomics  microbiology  metabolic networks
8 hdx：35
9 idx：46
10 chatTupleList：
[('2006', '100'), ('2007', '207'), ('2008', '369'), ('2009', '445'), ('2010', '553'), ('2011', '692'), ('2012', '715'), ('2013', '852'), ('2014', '842'), ('2015', '862'), ('2016', '803'), ('2017', '819'), ('2018', '176')]

11 year resultList
{'2004': 1, '2008': 4, '2012': 6, '2005': 3, '2016': 3, '2003': 1, '2013': 4, '2017': 8, '2014': 5, '2009': 7, '2015': 3, '2018': 2, '2007': 6, '2002': 1, '2010': 2, '2011': 8, '2006': 7}

```

* <font color='red'>**数据误差：**</font>
    1. **原始人名列表不是很规范，很多人名检索不到，检索率只有50%**
    2. **如需进一步提高数据准确率，需手动检验'target_name'和'name'是否一致（少量数据存在两项不一致）：**<br>target_name：检索列表中原始的人名<br>name：检索到的真实人名<br>![https://github.com/michaelwangtd](http://p3yz9xz5w.bkt.clouddn.com/image/blog/google_scholar/006.png)
    3. **google scholar中也有部分数据造成误差：**<br>![https://github.com/michaelwangtd](http://p3yz9xz5w.bkt.clouddn.com/image/blog/google_scholar/005.png)
* 下载<br>
    1. [原始代码github](https://github.com/michaelwangtd/out-food/tree/master/spiderAcademicStatistics)
    2. [数据](https://pan.baidu.com/s/160_ABEiAShDxVXyLZ1JHvQ)
