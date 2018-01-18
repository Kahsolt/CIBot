#encoding: utf-8
from django.db import models
from .Question import Question


# [运行时-活跃任务列表] =>[问题]
class RtTask(models.Model):
    question = models.ForeignKey(Question, help_text='等待解决的问题', on_delete=models.CASCADE)
    count = models.IntegerField(default=0, help_text='任务分发量')
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '[%s]: %s' %(self.question.id, self.create_time)
