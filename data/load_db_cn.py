# -*- coding:utf-8 -*-
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CIBot.settings")
django.setup()
from app.models import Answer,Question,User,Keyword
import json

# 完成中文数据加载
def load_db(file):
    f = open(file, 'r')
    data = json.load(f)
    return data

def main():
    data = load_db('health')
    # data = load_db('me_test.ann.json')
    # print(data)
    admin = User.objects.get(uid='admin')
    rawfile = open('raw_data','a+')
    for item in data:
        buffer = ""
        # item = data[item]
        # print(item['que'],item['ans'])
        q,created = Question.objects.get_or_create(user = admin, content=item['que'])
        a = Answer.objects.get_or_create(user = admin, qid = q, content = item['ans'], isBest = True)
        buffer = buffer + str(q.qid) + "%%%%%" + item['que']
        # ans_item = item['evidences']
        # for ansid in ans_item:
        #     ans = ans_item[ansid]
        #     a = Answer.objects.create(user = admin, qid = q, content = ans['evidence'], isBest = True)

        rawfile.write(buffer+'\r\n')

    rawfile.close()


if __name__ == '__main__':
    main()