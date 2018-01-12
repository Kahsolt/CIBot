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



