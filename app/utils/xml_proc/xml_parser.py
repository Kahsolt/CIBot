# -*- coding: UTF-8 -*-
# 从文件中读取数据
import xml.sax

class QuesHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.subject = ""
        self.content = ""
        self.answer = ""
        self.current = ""

    def startElement(self, name, attrs):
        self.current = name

    def endElement(self, name):
        if self.current == 'subject':
            f.write('\n')
        self.current = ""

    def characters(self, content):
        # if self.current in ['subject','content','answer_item']:
        if self.current == 'uri':
            f.write(content + ' %%%%% ')
        if self.current == 'subject':
            f.write(content)

f = open('F:\\full_subject_id.txt','w',encoding='utf-8')
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces,0)

Handler = QuesHandler()
parser.setContentHandler(Handler)

# parser.parse("small_sample.xml")
parser.parse("F:\\FullOct2007.xml")
f.flush()
f.close()