# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, DeleteView
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from ..models.groups_model import Group
from ..models.students_model import Student

@login_required
def groups_add(request):
    # Якщо форма була запощена:
    if request.method == "POST":

        # Якщо кнопка Додати була натиснута:
        if request.POST.get('add_button') is not None:
            # Перевіряємо дані на коректність та збираємо помилки
            errors = {}

            data = {'notes': request.POST.get('notes')}

            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = _(u"First Name field is required")
            else:
                data['title'] = title

            leader = request.POST.get('leader', '').strip()
            if not leader:
                errors['leader'] = _(u"Group field is required")
            else:
                groups = Group.objects.filter(pk=leader)
                if len(groups) != 1:
                    errors['leader'] = _(u"Choose correct group")
                else:
                    data['leader'] = groups[0]

            # Якщо дані були введені коректно:
            if not errors:
                # Створюємо та зберігаємо студента в базу
                group = Group(**data)

                group.save()

                # Повертаємо користувача до списку студентів
                return HttpResponseRedirect(u'%s?status_message=%s' %reverse('home'), _(u"Group added successfully!"))

            # Якщо дані були введені некоректно:
            else:
                # Віддаємо шаблон форми разом із знайденими помилками
                return render(request, 'students/groups_add.html', {'students': Student.objects.all().order_by('last_name'), 'errors': errors})

        # Якщо кнопка Скасувати була натиснута:
        elif request.POST.get('cancel_button') is not None:
            # Повертаємо користувача до списку студентів
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('group'), _(u"Group added canceled!!!")))
        # Якщо форма не була запощена:
    else:
        # повертаємо код початкового стану форми
        return render(request, 'students/groups_add.html', {'students': Student.objects.all().order_by('last_name')})



def groups_list(request):
    groups = Group.objects.all()

    # try to order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    # paginate groups
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        groups = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
        groups = paginator.page(paginator.num_pages)

    return render(request, 'students/groups_list.html', {'groups': groups})

class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})
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

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_edit.html'
    form_class = GroupUpdateForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GroupUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('group'), _(u"Student updated successfully!"))
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('group'), _(u"Student edit canceled!!!")))
        else:
            return super(GroupUpdateView, self).post(request, *args, ** kwargs)

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GroupDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return u'%s?status_message=%s'% (reverse('group'), _(u"Group deleted successfully"))
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('group'), _(u"Group delete canceled!!!")))
        else:
            return super(GroupDeleteView, self).post(request, *args, ** kwargs)


