#encoding: utf-8
import datetime

from django.shortcuts import redirect, render, resolve_url
from django.views.decorators.csrf import csrf_exempt

from CIBot.settings import LOG_FILE
from app.utils import *
from app.scheds import *

#
# 业务逻辑+视图层 Service/Controller + View
#   合理抽象出工具utils.py:)
#


# Headless API Views
@csrf_exempt
def user(request):
    try:
        us = request.body
        us = eval(json_load(us))
        us = us['users']
        for u in us:
            uid = u['id']
            uname = u['nickname']
            u = User.objects.get_or_create(uid=uid, username = uname)

        # uid = request.session.get('id')
        # u = User.objects.get_or_create(uid=uid)
        # if u:
        #     RtUser.objects.get_or_create(user=User.objects.get(uid=uid)).hello_time = datetime.datetime.now()
        #     return response_write(u.to_json())
        # else:
        #     return response_write(die(404))
    except:
        return response_write(die(401))


@csrf_exempt
def user_register(request):
    try:
        data = json_load(request.body)
        try:
            u = User()
            u.username=data.get('username')
            u.save()
            tag = data.get('tags')
            if (type(tag) == list):
                for tag in data.get('tags'):
                    t = Tag.objects.filter(name=tag).first()
                    if (t):
                        u.tags.add(t)
                    else:
                        t = Tag()
                        t.name = tag
                        t.save()
                        u.tags.add(t)
            else:
                #q:如果多个tag实际并不能进入第一个方法里面，这里先不管
                t = Tag()
                t.name = tag
                t.save()
                u.tags.add(t)
            u.save()
            return response_write(die(200))
        except Exception as e:
            print (e)
            u.delete()
            return response_write(die(404))
    except:
        return response_write(die(400))


@csrf_exempt
def user_login(request):
    try:
        data = json_load(request.body)
        u = User.objects.filter(username=data.get('username')).first()
        if u is not None:
            request.session['uid'] = u.id
            RtUser.objects.update_or_create(user=u)
            return response_write(die(200))
        else:
            return response_write(die(404))
    except:
       return response_write(die(400))


@csrf_exempt
def user_logout(request):
    uid = request.session.get('uid')
    RtUser.objects.get(user=User.objects.get(id=uid)).delete()
    request.session['uid'] = None
    return response_write(die(200))


@csrf_exempt
def user_keepalive(request):
    try:
        uid = request.session.get('uid')
        RtUser.objects.get(user=User.objects.get(id=uid)).hello_time = datetime.datetime.now()
        return response_write(die(200))
    except:
        return response_write(die(401))


def tag(request):
    return response_write(Tag.to_json())


@csrf_exempt
def q(request):
    try:

        data = json_load(request.body)
        resp = qa_dispatcher(data)
        return response_write({'answer': resp})
    except:
        return response_write(die(400))


@csrf_exempt
def a(request):
    try:

        data = json_load(request.body)
        resp = qa_callback(data)
        print('uid is '+resp)
        return response_write({'uid': resp})
    except:
        return response_write(die(000))


# Browser-oriented Views
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def test(request):
    if request.method == 'POST':
        resp = qa_dispatcher(request.POST.get('question'))
        return render(request, 'test.html', {'ans': resp})
    return render(request, 'test.html', {'ans':'input a question please??'})


def log(request):
    if request.GET.get("do") == 'clean':
        try:
            f = open(LOG_FILE, 'w+')
            f.write('===== [Log Cleaned] =====\n')
            f.close()
        except IOError as ioe:
            return HttpResponse('Failed due to %s... :(' % ioe)
        return redirect(resolve_url(log))
    else:
        f = open(LOG_FILE)
        logs = [l for l in f.readlines()][-100:]
        return render(request, 'log.html', {'logs': logs})
