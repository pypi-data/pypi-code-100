# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``views`` module defines ``View`` objects for converting web requests
into rendered responses.
"""

from django.shortcuts import render


def error_404(request, exception):
    return render(request, 'error_pages/error_404.html')


def error_500(request):
    return render(request, 'error_pages/error_500.html')
