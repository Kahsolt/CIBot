# -*- coding:utf-8 -*-
# 与Yahoo Answer xml格式数据集相关的方法
import xml.sax
import pprint


# 输入为xml文件，输出为由字典组成的list
class QuesHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.tag = ""
        self.dlist = []
        self.dist = {}
        self.tmp = []

    def startElement(self, name, attrs):
        self.tag = name
        self.buffer = ""

    def characters(self, content):
        self.buffer += content
        if (self.dist == 'answer_item'):
            self.tmp.append(self.buffer)

    def endElement(self, name):
        if (name in ['uri', 'subject', 'content', 'bestanswer', 'cat', 'maincat', 'subcat', 'date',
                     'res_date', 'vot_date', 'lastanswerts', 'best_id']):
            self.dist[name] = self.buffer.replace('<br />', ' ')

        elif (name == 'answer_item'):
            self.tmp.append(self.buffer.replace('<br />', ' '))

        elif (name == 'nbestanswers'):
            self.dist[name] = self.tmp
            self.tmp = []

        elif (name == 'document'):
            self.dlist.append(self.dist)
            self.dist = {}

# 从文件中读取数据
def importFile(str):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = QuesHandler()
    parser.setContentHandler(handler)
    parser.parse(str)
    # pprint.pprint(handler.dlist) #调试用
    return handler.dlist

from django.db import models
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CIBot.settings")
django.setup()

from app.models.Answer import Answer
from app.models.Question import Question
from app.models.Keyword import Keyword
from app.models.User import User

#直接在路径下用命令行输入python xml_input.py运行导入
# dist = load_db.importFile("xml_proc/small_sample.xml")#输入xml文件路径
# dist = load_db.importFile("F:\\FullOct2007.xml")#输入xml文件路径

def dist2db(dist):
    User.import_xml(dist)
    Keyword.importXml(dist)
    Question.import_file(dist)
    Answer.importXml_best(dist)
    for item in dist['nbestanswers']:
        Answer.importXml(dist,item)

class QuesHandler1(xml.sax.ContentHandler):
    def __init__(self,file):
        self.subject = ""
        self.content = ""
        self.answer = ""
        self.current = ""
        self.f = file

    def startElement(self, name, attrs):
        self.current = name

    def endElement(self, name):
        if self.current == 'subject':
            self.f.write('\n')
        self.current = ""

    def characters(self, content):
        # if self.current in ['subject','content','answer_item']:
        if self.current == 'uri':
            self.f.write(content + ' %%%%% ')
        if self.current == 'subject':
            self.f.write(content)

def xml2txt(xmlpath, txtpath):
    # f = open('F:\\full_subject_id.txt', 'w', encoding='utf-8')
    f = open(txtpath, 'w', encoding='utf-8')
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = QuesHandler1(txtpath)
    parser.setContentHandler(Handler)

    # parser.parse("small_sample.xml")
    # parser.parse("F:\\FullOct2007.xml")
    parser.parse(xmlpath)
    f.flush()
    f.close()