from django.conf.urls import url
from . import views

app_name = 'monitor'
urlpatterns = [
    # url(r'^$', views.main_page, name='main'),
    url(r'^device_model/detail/(?P<model_id>[0-9]+)$', views.device_model_page_detail, name='device_model_detail'),
    url(r'^device_item/detail/(?P<item_id>[0-9]+)$', views.device_item_page_detail, name='device_item_detail'),
    url(r'^device_model/add$', views.device_model_page_detail, {'type': 'add'}, name='device_model_add'),
    url(r'^device_item/add$', views.device_item_page_detail, {'type': 'add'}, name='device_item_add'),
    url(r'^device_model$', views.device_model_page, name='device_model'),
    url(r'^device_item$', views.device_item_page, name='device_item'),
    url(r'^user$', views.user_page, name='user'),
    url(r'^connection$', views.connection_page, name='connection'),
    url(r'^context$', views.context_page, name='context'),

    url(r'^index$', views.index_page),

    url(r'^test$', views.test_page, name='test'),
    url(r'^$', views.index_page, name='index'),
]