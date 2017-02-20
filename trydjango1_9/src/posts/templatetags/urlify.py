# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 21:25:41 2017

@author: Mark Account
"""

from urllib.parse import quote_plus
from django import template



register = template.Library()

@register.filter
def urlify(value):
    return quote_plus(value)