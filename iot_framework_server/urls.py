"""iot_framework_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import include, url
from django.contrib import admin
from . import apis, settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/agent$', apis.handle_agent_mgt),
    url(r'^api/user$', apis.handle_user_mgt),
    url(r'^api/device_model$', apis.handle_device_model_mgt),
    url(r'^api/device_item$', apis.handle_device_item_mgt),
    url(r'^api/context$', apis.handle_context_mgt),
    url(r'^api/series_context$', apis.handle_series_context_mgt),
    url(r'^api/context_retrieve$', apis.handle_context_retriever),
    url(r'^api/connect$', apis.handle_connection_mgt),
    url(r'^api/statistics$', apis.handle_statistics_mgt),

    url(r'^', include('iot_framework_monitor.urls')),
]

if settings.DEBUG and not urlpatterns:
    urlpatterns += staticfiles_urlpatterns()