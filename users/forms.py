# -*- coding: utf-8 -*-
from django import forms

from users.models import UserProfile

class UserProfileForm(forms.ModelForm):

    def save(self, user, **kwargs):
        form = super(UserProfileForm, self).save(commit=False,**kwargs)
        form.user = user
        form.save()


    class Meta:
        model = UserProfile
        fields = ['school_id','username','nickname','college','grade', 'major', 'gender','telephone', 'qq',] 


