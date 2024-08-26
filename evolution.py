import numpy as np
import re
import pandas as pd
import nltk
import seaborn as sns
import string
from pyecharts.globals import ThemeType
import pyecharts.options as opts
from pyecharts.charts import ThemeRiver
import time
from datetime import datetime

data = pd.read_csv('./data.csv')
new_data = data[['Author', 'Title', 'Source', 'Keywords', 'Keywords Plus', 'Abstract', 'Citations', 'Year']]

new_data = new_data.dropna(axis=0, subset=['Keywords'])
new_data = new_data[new_data['Year'] > 1990]

def get_key(key):
    key_tre = []
    n = len(key)
    for text in key:
        text = text.split(';')
        for keyword in text:
            keyword = keyword.strip()
            keyword = keyword.lower()
            # key_list.append(keyword)
            key_tre.append(keyword)

    sort_list = []
    key_set = set(key_tre)
    for key in key_set:
        sort_list.append([key, key_tre.count(key)])
    sort_list.sort(key=lambda x: (x[1], x[0]), reverse=True)

    sort_list = pd.DataFrame(sort_list)
    sort_list.columns = ['Keyword', 'Counts']

    return key_tre, sort_list, n

_, key_list_1991, n_1991 = get_key(new_data[(new_data['Year'] > 1990) & (new_data['Year'] <= 1995)]['Keywords'].values)
_, key_list_1996, n_1996 = get_key(new_data[(new_data['Year'] > 1995) & (new_data['Year'] <= 2000)]['Keywords'].values)
_, key_list_2001, n_2001 = get_key(new_data[(new_data['Year'] > 2000) & (new_data['Year'] <= 2005)]['Keywords'].values)
_, key_list_2006, n_2006 = get_key(new_data[(new_data['Year'] > 2005) & (new_data['Year'] <= 2010)]['Keywords'].values)
_, key_list_2011, n_2011 = get_key(new_data[(new_data['Year'] > 2010) & (new_data['Year'] <= 2015)]['Keywords'].values)
_, key_list_2016, n_2016 = get_key(new_data[(new_data['Year'] > 2015) & (new_data['Year'] <= 2020)]['Keywords'].values)

_, key_list, n_all = get_key(new_data[(new_data['Year'] > 1990) & (new_data['Year'] <= 2020)]['Keywords'].values)



len(new_data[(new_data['Year'] > 1990) & (new_data['Year'] <= 1995)]['Keywords'].values)  # 866
len(new_data[(new_data['Year'] > 1995) & (new_data['Year'] <= 2000)]['Keywords'].values)  # 1348
len(new_data[(new_data['Year'] > 2000) & (new_data['Year'] <= 2005)]['Keywords'].values)  # 1849
len(new_data[(new_data['Year'] > 2005) & (new_data['Year'] <= 2010)]['Keywords'].values)  # 2690
len(new_data[(new_data['Year'] > 2010) & (new_data['Year'] <= 2015)]['Keywords'].values)  # 3364
len(new_data[(new_data['Year'] > 2015) & (new_data['Year'] <= 2020)]['Keywords'].values)  # 3870

key_list_study = ['bootstrap', 'long memory', 'forecasting', 'markov chain monte carlo', 'cointegration', 'model selection',
                  'consistency', 'kalman filter', 'nonlinear time series', 'long-range dependence', 'autoregressive process',
                  'autocorrelation', 'garch', 'nonparametric regression', 'bayesian inference']

