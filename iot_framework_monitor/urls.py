from django.conf.urls import url
from . import views

app_name = 'monitor'
urlpatterns = [
    # url(r'^$', views.main_page, name='main'),
    url(r'^device_model/detail/(?P<model_id>[0-9]+)$', views.device_model_page_detail, name='device_model_detail'),
    url(r'^device_item/detail/(?P<item_id>[0-9]+)$', views.device_item_page_detail, name='device_item_detail'),
    url(r'^user/info/(?P<user_id>[a-zA-Z0-9_-]+)$', views.device_user_page_detail, name='user_detail'),
    url(r'^device_model/add$', views.device_model_page_detail, {'type': 'add'}, name='device_model_add'),
    url(r'^device_item/add$', views.device_item_page_detail, {'type': 'add'}, name='device_item_add'),
    url(r'^user/add$', views.device_user_page_detail, {'type': 'add'}, name='user_add'),
    url(r'^device_model$', views.device_model_page, name='device_model'),
    url(r'^device_item$', views.device_item_page, name='device_item'),
    url(r'^user$', views.user_page, name='user'),
    url(r'^connection$', views.connection_page, name='connection'),
    url(r'^context/data/(?P<context_id>[0-9]+)$', views.context_data_page,
        {'series_type': 'context'}, name='context_data'),
    url(r'^context/series_data/(?P<context_id>[0-9]+)$', views.context_data_page,
        {'series_type': 'series'}, name='series_context_data'),
    url(r'^context/all$', views.context_all_page, name='context_all'),
    url(r'^context$', views.context_page, name='context'),
    url(r'^statistics/(?P<context_type>[a-z]+)/(?P<item_id>[0-9]+)/(?P<type>[0-9a-zA-z%_ -]+)/(?P<subtype>[0-9a-zA-z%_ -]+)$',
        views.statistics_detail_page, name='statistics_detail_subtype'),
    url(r'^statistics/(?P<context_type>[a-z]+)/(?P<item_id>[0-9]+)/(?P<type>[0-9a-zA-z%_ -]+)$',
        views.statistics_detail_page, name='statistics_detail'),
    url(r'^statistics/total$', views.statistics_total_page, name='statistics_total'),
    url(r'^statistics$', views.statistics_page, name='statistics'),

    url(r'^index$', views.index_page),

    url(r'^test$', views.test_page, name='test'),
    url(r'^$', views.index_page, name='index'),
]
