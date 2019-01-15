# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

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