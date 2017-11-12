# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def index(request):
    return render(request,'layouts/index.html')

def courses(request):
    context = {'name': 'stuff'} # get course data from db
    
    return render(request,'ce_ledger/courses.html', context)
