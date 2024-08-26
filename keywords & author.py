import numpy as np
import re
import pandas as pd
import nltk
import seaborn as sns
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import os
import openpyxl
from textblob import TextBlob

data = pd.read_csv('./data.csv')

key = data.dropna(axis=0, subset=['Keywords'])['Keywords'].values
author = data.dropna(axis=0, subset=['Author'])['Author'].values

# 预处理
key_tre = []
for text in key:
    text = text.split(';')
    key_list = []
    for keyword in text:
        keyword = keyword.strip()
        keyword = keyword.lower()
        keyword = keyword.replace(',', '')
        key_list.append(keyword)
    text_cv = ";".join(key_list)
    key_tre.append(text_cv)

author_tre = []
for text in author:
    text = text.split(';')
    key_list = []
    for keyword in text:
        keyword = keyword.strip()
        keyword = keyword.lower()
        keyword = keyword.title()
        keyword = keyword.replace(',', '')
        key_list.append(keyword)

    text_cv = ";".join(key_list)
    author_tre.append(text_cv)


def sortDictValue(dict, is_reverse):
    '''
    将字典按照value排序
    :param dict: 待排序的字典
    :param is_reverse: 是否按照倒序排序
    :return s: 符合csv逗号分隔格式的字符串
    '''
    # 对字典的值进行倒序排序,items()将字典的每个键值对转化为一个元组,key输入的是函数,item[1]表示元组的第二个元素,reverse为真表示倒序
    tups = sorted(dict.items(), key=lambda item: item[1], reverse=is_reverse)
    s = ''
    for tup in tups:  # 合并成csv需要的逗号分隔格式
        s = s + tup[0] + ',' + str(tup[1]) + '\n'
    return s



def build_matrix(co_authors_list, is_reverse):
    '''
    根据共同列表,构建共现矩阵(存储到字典中),并将该字典按照权值排序
    :param co_authors_list: 共同列表
    :param is_reverse: 排序是否倒序
    :return node_str: 三元组形式的节点字符串(且符合csv逗号分隔格式)
    :return edge_str: 三元组形式的边字符串(且符合csv逗号分隔格式)
    '''
    node_dict = {}  # 节点字典,包含节点名+节点权值(频数)
    edge_dict = {}  # 边字典,包含起点+目标点+边权值(频数)
    # 第1层循环,遍历整表的每行信息
    for row_authors in co_authors_list:
        row_authors_list = row_authors.split(';') # 依据','分割每行,存储到列表中
        # 第2层循环
        for index, pre_au in enumerate(row_authors_list): # 使用enumerate()以获取遍历次数index
            # 统计单个词出现的频次
            if pre_au not in node_dict:
                node_dict[pre_au] = 1
            else:
                node_dict[pre_au] += 1
            # 若遍历到倒数第一个元素,则无需记录关系,结束循环即可
            if pre_au == row_authors_list[-1]:
                break
            connect_list = row_authors_list[index+1:]
            # 第3层循环,遍历当前行词后面所有的词,以统计两两词出现的频次
            for next_au in connect_list:
                A, B = pre_au, next_au
                # 固定两两词的顺序
                # 仅计算上半个矩阵
                if A == B:
                    continue
                if A > B:
                    A, B = B, A
                key = A+','+B  # 格式化为逗号分隔A,B形式,作为字典的键
                # 若该关系不在字典中,则初始化为1,表示词间的共同出现次数
                if key not in edge_dict:
                    edge_dict[key] = 1
                else:
                    edge_dict[key] += 1
    # 对得到的字典按照value进行排序
    node_str = sortDictValue(node_dict, is_reverse)  # 节点
    edge_str = sortDictValue(edge_dict, is_reverse)   # 边
    return node_str, edge_str


def str2csv(filePath, s, x):
    '''
    将字符串写入到本地csv文件中
    :param filePath: csv文件路径
    :param s: 待写入字符串(逗号分隔格式)
    '''
    if x == 'node':
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write("Label,Weight\r")
            f.write(s)
    else:
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write("Source,Target,Weight\r")
            f.write(s)


def get_relation(edge, node_list):
    Source = []
    Target = []
    Type = []
    Weight = []
    new_node_list = []
    for i in range(len(edge)):
        if edge.iloc[i, 0] in node_list:
            if edge.iloc[i, 1] in node_list:
                Source.append(edge.iloc[i, 0])
                Target.append(edge.iloc[i, 1])
                Type.append('Undirected')
                Weight.append(edge.iloc[i, 2])
                new_node_list.append(edge.iloc[i, 0])
                new_node_list.append(edge.iloc[i, 1])

    new_node_list = list(set(new_node_list))

    relationship = {'Source': Source, 'Target': Target, 'Type': Type, 'Weight': Weight}
    entity = {'id': new_node_list, 'label': new_node_list}
    relationship = pd.DataFrame(relationship)
    entity = pd.DataFrame(entity)

    return entity, relationship

