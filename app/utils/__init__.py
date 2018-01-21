# -*- coding:utf-8 -*-
import json
import socket
import logging
import threading
import jieba
from django.conf import settings
from django.shortcuts import HttpResponse
from CIBot.settings import QASNAKE_HOST, QASNAKE_PORT
from app.models import *

logger = logging.getLogger("django")

# 服务工具包 Utils
#   Aux functions for views.py
#


# Section A 业务计算
def find_user(que):
    newline = jieba.cut(que, cut_all=False)
    str_out = ""
    # 哥，请改用正则表达式 (by kahsolt
    str_out = str_out + ' '.join(newline).replace('，', ' ').replace('。', ' ').replace('、', ' ').replace('；', ' ') \
        .replace('：', ' ').replace('“', ' ').replace('”', ' ').replace('【', ' ').replace('】', ' ').replace('！', ' ') \
        .replace('……', ' ').replace('《', ' ').replace('》', ' ').replace('~', ' ').replace('·', ' ').replace('（', ' ') \
        .replace('）', ' ').replace('-', ' ').replace(',', ' ').replace('.', ' ').replace(':', ' ')

    key_list = str_out.split(' ')
    try:
        final_key_list = []
        word = ""
        for word in key_list:
            if(word == ""):
                continue
            cout = 0
            temp_key_list = settings.WORD2VEC_MODEL.similar_by_word(word)
            for k in temp_key_list:
                final_key_list.append(k[0])
                cout = cout + 1
                if (cout > 3):
                    break;
        user_list = []
        cout_list = []
        for word in final_key_list:
            print(word)
            try:
                obj = User.objects.filter(tags__name = word)
                if(obj != None):
                    for user in obj:
                        flag = True
                        for i in range(len(user_list)):
                            if(user == user_list[i]):
                                cout_list[i] = cout_list[i] + 1
                                flag = False
                                break
                        if(flag):
                            user_list.append(user)
                            cout_list.append(1)
            except User.DoesNotExist:
                continue
            except Exception as e:
                print(e)

        for i in range(len(user_list)):
            print(user_list[i].username + " " + str(cout_list[i]))
        if len(user_list)>0:
            return user_list
    except Exception as e:
        print(e)
    print("over~")
    return False

def qa_dispatcher(data):
    quest = data.get('question')
    if not quest:
        return ''
    #to do：判断q是否存在
    # Save Question
    print("cibot get the question:"+quest)
    try:
        print("cibot get the uid:" + data.get('uid'))
        u = User.objects.get(uid=data.get('uid'))
        q = Question.objects.create(user=u, content=quest)
    except:
        q = Question.objects.create(content=quest)  # for anonymous
    # q.keywords.add()
    # q.save()
    # logger.info('[Q] new quest, qid=%d', q.id)

    # dispatch SE
    # TODO: try to ASYNC this part!!
    # t = threading.Thread(target=qa_snake, args=(data.get('question'),))
    # t.setDaemon(True)
    # t.start()
    #To do:是否有类似问题？
    #if not
    
    snake_re = qa_snake(data.get('question'))
    #
    if snake_re.get('founded'):
        resp = {'qid':q.qid,'answer':snake_re.get('answer')}
        return resp
    else:
        print("qa_snake give no answer")
        users = find_user(data.get('question'))
        if users :
            resp = {'qid':q.qid,'answer':snake_re.get('answer'),'user':users}
        else:
            resp = {'qid': q.qid, 'answer': snake_re.get('answer')}

    # dispatch local-DB

    # dispatch CI

    return resp




def qa_snake(kw):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((QASNAKE_HOST, QASNAKE_PORT))
        client.settimeout(30)
        client.send(kw.encode('utf8'))
        ans = client.recv(4096).decode('utf8')
        logger.info('[QA-Snake] %s...' % ans[:30])
        return ans
    except Exception as e:
        print(e)
        return None


# Section B 语法糖 Wrapper
def response_write(jsonData):
    response = HttpResponse(json.dumps(jsonData, ensure_ascii=False))
    return response


def json_load(byteData):
    try:
        strData = isinstance(byteData, bytes) and byteData.decode('utf8') or byteData
        logger.info('Raw Data: %s' % strData)
        jsonData = json.loads(strData, encoding='utf8', parse_int=int, parse_float=float)
        logger.info('Received Json Data: %s' % jsonData)
        return jsonData
    except :
        raise Exception('Bad Json Data')


# Section C 错误码 Error Code
def die(codeno):
    ERRMSG = {
        200: 'Done',
        400: 'Malformatted Request',
        401: 'Not Authorized',
        403: 'Missing Parameter or TypeError',
        404: 'Resource Not Found',
        405: 'Method Not Allowed',
        500: 'Server Internal Error',
        000: 'Not Implemented Yet',
    }

    return {'errorno': codeno, 'errormsg': ERRMSG.get(codeno) or 'Unkown Error'}


# Section D 默认值配置 Defaults

# Section E 导入xml文件
