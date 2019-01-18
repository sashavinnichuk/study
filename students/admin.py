# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models.students_model import Student
from .models.groups_model import Group
from django.contrib import admin

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)