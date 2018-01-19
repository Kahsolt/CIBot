#encoding: utf-8
from django.db import models
from .User import User
from .Question import Question


# [答案] ->[用户]|[问题]
class Answer(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, help_text='答主|为空时意为搜索引擎',on_delete=models.CASCADE)
    qid = models.ForeignKey(Question, help_text='对应的问题',on_delete=models.CASCADE)
    content = models.TextField(help_text='答案内容')
    isBest = models.BooleanField(help_text='是否最佳')
    grade = models.PositiveSmallIntegerField(blank=True, default=3, help_text='评分1-5')
    like = models.PositiveIntegerField(blank=True, default=0, help_text='赞同数')
    dislike = models.PositiveIntegerField(blank=True, default=0, help_text='反对数')

    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[%s] %s' % (self.user.username, self.content[:10])

    @classmethod
    def update_answerlist(cls, dist):
        try:
            u = User.objects.get(uid = dist['uid'])
            q = Question.objects.get(qid = dist['qid'])
            a, created = Answer.objects.get_or_create(user=u, content=dist['answer'], question0=q)
        except:
            print("poinson")

    @classmethod
    def qid_get_ans_con(cls,qid):
        ans = Answer.objects.get(qid = qid).content
        return ans
    @classmethod
    def importXml_best(self,dist):
        q, create = Question.objects.get_or_create(qid=dist['qid'])
        a = Answer.objects.get_or_create(qid = q, content=dist['bestanswer'], isBest=True)
        #a.question0.add(q)
        return a

    @classmethod
    def importXml(self, dist, item):
        q = Question.objects.get(qid = dist['qid'])
        a = Answer(qid = q, content=item, isBest=False)
        a.save()
        #a.question0.add(q)
        return a

