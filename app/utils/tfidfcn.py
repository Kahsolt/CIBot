from gensim import models,corpora,similarities
#load model & data
import logging,nltk,re,linecache,jieba,jieba.analyse
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CIBot.settings")
django.setup()
import json
from app.models import Answer,Question,User,Keyword

RAW_DATA_PATH = '/home/lusong/PycharmProjects/CIBot_clean/data/raw_data'
MODEL_PATH  = '/home/lusong/PycharmProjects/CIBot_clean/data/tfidf/tfidf_question_webQA.model'
DICT_PATH = '/home/lusong/PycharmProjects/CIBot_clean/data/tfidf/dict_webQA'
CORPUS_PATH = '/home/lusong/PycharmProjects/CIBot_clean/data/tfidf/corpus_webQA.mm'
SIMILARITY_PATH = '/home/lusong/PycharmProjects/CIBot_clean/data/tfidf/Similarity_webQA'

class Myquestions(object):
    def  __init__(self,dirname):
        self.dirname = dirname

    def __iter__(self):
        for line in open(self.dirname,'r',encoding='utf-8'):
            word_list = jieba.lcut(line)
            # print(word_list)
            yield word_list


def train():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    sentences = Myquestions(RAW_DATA_PATH)
    dict = corpora.Dictionary(sentences)
    dict.save(DICT_PATH)
    corpus = [dict.doc2bow(text) for text in sentences]
    corpora.MmCorpus.serialize(CORPUS_PATH, corpus)

    tfidf = models.TfidfModel(corpus, dict, normalize=False)
    tfidf.save(MODEL_PATH)
    tfidf_corpus = tfidf[corpus]
    similarity = similarities.Similarity(SIMILARITY_PATH, tfidf_corpus, num_features=len(dict))
    similarity.save(SIMILARITY_PATH)

def jieba_search(input_content):
    keyword = jieba.analyse.extract_tags(input_content)
    query = keyword[0]
    q = Question.objects.filter(content__contains=query)
    return q

def tfidf_search(raw_input, top = 5):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = models.TfidfModel.load(MODEL_PATH)
    corpus = corpora.MmCorpus(CORPUS_PATH)
    dictionary = corpora.Dictionary.load(DICT_PATH)
    tfidf_corpus = model[corpus]
    similarity = similarities.MatrixSimilarity.load(SIMILARITY_PATH)

    seg_list = ' '.join(jieba.cut(raw_input))
    print(seg_list.split())

    ques_corpus = dictionary.doc2bow(seg_list.split())
    ques_corpus_tfidf = model[ques_corpus]
    similarity.num_best = top
    n_best_ans = similarity[ques_corpus_tfidf]
    res = []

    for items in n_best_ans:
        raw = linecache.getline(RAW_DATA_PATH,items[0]+1).split('%%%%%')
        print(raw)
        res.append(raw[0])

    return res

def main():
    # train()

    while(True):
        print("请输入需要查找相似度的语句")
        ques_raw = input()
        res = tfidf_search(ques_raw)
        print(res)

if __name__ == '__main__':
    main()