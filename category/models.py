#coding:utf-8
from django.db import models

class category(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    alter_at = models.DateTimeField(auto_now=True)
    production_count = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        verbose_name="category"
        verbose_name_plural="categories"

    def __unicode__(self):
        return u"name:%s created_at: %s latest_at: %s production_count: %d" % (self.name, self.created_at, self.alter_at, self.production_count)


