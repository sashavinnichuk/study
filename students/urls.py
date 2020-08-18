from django.conf.urls import url, include
from .views import groups_view , students_view, contact_admin_view
from students.views.students_view import StudentUpdateView, StudentDeleteView
from students.views.groups_view import GroupUpdateView, GroupDeleteView
from students.views.journal import JournalView
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Students urls
    url(r'^$', students_view.students_list, name='home'),
    url(r'^students/add/$', students_view.students_add, name='students_add'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),

    # Groups urls
    url(r'groups/$', groups_view.groups_list, name='group'),
    url(r'^groups/add/$', groups_view.groups_add, name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),
    
    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),
    
    # User Related urls
    url(r'^users/profile/$', login_required(TemplateView.as_view(template_name='registration/profile.html')), name='profile'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^registration_complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),

    # Contact Admin Form
    url(r'^contact-admin/$', contact_admin_view.contact_admin, name='contact_admin'),
]
