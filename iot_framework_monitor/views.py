from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.views.generic.edit import FormView
import logging, json, time

from iot_framework_server import db_manager

logging.basicConfig(
    format="[%(name)s][%(asctime)s] %(message)s",
    handlers=[logging.StreamHandler()],
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def device_model_page_detail(request, type='detail', model_id=None):
    context = dict()
    context['type'] = type
    if type == 'detail' and model_id:
        db = db_manager.DbManager()
        context['device_model'] = db.retrieve_device_model(model_id=model_id)[0]
        db.close()
    return render(request, 'monitor/device_model_detail.html', context)


def device_item_page_detail(request, type='detail', item_id=None):
    context = dict()
    context['type'] = type
    db = db_manager.DbManager()
    if type == 'detail' and item_id:
        context['device_item'] = db.retrieve_device_item(item_id=item_id)[0]
    context['model_list'] = db.retrieve_device_model()
    context['user_list'] = db.retrieve_user_list()
    db.close()
    return render(request, 'monitor/device_item_detail.html', context)


def device_user_page_detail(request, type='detail', user_id=None):
    context = dict()
    context['type'] = type
    if type == 'detail' and user_id:
        db = db_manager.DbManager()
        context['user_info'] = db.retrieve_user(user_id=user_id)
        db.close()
    return render(request, 'monitor/user_detail.html', context)


def device_model_page(request):
    context = dict()

    dt_list = list()
    db = db_manager.DbManager()
    model_list = db.retrieve_device_model()
    for model in model_list:
        data = list()
        data.append(model['model_id'])
        data.append(model['model_name'])
        data.append(model['model_network_protocol'])
        if data:
            dt_list.append(data)
    context['dt_list'] = json.dumps(dt_list)
    db.close()
    return render(request, 'monitor/device_model.html', context)


def device_item_page(request):
    context = dict()

    dt_list = []
    db = db_manager.DbManager()
    item_list = db.retrieve_device_item()
    for item in item_list:
        data = list()
        data.append(item['item_id'])
        data.append(item['model_id'])
        data.append(item['user_id'])
        data.append(item['item_address'])
        data.append(item['item_name'])
        data.append(item['connected'])
        if data:
            dt_list.append(data)
    context['dt_list'] = json.dumps(dt_list)
    db.close()
    return render(request, 'monitor/device_item.html', context)


def user_page(request):
    context = dict()

    dt_list = list()
    db = db_manager.DbManager()
    user_list = db.retrieve_user_list()
    for user in user_list:
        data = list()
        data.append(user['user_id'])
        data.append(user['user_name'])
        if data:
            dt_list.append(data)
    context['dt_list'] = json.dumps(dt_list)
    db.close()
    return render(request, 'monitor/user.html', context)


def connection_page(request):
    context = dict()
    return render(request, 'monitor/connection.html', context)


def context_data_page(request, context_id, series_type='context'):
    context = dict()
    context['context_id'] = context_id
    context['series_type'] = series_type
    db = db_manager.DbManager()
    ctx = dict()
    if series_type == 'context':
        ctx = db.retrieve_context(context_id=context_id)[0]
        ctx['data'] = json.dumps(db.retrieve_context_data(context_id=context_id))
    elif series_type == 'series':
        ctx = db.retrieve_series_context(context_id=context_id, json_load=False)[0]
        ctx['time'] = [ctx['time_from'], ctx['time_to']]
    db.close()
    context['context'] = ctx
    return render(request, 'monitor/context_data.html', context)


def context_page(request):
    context = dict()
    dt_list = list()
    db = db_manager.DbManager()
    context_list = db.retrieve_context()
    for ctx in context_list:
        # ctx_data = db.retrieve_context_data(context_id=ctx['context_id'])
        # context['data'] = context_data
        data = list()
        data.append(ctx['device_item_id'])
        data.append(ctx['type'])
        data.append(ctx['time'])
        # data.append(json.dumps(context_data))
        # data.append(ctx_data)
        data.append(ctx['context_id'])
        data.append('context')
        if data:
            dt_list.append(data)
    series_context_list = db.retrieve_series_context()
    for ctx in series_context_list:
        data = list()
        data.append(ctx['device_item_id'])
        data.append(ctx['type'])
        ctx_time = (ctx['time_from'], ctx['time_to'])
        data.append(ctx_time)
        # data.append(ctx['data'])
        data.append(ctx['context_id'])
        data.append('series')
        if data:
            dt_list.append(data)
    context['dt_list'] = json.dumps(dt_list)
    db.close()
    return render(request, 'monitor/context.html', context)


def test_page(request):
    context = dict()
    return render(request, 'monitor/test.html', context)


def index_page(request):
    context = dict()
    return render(request, 'monitor/index.html', context)
