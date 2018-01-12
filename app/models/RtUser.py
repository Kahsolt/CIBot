from django.db import models
from .User import User


# [运行时-在线用户列表] =>[用户]
class RtUser(models.Model):
    user = models.ForeignKey(User, help_text='所关联的用户账户')
    hello_time = models.DateTimeField(auto_now_add=True, help_text='上次心跳检测时间')

    def __str__(self):
        return '[%s]: %s' %(self.user.username, self.hello_time)
