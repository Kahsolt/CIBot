from gensim import corpora,models
import logging,nltk,re

class Myquestions(object):
    def  __init__(self,dirname):
        self.dirname = dirname

    def __iter__(self):
        for line in open(self.dirname,'r',encoding='utf-8'):
            sentence_stop = [i for i in line.lower().split() if i not in stoplist and not re.search('%%%%%',i)]
            yield sentence_stop

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

stoplist = set(nltk.corpus.stopwords.words('english'))
sentences = Myquestions('F:\\full_subject_id.txt')
dict = corpora.Dictionary(sentences)
dict.save('dict_tfidf_stop')
corpus = [dict.doc2bow(text) for text in sentences]
corpora.MmCorpus.serialize('corpus_stop.mm',corpus)

tfidf = models.TfidfModel(corpus,dict,normalize=False)
tfidf.save('tfidf_question_stop.model')




