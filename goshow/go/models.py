# -*- encoding: utf-8 -*-#
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class List(models.Model):
    ''' Normal list '''
    title = models.CharField(max_length=30, verbose_name='ListName')
    user = models.ForeignKey(User, null=True, blank=True)
    public = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.title)

    def remove(self):
        self.removed = True

    def restore(self):
        self.removed = False


class ListItem(models.Model):
    ''' Item in list '''
    title = models.CharField(max_length=30, verbose_name='ItemName')
    nextstep = models.CharField(max_length=100, verbose_name='ItemStep')
    weight = models.IntegerField(default=0)
    checked = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    parent = models.ForeignKey(List)
    finishedDate = models.DateField(default=None)

    def __unicode__(self):
        return unicode(self.title)

    def setWeight(self, weight):
        self.weight = weight

    def check(self):
        self.checked = True
        self.finishedDate = datetime.now()

    def uncheck(self):
        self.checked = False
        self.finishedDate = None

    def remove(self):
        self.removed = True

    def restore(self):
        self.removed = False
