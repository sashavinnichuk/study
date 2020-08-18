# -*- coding: utf-8 -*-
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from ..models import MonthJournal
from ..util import paginate
from ..models.students_model import Student
from django.http import JsonResponse

class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)
        # перевіряємо чи передали нам місяць в параметрі,
        # якщо ні - вичисляємо поточний;
        # поки що ми віддаємо лише поточний:
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()
        else:
            today = datetime.today()
            month = date(today.year, today.month, 1)
        # обчислюємо поточний рік, попередній і наступний місяці
        # а поки прибиваємо їх статично:
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')
        # також поточний місяць;
        # змінну cur_month ми використовуватимемо пізніше
        # в пагінації; а month_verbose в
        # навігації помісячній:
        context['cur_month'] = month.strftime('%Y-%m-%d')
        # тут будемо обчислювати список днів у місяці,
        # а поки заб'ємо статично:
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{'day': d,
            'verbose': day_abbr[weekday(myear, mmonth, d)][:3]}
            for d in range(1, number_of_days + 1)]
        # витягуємо усіх студентів посортованих по
        if kwargs.get('pk'):
            queryset = [Student.objects.get(pk=kwargs['pk'])]
        else:
            queryset = Student.objects.order_by('last_name')
        # це адреса для посту AJAX запиту, як бачите, ми
        # робитимемо його на цю ж в'юшку; в'юшка журналу
        # буде і показувати журнал і обслуговувати запити
        # типу пост на оновлення журналу;
        update_url = reverse('journal')
        # пробігаємось по усіх студентах і збираємо
        # необхідні дані:
        students = []
        for student in queryset:
            #витягуємо журнал для студента і
            #вибраного місяця
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None
            # набиваємо дні для студента
            days = []
            for day in range(1, number_of_days+1):
                days.append({
                'day': day,
                'present': journal and getattr(journal, 'present_day%d' %day, False) or False,
                'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                })
            # набиваємо усі решту даних студента
            students.append({
                'fullname': u' % s % s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })  # застосовуємо піганацію до списку студентів
        context = paginate(students, 10, self.request, context, var_name='students')
        # повертаємо оновлений словник із даними
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        # prepare student, dates and presence data
        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])

        # get or create journal object for given student and month
        journal = MonthJournal.objects.get_or_create(student=student, date=month)[0]

        # set new presence on journal for given student and save result
        setattr(journal, 'present_day%d' % current_date.day, present)
        journal.save()
        # return success status
        return JsonResponse({'key': 'success'})