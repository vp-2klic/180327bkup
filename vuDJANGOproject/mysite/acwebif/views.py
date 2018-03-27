# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render

import datetime

from .models import MyLog

# Create your views here.

class IndexView(generic.ListView):
    template_name = "acwebif/index.html"
    context_object_name = "latest_log_list"

    def get_queryset(self):
        return MyLog.objects.order_by('-log_date')[:20]

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It's now %s.</body></html>" % now
    return HttpResponse(html)
