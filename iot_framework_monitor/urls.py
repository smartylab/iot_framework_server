from django.conf.urls import url
from . import views

app_name = 'monitor'
urlpatterns = [
    # url(r'^$', views.main_page, name='main'),
    url(r'^test$', views.test_page, name='test'),
    url(r'^index$', views.index_page),
    url(r'^$', views.index_page, name='index'),
]