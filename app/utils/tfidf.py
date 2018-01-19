from gensim import models,corpora,similarities
#load model & data
import logging,nltk,re,linecache,jieba,jieba.analyse
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CIBot.settings")
django.setup()
import json
from app.models import Answer,Question,User,Keyword

def get_uri(input_content,top = 5):
    ques_corpus = dictionary.doc2bow(input_content.split())
    ques_corpus_tfidf = model[ques_corpus]
    similarity.num_best = top
    n_best_ans = similarity[ques_corpus_tfidf]
    res = []

    for items in n_best_ans:
        raw = linecache.getline('F:\\full_subject_id.txt',items[0]+1).split('%%%%%')
        print(raw)
        res.append(raw[0])

    return res

class Myquestions(object):
    def  __init__(self,dirname):
        self.dirname = dirname

    def __iter__(self):
        for line in open(self.dirname,'r',encoding='utf-8'):
            sentence_stop = [i for i in line.lower().split() if i not in set(nltk.corpus.stopwords.words('english'))
                             and not re.search('%%%%%',i)]
            yield sentence_stop

def tfidf_model():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    sentences = Myquestions('/home/lusong/PycharmProjects/CIBot_clean/data/raw_data')
    dict = corpora.Dictionary(sentences)
    dict.save('dict_tfidf_stop')
    corpus = [dict.doc2bow(text) for text in sentences]
    corpora.MmCorpus.serialize('corpus_stop.mm', corpus)

    tfidf = models.TfidfModel(corpus, dict, normalize=False)
    tfidf.save('tfidf_question_stop.model')

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = models.TfidfModel.load('tfidf_question_stop.model')
corpus = corpora.MmCorpus('corpus_stop.mm')
dictionary = corpora.Dictionary.load('dict_tfidf_stop')
tfidf_corpus = model[corpus]

# similarity = similarities.Similarity('Similarity-tfidf-stop-index',tfidf_corpus,num_features=len(dictionary))
# similarity = similarities.MatrixSimilarity(tfidf_corpus)
# similarity.save('Similarity-tfidf-stop-index')
similarity = similarities.MatrixSimilarity.load('Similarity-tfidf-stop-index')
while(True):
    print("请输入需要查找相似度的语句")
    ques_raw=input()
    uri_list = get_uri(ques_raw)
    print(uri_list)



    # ques_corpus = dictionary.doc2bow(ques_raw.split())
    # similarity.num_best = 5
    #
    # ques_corpus_tfidf = model[ques_corpus]
    #
    # print("查找结果如下：")
    # n_best_ans = similarity[ques_corpus_tfidf]
    # for items in n_best_ans:
    #     print('问题编号：',items[0],'相似度：',items[1])
    #     print(linecache.getline('F:\\full_subject_id.txt',items[0]+1))

# def main():
    # bot = QaBot()
    # bot.DEBUG = True
    # bot.conf['qr'] = 'tty'  # use terminal instead of 'png'
    # bot.run()


# if __name__ == '__main__':
#     main()