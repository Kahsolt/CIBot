#encoding: utf-8
from .Answer import Answer
from .Keyword import Keyword
from .Question import Question
from .Tag import Tag
from .User import User
from .RtTask import RtTask
from .RtUser import RtUser


#
# 模型层 Model
#    为了避免模型层臃肿，复杂业务请放在Service层(views.py)
#
# 关系例图：
#    [实体]       一 -> 一              | 且，和，同时
#    {弱实体}     一 => 多               & 连接(若干个关系式)
#    <关系>      (箭头反向时为反向查询set)
#
