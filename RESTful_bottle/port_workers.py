# coding=utf-8
"""
synopsis: transfer requests to bussiness logic level
author: haoranzeus@gmail.com (zhanghaoran)
"""
from bll.receptionist import receptionist


def helloworld():
    return 'helloworld'


def add_cooker(foods):
    return receptionist.add_cooker()