node_str_key, edge_str_key = build_matrix(key_tre, is_reverse=True)
node_str_au, edge_str_au = build_matrix(author_tre, is_reverse=True)

str2csv('./mydata/network/node_key.csv', node_str_key, 'node')
str2csv('./mydata/network/edge_key.csv', edge_str_key, 'edge')
str2csv('./mydata/network/node_au.csv', node_str_au, 'node')
str2csv('./mydata/network/edge_au.csv', edge_str_au, 'edge')

node_key = pd.read_csv('./mydata/network/node_key.csv')
edge_key = pd.read_csv('./mydata/network/edge_key.csv')
node_au = pd.read_csv('./mydata/network/node_au.csv')
edge_au = pd.read_csv('./mydata/network/edge_au.csv')

node_key = node_key[['Label', 'Weight']]
node_list_key = node_key['Label'].values
node_list_key = node_list_key[0:100]

node_au = node_au[['Label', 'Weight']]
node_list_au = node_au['Label'].values
node_list_au = node_list_au[0:150]

entity_key, relationship_key = get_relation(edge_key, node_list_key)
relationship_key.to_csv('./mydata/network/relationship_key.csv', encoding='utf-8', index=False)
entity_key.to_csv('./mydata/network/entity_key.csv', encoding='utf-8', index=False)

entity_au, relationship_au = get_relation(edge_au, node_list_au)
relationship_au.to_csv('./mydata/network/relationship_au.csv', encoding='utf-8', index=False)
entity_au.to_csv('./mydata/network/entity_au.csv', encoding='utf-8', index=False)

data = data[data['Year'] != 2021]

University = []
for text in data['Address'].values:
    if str(text) != 'nan' and ']' in text:
        temp = re.findall(r"](.+?),", text)[0].strip()
        temp = temp.lower()
        temp = temp.title()
        University.append(temp)
    elif str(text) != 'nan' and ']' not in text:
        temp = re.findall(r"(.+?),", text)[0].strip()
        temp = temp.lower()
        temp = temp.title()
        University.append(temp)
    else:
        University.append('NA')

USA = []
England = []
China = []
Germany = []
Canada = []
France = []
Australia = []
Italy = []
Spain = []
South_Korea = []

for text in data['Address'].values:
    if str(text) == 'nan':
        text = 'a'

    text = text.lower()
    if 'usa' in text:
        USA.append(1)
    else:
        USA.append(0)

    if 'england' in text:
        England.append(1)
    else:
        England.append(0)

    if 'china' in text:
        China.append(1)
    else:
        China.append(0)

    if 'germany' in text:
        Germany.append(1)
    else:
        Germany.append(0)

    if 'canada' in text:
        Canada.append(1)
    else:
        Canada.append(0)

    if 'france' in text:
        France.append(1)
    else:
        France.append(0)

    if 'australia' in text:
        Australia.append(1)
    else:
        Australia.append(0)

    if 'italy' in text:
        Italy.append(1)
    else:
        Italy.append(0)

    if 'spain' in text:
        Spain.append(1)
    else:
        Spain.append(0)

    if 'south korea' in text:
        South_Korea.append(1)
    else:
        South_Korea.append(0)

data['University'] = University
data['USA'] = USA
data['England'] = England
data['China'] = China
data['Germany'] = Germany
data['Canada'] = Canada
data['France'] = France
data['Australia'] = Australia
data['Italy'] = Italy
data['Spain'] = Spain
data['South Korea'] = South_Korea

data = data.rename(columns={'Class': 'Category'})
# data.to_csv('data.csv', index=False)


node_au = pd.read_csv('./mydata/network/node_au.csv')
author_hot = node_au.iloc[0:50]
author_hot = author_hot.rename(columns={'Label': 'Author', 'Weight': 'Counts'})
citations = []
for author in author_hot['Author'].values:
    citation = 0
    for i in range(len(data)):
        temp_author = data.iloc[i, 0]
        temp_author = temp_author.strip()
        temp_author = temp_author.lower()
        temp_author = temp_author.replace(',', '')
        if author.lower() in temp_author:
            citation = citation + data.iloc[i, 10]

    citations.append(citation)

author_data = {'Author': author_hot['Author'].values, 'Counts': author_hot['Counts'].values, 'Citations': citations}
author_data = pd.DataFrame(author_data)
author_data.to_csv('./mydata/author data.csv', index=False)

author_data.to_excel('./mydata/author data.xlsx', encoding='utf-8', index=False)


