from gensim import models,corpora,similarities
import logging,linecache
#load model & data

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