def get_river(if_count):
    Counts = []
    Year = []
    Keyword = []
    for key in key_list_study:
        Keyword.append(key)

        Year.append(datetime.strptime('1991-01-01', '%Y-%m-%d'))
        if(key in key_list_1991['Keyword'].values):
            if if_count == True:
                Counts.append(key_list_1991[key_list_1991['Keyword'] == key]['Counts'].values[0])
            else:
                Counts.append(key_list_1991[key_list_1991['Keyword'] == key]['Counts'].values[0]/n_1991)
        else:
            Counts.append(0)

        Keyword.append(key)
        Year.append(datetime.strptime('1996-01-01', '%Y-%m-%d'))
        if(key in key_list_1996['Keyword'].values):
            if if_count == True:
                Counts.append(key_list_1996[key_list_1996['Keyword'] == key]['Counts'].values[0])
            else:
                Counts.append(key_list_1996[key_list_1996['Keyword'] == key]['Counts'].values[0]/n_1996)
        else:
            Counts.append(0)

        Keyword.append(key)
        Year.append(datetime.strptime('2001-01-01', '%Y-%m-%d'))
        if(key in key_list_2001['Keyword'].values):
            if if_count == True:
                Counts.append(key_list_2001[key_list_2001['Keyword'] == key]['Counts'].values[0])
            else:
                Counts.append(key_list_2001[key_list_2001['Keyword'] == key]['Counts'].values[0]/n_2001)
        else:
            Counts.append(0)

        Keyword.append(key)
        Year.append(datetime.strptime('2006-01-01', '%Y-%m-%d'))
        if(key in key_list_2006['Keyword'].values):
            if if_count == True:
                Counts.append(key_list_2006[key_list_2006['Keyword'] == key]['Counts'].values[0])
            else:
                Counts.append(key_list_2006[key_list_2006['Keyword'] == key]['Counts'].values[0]/n_2006)
        else:
            Counts.append(0)

        Keyword.append(key)
        Year.append(datetime.strptime('2011-01-01', '%Y-%m-%d'))
        if(key in key_list_2011['Keyword'].values):
            if if_count == True:
                Counts.append(key_list_2011[key_list_2011['Keyword'] == key]['Counts'].values[0])
            else:
                Counts.append(key_list_2011[key_list_2011['Keyword'] == key]['Counts'].values[0]/n_2011)
        else:
            Counts.append(0)

        Keyword.append(key)
        Year.append(datetime.strptime('2016-01-01', '%Y-%m-%d'))
        if(key in key_list_2016['Keyword'].values):
            if if_count == True:
                Counts.append(key_list_2016[key_list_2016['Keyword'] == key]['Counts'].values[0])
            else:
                Counts.append(key_list_2016[key_list_2016['Keyword'] == key]['Counts'].values[0]/n_2016)
        else:
            Counts.append(0)

    river_data = {'Year': Year, 'Counts': Counts, 'Keyword': Keyword}
    river_data = pd.DataFrame(river_data)

    return river_data

river_data_count = get_river(if_count=True)
river_data_pro = get_river(if_count=False)

c_ThemeRiver = (
    ThemeRiver(init_opts=opts.InitOpts(width="1000px", height="600px", theme=ThemeType.DARK))
    .add(
        series_name=list(river_data_count["Keyword"].unique()),
        data=river_data_count.values.tolist(),
        singleaxis_opts=opts.SingleAxisOpts(
            pos_top="50", pos_bottom="50", type_="time"
        ),
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
        title_opts=opts.TitleOpts(title="Trend of Count", pos_bottom="85%", pos_right="20%")
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=0))
    .render("./plot/river1.html")
)
# c_ThemeRiver.render_notebook()

d_ThemeRiver = (
    ThemeRiver(init_opts=opts.InitOpts(width="1000px", height="600px", theme=ThemeType.DARK))
    .add(
        series_name=list(river_data_pro["Keyword"].unique()),
        data=river_data_pro.values.tolist(),
        singleaxis_opts=opts.SingleAxisOpts(
            pos_top="50", pos_bottom="50", type_="time"
        ),
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
        title_opts=opts.TitleOpts(title="Trend of Proportion", pos_bottom="85%", pos_right="20%")
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=0))
    .render("./plot/river2.html")
)
# d_ThemeRiver.render_notebook()

# ThemeType.CHALK
# ThemeType.DARK
# ThemeType.VINTAGE




