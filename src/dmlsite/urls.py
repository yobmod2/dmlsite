"""
URL configuration for simpleproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from dmlmain.views import test

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    # path('accounts/login/$', 'django.contrib.auth.login', name='login'),
    # path('accounts/logout/$', 'django.contrib.auth.logout, name='logout',
    #       kwargs={'next_page': '/'}),
    path("accounts/", include("allauth.urls")),
    path("", include("dmlmain.urls")),
    path("test/", test, name="test"),
    # path(r'^blog/', include('dmlblog.urls', namespace='blog')),
    # path(r'^polls/', include('dmlpolls.urls', namespace='polls')),
    # path(r'^comments/', include('dmlcomments.urls', namespace='comments')),
    # path(r'^research/', include('dmlresearch.urls', namespace='research')),
    # path(r'^chat/', include('dmlchat.urls', namespace='chat')),
]
