#encoding: utf-8
from django.db import models
from .User import User
from .Keyword import Keyword
#import app.models.Answer


# [问题] ->[用户] & =>{问题关键词} & <=[答案]
class Question(models.Model):
    qid = models.AutoField(primary_key=True, unique=True, null=False, max_length=128, help_text='问题唯一标识')
    user = models.ForeignKey(User, blank=True, null=True, help_text='题主', on_delete=models.CASCADE)
    content = models.TextField(help_text='问题内容')
    date = models.TextField(help_text='提问时间')
    resdate = models.TextField(help_text='解决时间')
    votdate = models.TextField(help_text='投票时间')
    lastdate = models.TextField(help_text='最后回答时间')
    keys = models.TextField(null=True, help_text='关键词')
    keywords = models.ManyToManyField('Keyword', help_text='问题关键字')
    answers = models.ManyToManyField('Answer', help_text='答案')

    create_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '[%s] %s' % (self.qid or 'Anonymous', self.content[:10])

    @classmethod
    def find_alike(cls, ques):
        keywords=ques['keywords']
        key_list=keywords.split(' ')
        for word in key_list:
            print ("\n key is " + word + "\n")
        try:
            q = Question.objects.filter(keywords__name = keywords)
        except Question.DoesNotExist:
            return False
        if q:
            if q[0]:
                return q[0].id
        return False

    def get_uid_byqid(qid):
        try:
            q = Question.objects.get(qid = qid)
            return q.user.uid
        except Exception as e:
            print(e)
            print("NO SUCH QUESTION:QID = " + qid)
            return False
        return None

    @classmethod
    def update_questionlist(cls, dist):
        u = User.objects.get(uid = dist['uid'])
        p,created = Keyword.objects.get_or_create(name = dist['keywords'])
        #a,created = Answer.objects.get_or_create(name=dist['answers'])
        q,created = Question.objects.get_or_create(user = u,content = dist['question'])
        q.keywords.add(p)
        #q.answers.add(a)
        return q

    @classmethod
    def import_file(self,dist):
        #p, created = Keyword.objects.get(name = dist['keywords'])
        q = Question(qid = dist['qid'], content = dist['content'], date = dist['date'], keys = dist['keywords'],
                     resdate = dist['resdate'], votdate = dist['votdate'], lastdate = dist['lastdate'])
        q.save()
        #q.keywords.add(p)
        return q



