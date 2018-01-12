from django.db import models


# {问题关键词} <=[问题]
class Keyword(models.Model):
    name = models.CharField(null=True, blank=True, max_length=64)
    father = models.CharField(null=True, blank=True, max_length=64)
    son = models.CharField(null=True, blank=True, max_length=64)

    def __str__(self):
        return self.name + self.father + self.son

    @classmethod
    def to_json(cls):
        return {
            'keywords': [kw.name for kw in Keyword.objects.all()]
        }

    @classmethod
    def importXml(self, dist):
        t = Keyword.objects.get_or_create(name=dist['keywords'], father=dist['cat'], son=dist['subcat'])
        return t
