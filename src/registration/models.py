# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import datetime


class Registration(models.Model):
    #id = models.AutoField()

    user = models.ForeignKey(User)

    fullname = models.TextField(null=False, blank=False)

    notes = models.TextField()

    stct = models.BooleanField()
    ctpa = models.BooleanField()
    paso = models.BooleanField()
    sone = models.BooleanField()

    created_at = models.DateTimeField(blank=False, null=False, default=datetime.now)

    paid = models.BooleanField(blank=False, null=False, default=False)