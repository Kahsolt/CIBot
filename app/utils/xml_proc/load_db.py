# conding:utf-8
# -*- coding:utf-8 -*-
# 从文件中读取数据
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


def importFile(str):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = QuesHandler()
    parser.setContentHandler(handler)
    parser.parse(str)
    # pprint.pprint(handler.dlist)
    return handler.dlist


###test###
# d = importFile("small_sample.xml")  # 输入xml文件路径
#
# print(d)