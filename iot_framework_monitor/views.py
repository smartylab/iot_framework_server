from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.views.generic.edit import FormView
from iot_framework_server import statistics
import logging, json, time
import pprint

from iot_framework_server import db_manager

logging.basicConfig(
    format="[%(name)s][%(asctime)s] %(message)s",
    handlers=[logging.StreamHandler()],
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def device_model_page_detail(request, type='detail', model_id=None):
    req_context = dict()
    req_context['type'] = type
    if type == 'detail' and model_id:
        db = db_manager.DbManager()
        req_context['device_model'] = db.retrieve_device_model(model_id=model_id)[0]
        db.close()
    return render(request, 'monitor/device_model_detail.html', req_context)


def device_item_page_detail(request, type='detail', item_id=None):
    req_context = dict()
    req_context['type'] = type
    db = db_manager.DbManager()
    if type == 'detail' and item_id:
        req_context['device_item'] = db.retrieve_device_item(item_id=item_id)[0]
    req_context['model_list'] = db.retrieve_device_model()
    req_context['user_list'] = db.retrieve_user_list()
    db.close()
    return render(request, 'monitor/device_item_detail.html', req_context)


def device_user_page_detail(request, type='detail', user_id=None):
    req_context = dict()
    req_context['type'] = type
    if type == 'detail' and user_id:
        db = db_manager.DbManager()
        req_context['user_info'] = db.retrieve_user(user_id=user_id)
        db.close()
    return render(request, 'monitor/user_detail.html', req_context)


def device_model_page(request):
    req_context = dict()

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
    req_context['dt_list'] = json.dumps(dt_list)
    db.close()
    return render(request, 'monitor/device_model.html', req_context)


def device_item_page(request):
    req_context = dict()

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
    req_context['dt_list'] = json.dumps(dt_list)
    db.close()
    return render(request, 'monitor/device_item.html', req_context)


def user_page(request):
    req_context = dict()

    dt_list = list()
    db = db_manager.DbManager()
    user_list = db.retrieve_user_list()
    for user in user_list:
        data = list()
        data.append(user['user_id'])
        data.append(user['user_name'])
        if data:
            dt_list.append(data)
    req_context['dt_list'] = json.dumps(dt_list)
    db.close()
    return render(request, 'monitor/user.html', req_context)


def connection_page(request):
    req_context = dict()
    return render(request, 'monitor/connection.html', req_context)


def context_data_page(request, context_id, series_type='context'):
    req_context = dict()
    req_context['context_id'] = context_id
    req_context['series_type'] = series_type
    db = db_manager.DbManager()
    ctx = dict()
    if series_type == 'context':
        ctx = db.retrieve_context(context_id=context_id)[0]
        ctx['data'] = json.dumps(db.retrieve_context_data(context_id=context_id))
    elif series_type == 'series':
        ctx = db.retrieve_series_context(context_id=context_id, json_load=False)[0]
        ctx['time'] = [ctx['time_from'], ctx['time_to']]
    db.close()
    req_context['context'] = ctx
    return render(request, 'monitor/context_data.html', req_context)


def context_page(request):
    return render(request, 'monitor/context.html')


def context_all_page(request):
    req_context = dict()
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
    req_context['dt_list'] = json.dumps(dt_list)
    db.close()
    return render(request, 'monitor/context_all.html', req_context)


def statistics_total_page(request):
    req_context = dict()
    dt_list = list()

    context_stat_dict = statistics.get_statistics_dict(context_type='context')
    series_stat_dict = statistics.get_statistics_dict(context_type='series_context')

    for device_item_id in context_stat_dict.keys():
        device_context_dict = context_stat_dict[device_item_id]
        for context_type in device_context_dict.keys():
            context_type_dict = device_context_dict[context_type]
            for subtype in context_type_dict.keys():
                subtype_dict = context_type_dict[subtype]
                data = list()
                data.append(device_item_id)
                data.append(context_type)
                data.append(subtype)
                # data.append(subtype_dict.get('unit'))
                data.append(subtype_dict.get('min'))
                data.append(subtype_dict.get('max'))
                data.append(subtype_dict.get('avg'))
                data.append(subtype_dict.get('var'))
                dt_list.append(data)

    for device_item_id in series_stat_dict.keys():
        device_context_dict = series_stat_dict[device_item_id]
        for context_type in device_context_dict.keys():
            context_type_dict = device_context_dict[context_type]
            data = list()
            data.append(device_item_id)
            data.append(context_type)
            data.append(None)
            # data.append(context_type_dict.get('unit'))
            data.append(context_type_dict.get('min'))
            data.append(context_type_dict.get('max'))
            data.append(context_type_dict.get('avg'))
            data.append(context_type_dict.get('var'))
            dt_list.append(data)

    req_context['dt_list'] = json.dumps(dt_list)
    return render(request, 'monitor/statistics_total.html', req_context)


def statistics_page(request):
    req_context = dict()
    dt_list = list()

    db = db_manager.DbManager()

    context_list = db.retrieve_context()
    device_context_dict = dict()
    for ctx in context_list:
        context_data = db.retrieve_context_data(context_id=ctx['context_id'])
        item_context_dict = device_context_dict.get(ctx['device_item_id'])
        if not item_context_dict:
            item_context_dict = dict()
            device_context_dict[ctx['device_item_id']] = item_context_dict

        subtype_set = item_context_dict.get(ctx['type'])
        if not subtype_set:
            subtype_set = set()
            item_context_dict[ctx['type']] = subtype_set

        for data in context_data:
            subtype_name = data.get('sub_type')
            if not subtype_name:
                subtype_name = "None"
            subtype_set.add(subtype_name)

    series_context_list = db.retrieve_series_context()
    device_series_context_dict = dict()
    for ctx in series_context_list:
        item_context_set = device_series_context_dict.get(ctx['device_item_id'])
        if not item_context_set:
            item_context_set = set()
            device_series_context_dict[ctx['device_item_id']] = item_context_set
        item_context_set.add(ctx['type'])

    pprint.pprint(device_context_dict)
    pprint.pprint(device_series_context_dict)

    for device_item_id in device_context_dict.keys():
        item_context_dict = device_context_dict[device_item_id]
        for context_type in item_context_dict.keys():
            subtype_set = item_context_dict[context_type]
            for subtype in subtype_set:
                data = list()
                data.append(device_item_id)
                data.append(context_type)
                data.append(subtype)
                data.append('context')
                dt_list.append(data)

    for device_item_id in device_series_context_dict.keys():
        device_context_set = device_series_context_dict[device_item_id]
        for context_type in device_context_set:
            data = list()
            data.append(device_item_id)
            data.append(context_type)
            data.append(None)
            data.append('series')
            dt_list.append(data)
        req_context['dt_list'] = json.dumps(dt_list)
    return render(request, 'monitor/statistics.html', req_context)


def analytics_statistics_page(request):
    return render(request, 'monitor/statistics.html')


def statistics_detail_page(request, context_type, item_id, type, subtype=None):
    item_id = int(item_id)
    if subtype is None:
        subtype = "None"

    req_context = dict()
    stat_info = dict()

    stat_dict = statistics.get_statistics_dict(context_type=context_type,
                                               device_item_id=item_id,
                                               type=type, subtype=subtype)
    pprint.pprint(stat_dict)
    if context_type == 'context':
        stat_data = stat_dict[item_id][type][subtype]
        stat_info['item_id'] = item_id
        stat_info['type'] = type
        if subtype is None or subtype == "None":
            stat_info['subtype'] = ''
        else:
            stat_info['subtype'] = subtype
        stat_info['unit'] = stat_data['unit']
        stat_info['num'] = stat_data['num']
        stat_info['min'] = stat_data['min']
        stat_info['max'] = stat_data['max']
        stat_info['avg'] = stat_data['avg']
        stat_info['var'] = stat_data['var']
    elif context_type == 'series' or context_type == 'series_context':
        stat_data = stat_dict[item_id][type]
        stat_info['item_id'] = item_id
        stat_info['type'] = type
        stat_info['subtype'] = ''
        stat_info['unit'] = stat_data['unit']
        stat_info['num'] = stat_data['num']
        stat_info['min'] = stat_data['min']
        stat_info['max'] = stat_data['max']
        stat_info['avg'] = stat_data['avg']
        stat_info['var'] = stat_data['var']
    req_context['statistics_info'] = stat_info
    return render(request, 'monitor/statistics_detail.html', req_context)

def test_page(request):
    context = dict()
    return render(request, 'monitor/test.html', context)


def index_page(request):
    context = dict()
    return render(request, 'monitor/index.html', context)
