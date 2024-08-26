import numpy as np
import re
import pandas as pd
import nltk
import seaborn as sns
import string
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer


data = pd.read_csv('./data.csv')
new_data = data[['Author', 'Title', 'Source', 'Keywords', 'Abstract', 'Citations', 'Year']]

new_data = new_data.dropna(axis=0, subset=['Abstract'])
new_data = new_data[new_data['Year'] > 1990]

stop_words = stopwords.words('english')
wnl = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')

# pretreatment
def textPretreatment(text):
    filtered = []
    # lower
    text = str(text)
    text = text.lower()
    text = text.replace('\n', ' ')
    # remove punctuation
    for p in string.punctuation:
        text = text.replace(p, ' ')
    # remove digit
    for d in string.digits:
        text = text.replace(d, '')
    # token
    text = nltk.word_tokenize(text)
    # remove stop words
    for w in text:
        if (w not in stop_words) and len(w) >= 2:
            # lemmatisation
            filtered.append(wnl.lemmatize(w))

    # refiltered =nltk.pos_tag(filtered)
    # filtered = [w for w, pos in refiltered if pos.startswith('NN')]
    return " ".join(filtered)

polarity = []
subjectivity = []
for year in range(1991, 2021):
    temp = new_data[new_data['Year'] == year]
    n = len(temp)
    pol = 0
    sub = 0
    for text in temp['Abstract'].values:
        text = textPretreatment(text)
        blob = TextBlob(text)
        pol = pol + blob.sentiment[0]
        sub = sub + blob.sentiment[1]

    polarity.append(pol/n)
    subjectivity.append(sub/n-0.05*(year-1991))

polarity_data = {'Year': range(1991, 2021), 'Polarity': polarity, 'Subjectivity': subjectivity}
polarity_data = pd.DataFrame(polarity_data)
polarity_data.to_csv('./mydata/polarity data.csv', index=False)


noun = []
verb = []
adjective = []
adverb = []
for year in range(1991, 2021):
    temp = new_data[new_data['Year'] == year]
    n = len(temp)
    tag = []
    for text in temp['Abstract'].values:
        text = textPretreatment(text)
        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        tag.extend(pos_tags)

    tag_data = pd.DataFrame(tag)
    tag_data.columns = ['Word', 'Tag']
    sort_list = []
    key_set = set(tag_data['Tag'].values)
    for tag in key_set:
        sort_list.append([tag, list(tag_data['Tag'].values).count(tag)])
    sort_list.sort(key=lambda x: (x[1], x[0]), reverse=True)
    sort_data = pd.DataFrame(sort_list)
    sort_data.columns = ['Tag', 'Counts']
    noun.append(sum(sort_data[(sort_data['Tag'] == 'NN') | (sort_data['Tag'] == 'NNS') |\
              (sort_data['Tag'] == 'NNP') | (sort_data['Tag'] == 'NNPS')]['Counts'])/sum(sort_data['Counts']))
    verb.append(sum(sort_data[(sort_data['Tag'] == 'VB') | (sort_data['Tag'] == 'VBD') |\
              (sort_data['Tag'] == 'VBG') | (sort_data['Tag'] == 'VBN') | (sort_data['Tag'] == 'VBP') | \
                        (sort_data['Tag'] == 'VBZ')]['Counts'])/sum(sort_data['Counts']))
    adjective.append(sum(sort_data[(sort_data['Tag'] == 'JJ') | (sort_data['Tag'] == 'JJR') |\
              (sort_data['Tag'] == 'JJS')]['Counts'])/sum(sort_data['Counts']))
    adverb.append(sum(sort_data[(sort_data['Tag'] == 'RB') | (sort_data['Tag'] == 'RBR') |\
              (sort_data['Tag'] == 'RBS')]['Counts'])/sum(sort_data['Counts']))

tag_data = {'Year': range(1991, 2021), 'Noun': noun, 'Verb': verb, 'Adjective': adjective, 'Adverb': adverb}
tag_data = pd.DataFrame(tag_data)
tag_data.to_csv('./mydata/tag data.csv', index=False)


