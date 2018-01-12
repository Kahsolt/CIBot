from django.db import models

class ImportFile(models.Model):
    File = models.FileField(upload_to='LogFile')
    FileName = models.CharField(max_length=50, verbose_name=u'文件名')

    class Meta:
        ordering = ['FileName']

    def __str__(self):
        return self.FileName