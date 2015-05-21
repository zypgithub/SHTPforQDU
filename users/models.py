#coding:utf-8
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    school_id = models.CharField(max_length=12, null=False, blank=False)
    username = models.CharField(max_length=30, null=False, blank=False)
    nickname = models.CharField(max_length=30, null=False, blank=False)
    college = models.CharField(max_length=30, null=False, blank=False)
    grade = models.CharField(max_length=10, null=False, blank=False)
    major = models.CharField(max_length=20, null=False, blank=False)
    gender = models.CharField(max_length=1, null=False, blank=False)
    telephone = models.CharField(max_length=15, null=False, blank=False)
    qq = models.CharField(max_length=20, null=False, blank=False)
   # pswquestion = models.CharField(max_length=30, null=False, blank=False)
   # pswanwser = models.CharField(max_length=30, null=False, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"

    def __unicode__(self):
        return u"School Id: %s Username: %s Nickname: %s College: %s Grade: %s Major: %s Gender: %s " % (
                self.school_id, self.username, self.nickname, self.college, 
                self.grade, self.major, self.gender)
