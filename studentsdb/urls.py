"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG

js_info_dict = {
    'packages': ('students',),
}

urlpatterns = [
    # Students urls
    url(r'^', include('students.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),
]

if DEBUG:
    # serve files from media folder
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT})
        ]
