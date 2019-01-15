from django.conf.urls import url , include
from .views import groups , journal , students
from django.contrib import admin

urlpatterns = [
    # Students urls
    url(r'^$', students.students_list,  name='home'),
    url(r'^students/add/$', students.students_add, name='students_add'),
    url(r'^students/(?P<sid>\d+)/edit/$', students.students_edit, name='students_edit'),
    url(r'^students/(?P<sid>\d+)/delete/$', students.students_delete,
        name='students_delete'),

    # Groups urls
    url(r'groups/$', groups.groups_list, name='group'),
    url(r'^groups/add/$', groups.groups_add, name='groups_add'),
    url(r'^groups/(?P<gid>\d+)/edit/$', groups.groups_edit, name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete/$', groups.groups_delete,
        name='groups_delete'),

    url(r'^admin/', include(admin.site.urls)),
]