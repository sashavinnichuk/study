# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from PIL import Image
from django.views.generic import UpdateView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView
from django import forms

from ..util import paginate, get_current_group

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models.students_model import Student
from ..models.groups_model import Group
from django.utils.translation import ugettext as _









def students_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paginate students
    context = paginate(students, 3, request, {}, var_name ='students')

    return render(request, 'students/students_list.html', context)

@login_required
def students_add(request):
    # Якщо форма була запощена:
    if request.method == "POST":

        # Якщо кнопка Додати була натиснута:
        if request.POST.get('add_button') is not None:
            # Перевіряємо дані на коректність та збираємо помилки
            errors = {}

            data = {'middle_name': request.POST.get('middle_name'), 'notes': request.POST.get('notes')}

            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = _(u"First Name field is required")
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = _(u"Last Name field is required")
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = _(u"Date field is required")
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = _(u"Input correct format of data (ex. 1984-12-30)")
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = _(u"Ticket number is required")
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = _(u"Group field is required")
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = _(u"Choose correct group")
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                try:
                    im = Image.open(photo)
                    im.verify()
                except Exception:
                    errors['photo'] = _(u"Added Photo is incorrect")
                else:
                    data['photo'] = photo

            # Якщо дані були введені коректно:
            if not errors:
                # Створюємо та зберігаємо студента в базу
                student = Student(**data)

                student.save()

                # Повертаємо користувача до списку студентів
                return HttpResponseRedirect(u'%s?status_message=%s' %reverse('home'), _(u"Student added successfully!"))

            # Якщо дані були введені некоректно:
            else:
                # Віддаємо шаблон форми разом із знайденими помилками
                return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'), 'errors': errors})

        # Якщо кнопка Скасувати була натиснута:
        elif request.POST.get('cancel_button') is not None:
            # Повертаємо користувача до списку студентів
            return HttpResponseRedirect(u'%s?status_message=%s' %reverse('home'), _(u"Student aded canceled!!!"))
        # Якщо форма не була запощена:
    else:
        # повертаємо код початкового стану форми
        return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)
def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', _(u'Save'), css_class ="btn btn-primary"),
            Submit('cancel_button', _(u'Cancel'), css_class ="btn btn-link"),
        )


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'), _(u"Student updated successfully!"))
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' %reverse('home'), _(u"Student edit canceled!!!"))
        else:
            return super(StudentUpdateView, self).post(request, *args, ** kwargs)
        
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return u'%s?status_message=%s'% (reverse('home'), _(u"Student deleted successfully"))
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' %reverse('home'), _(u"Student delete canceled!!!"))
        else:
            return super(StudentDeleteView, self).post(request, *args, ** kwargs)


