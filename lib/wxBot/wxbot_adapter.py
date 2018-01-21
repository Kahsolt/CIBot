#!/usr/bin/env python2
# -*- coding:utf-8 -*-
#
# author:       kahsolt
# create date:  2017-09-08
# update date:  2018-01-12

import sys

import requests
from wxbot import WXBot

# Consts / Magical Number
MSG_FROM_CONTACT = 4
MSG_TEXT = 0
QABOT_HELP = 'QaBot打开方式：\n    ? 我要问个问题诶\n    !123 我要回答123号问题诶'
URL_BASE = 'http://127.0.0.1:8000'
URL_USER = URL_BASE + '/user'
URL_Q = URL_BASE + '/q'
URL_A = URL_BASE + '/a'


import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class QaBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.is_contact_book_inited = False

    def schedule(self): #  考虑在SDK里加一个onLogin? (run once)
        if not self.is_contact_book_inited:
            self.send_contact_book()
            self.is_contact_book_inited = True

    def handle_msg_all(self, msg):
        if msg['msg_type_id'] != MSG_FROM_CONTACT and msg['content']['type'] != MSG_TEXT:
            return

        text = msg['content']['data'].strip(' \n\r\0\t')
        username = msg['user']['name']
        uid = msg['user']['id']
        qid = None

        if text in [u'?', u'？']:
            self.send_msg_by_uid(QABOT_HELP, uid)

        elif text.startswith(u'?') or text.startswith(u'？'):
            question = text[1:].strip(' \n\r\0\t')
            print('[Q] %s asks about "%s..."' % (username, question[:30]))

            resp = self.send_question(uid, question)
            if resp is None:
                reply = u'可能不在服务区?'
                self.send_msg_by_uid(reply, uid)
                return

            if resp.get('answer'):

                qid = resp.get('qid')
                answer = resp.get('answer')
                # print('this is a test message:')
                # print(resp)
                # print('[A-AI] Bot answered [#%d]: %s' % (qid, answer[:30]))
                reply = u'问题[#%d]的答案: \n%s' % (qid, answer)
                self.send_msg_by_uid(reply, uid)
                if resp.get('users'):
                    qid = resp.get('qid')
                    helpers = resp.get('users') or []
                    reply = u'快来抢答问题啦OwO: \n[#%d] %s\n' % (qid, question)
                    for helpers_id in helpers:
                        self.send_msg_by_uid(reply, helpers_id)
            else:
                reply = u'有问必答不知道，何况还是乱问的:o'
                self.send_msg_by_uid(reply, uid)
                self.send_msg_by_uid(QABOT_HELP, uid)

        elif text.startswith(u'!') or text.startswith(u'！'):
            def parse(text):
                i = 0
                while i < len(text):
                    if text[i] not in [str(digit) for digit in range(9)]:
                        break
                    i += 1
                try:
                    qid = int(text[0:i])
                    answer = text[i:].strip(' \n\r\0\t')
                except:
                    qid = None
                    answer = None
                return qid, answer

            qid, answer = parse(text[1:].strip(' \n\r\0\t'))
            if qid is None:
                print('[A] No Qid found ??')
                reply = u'您好像没有指定Qid诶OwO...'
                self.send_msg_by_uid(reply, uid)
            else:
                print('[A-CI] %s answered [#%d]: %s' % (username, qid, answer[:30]))
                self.send_answer(uid, qid, answer)

    def send_contact_book(self):
        data = {'users': []}
        # Dummy bot account
        u = {
            u'id': 'QaBot',
            u'nickname': 'QaBot',
            u'gender': 0,
        }
        data['users'].append(u)
        for u in self.contact_list:
            u = {
                u'id': u.get('UserName'),
                u'nickname': u.get('NickName'),
                u'gender': u.get('Sex'),
            }
            data['users'].append(u)
        f = open('user.list', 'w+')
        import json
        data = json.dumps(data)
        print(data)

        f.write(str(json.loads(data)))
        f.flush()
        f.close()
        try:
            requests.post(url=URL_USER, json=data)
            print('[Contact] Sent %d contacts info :)' % len(data['users']))
        except:
            print('[Contact] You live alone on the island, uha? :(')

    def send_question(self, uid, quest):
        data = {'uid': uid, 'question': quest}
        try:
            resp = requests.post(URL_Q, json=data).json()
            #attention!!!
            #I has no idea why resp's format is {answer{XXX}}!!!
            resp = resp.get('answer')
            if resp.get('user'):
                pass
            else:
                print('[Q] Got the response: %s' % resp)
                return resp
        except:
            print('[Q] You ask me, I ask whom?? :(')
            return None

    def send_answer(self, uid, qid, ans):
        data = {'uid': uid, 'qid': qid, 'anwser': ans}
        try:
            resp = requests.post(URL_A, json=data).json()
            print('[A-CI] Got the response: %s' % resp)
            return resp
        except:
            print('[A-CI] Wire been cut by mouse :(')
            return None


def main():
    bot = QaBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'tty'  # use terminal instead of 'png'
    bot.run()


if __name__ == '__main__':
    main()
