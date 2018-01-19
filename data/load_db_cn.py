# -*- coding:utf-8 -*-
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CIBot.settings")
django.setup()
import json
from app.models import Answer,Question,User,Keyword

# TODO: 完成中文数据加载
def load_db(file):
    f = open(file, 'r')
    data = json.load(f)
    return data

def main():
    data = load_db('me_test.ann.json')
    # print(data)
    admin = User.objects.get(uid='admin')
    for key in data:
        item = data[key]
        q,created = Question.objects.get_or_create(user = admin, content=item['question'])
        ans_item = item['evidences']
        for ansid in ans_item:
            ans = ans_item[ansid]
            a = Answer.objects.create(user = admin, qid = q, content = ans['evidence'], isBest = True)

if __name__ == '__main__':
    main()