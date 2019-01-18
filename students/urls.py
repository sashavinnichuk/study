from django.conf.urls import url , include
from .views import groups_view , journal_view , students_view


urlpatterns = [
    # Students urls
    url(r'^$', students_view.students_list, name='home'),
    url(r'^students/add/$', students_view.students_add, name='students_add'),
    url(r'^students/(?P<sid>\d+)/edit/$', students_view.students_edit, name='students_edit'),
    url(r'^students/(?P<sid>\d+)/delete/$', students_view.students_delete,
        name='students_delete'),

    # Groups urls
    url(r'groups/$', groups_view.groups_list, name='group'),
    url(r'^groups/add/$', groups_view.groups_add, name='groups_add'),
    url(r'^groups/(?P<gid>\d+)/edit/$', groups_view.groups_edit, name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete/$', groups_view.groups_delete,
        name='groups_delete'),
]