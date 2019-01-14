# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

# Views for Students
def students_list(request):
    students = (
        {'id': 1,
        'first_name': u'Віталій',
        'last_name': u'Подоба',
        'ticket': 235,
        'image': 'img/1.jpg'},

        {'id': 2,
        'first_name': u'Корост',
        'last_name': u'Андрій',
        'ticket': 2123,
        'image': 'img/2.jpg'},

        {'id': 3,
         'first_name': u'Потапенко',
         'last_name': u'Артем',
         'ticket': 2223,
         'image': 'img/3.jpg'},
    )
    return render(request, 'students/students_list.html', {'students': students})
def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')
def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)
def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

# Views for Groups

def groups_list(request):
    groups = (
        {'id': 1,
         'group_name': u'МтМ-21',
         'group_leader': u'Ячменев Олег'},

        {'id': 2,
         'group_name': u'МтМ-22',
         'group_leader': u'Віталій Подоба'},

        {'id': 3,
         'group_name': u'МтМ-23',
         'group_leader': u'Іванов Андрій'},
    )
    return render(request, 'students/groups_list.html', {'groups': groups})
def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')
def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)
def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)