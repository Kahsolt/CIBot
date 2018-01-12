import datetime

from django.test import TestCase

# 单元和集成测试 Tests
#    RegularTest    常规测试，主要测试正确用例的可用性
#    EdgeTest       边缘测试，主要测试极端用例对系统的安全性影响
#
# （我觉得一般都没人愿意写）


class RegularTest(TestCase):
    def setUp(self):
        pass

    def testWhat(self):
        pass


class EdgeTest(TestCase):
    def setUp(self):
        pass

    def testWhat(self):
        pass


### Faker
import random

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
SYMBOL = '~!@#$%^&*()_{}:"<>`,./;[]\\'
DIGIT = '0123456789'
ALPH_DIG = ALPHABET + DIGIT
CHARACTER = ALPHABET + SYMBOL + DIGIT

def fakeUsername(length=10):
    ret = ''
    for i in range(length):
        ret += random.choice(ALPH_DIG)
    return ''.join(ret)

def fakePassword(length=10):
    ret = ''
    for i in range(length):
        ret += random.choice(CHARACTER)
    return ''.join(ret)

def fakeString(length=8):
    ret = ''
    for i in range(length):
        ret += random.choice(ALPHABET)
    return ''.join(ret)

def fakeNumber(length=10):
    ret = ''
    for i in range(length):
        ret += random.choice(DIGIT)
    return ''.join(ret)

def fakeInteger(min=0, max=100):
    return random.randint(min, max)

def fakeFloat(min=0, max=180):
    return (random.random()*(max-min)+min)

def fakeDatetime():
    return datetime.datetime.now().replace(month=fakeInteger(1, 12), day=fakeInteger(1, 28)).strftime('%Y-%m-%d %H:%M:%S')

def fakeLorem(length=110):
    lorem = ''
    while len(lorem) <= length:
        lorem += fakeString(fakeInteger(5, 12))
        lorem += '. '
    return lorem

def fakeUrl():
    url = 'http://'
    url += fakeString(fakeInteger(5, 12))
    url += random.choice(['.com', '.org', '.edu', '.net', '.tk'])
    url += '//'
    url += fakeString(fakeInteger(6, 10))
    url += '//'
    url += fakeString(fakeInteger(4, 12))
    url += '//'
    return url

