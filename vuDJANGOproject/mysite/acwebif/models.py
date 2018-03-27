# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class MyLog(models.Model):
    log_text = models.CharField(max_length=200)
    log_date = models.DateTimeField('date logged')
    def __str__(self):
        return self.log_text
    def was_logged_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
