from django.db import models


# {用户标签} <=[用户]
class Tag(models.Model):
    name = models.CharField(null=True, blank=True, max_length=64)
    father = models.CharField(null=True, blank=True, max_length=64)
    son = models.CharField(null=True, blank=True, max_length=64)

    def __str__(self):
        return self.name + self.father + self.son

    @classmethod
    def to_json(cls):
        return {
            'tags': [t.name for t in Tag.objects.all()]
        }

    @classmethod
    def importXml(self,dist):
        t = Tag.objects.get_or_create(name = dist['keywords'], father = dist['cat'], son = dist['subcat'])
        return t
