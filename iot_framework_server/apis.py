import json
import logging
import time
import re
from pprint import pprint

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

from . import constants, utils, statistics, db_manager
# import constants, db_manager

logging.basicConfig(
    format="[%(name)s][%(asctime)s] %(message)s",
    handlers=[logging.StreamHandler()],
    level=logging.INFO
)
logger = logging.getLogger(__name__)


@csrf_exempt
def handle_agent_mgt(request):
    pass


@csrf_exempt
def handle_user_mgt(request):
    db = db_manager.DbManager()
    try:
        if request.method == 'POST':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            user = json.loads(request.body.decode('utf-8'))
            if not db.add_user(user):
                raise Exception(constants.MSG_ID_ALREADY_EXISTED)
            return JsonResponse(constants.CODE_SUCCESS)

        if request.method == 'PUT':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            user = json.loads(request.body.decode('utf-8'))
            if not db.update_user(user):
                raise Exception(constants.MSG_UPDATE_ERROR)
            return JsonResponse(constants.CODE_SUCCESS)

        elif request.method == 'GET':
            user_id = request.GET.get('user_id')
            if not user_id:
                raise Exception(constants.MSG_INVALID_PARAMETER)
            user = db.retrieve_user(user_id)
            return JsonResponse(dict(constants.CODE_SUCCESS,
                                     **{'user': user}))

        elif request.method == 'DELETE':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')
            if not db.delete_user(user_id):
                raise Exception(constants.MSG_DELETE_ERROR)
            return JsonResponse(constants.CODE_SUCCESS)

        else:
            raise Exception(constants.MSG_UNKNOWN_ERROR)

    except Exception as e:
        logger.exception(e)
        return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': str(e)}))
    finally:
        db.close()

@csrf_exempt
def handle_device_model_mgt(request):
    db = db_manager.DbManager()
    try:
        if request.method == 'POST':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            device_model = json.loads(request.body.decode('utf-8'))
            if not db.add_device_model(device_model):
                raise Exception(constants.MSG_MODEL_NAME_ALREADY_EXISTED)
            return JsonResponse(constants.CODE_SUCCESS)

        if request.method == 'PUT':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            device_model = json.loads(request.body.decode('utf-8'))
            if not db.update_device_model(device_model):
                raise Exception(constants.MSG_UPDATE_ERROR)
            return JsonResponse(constants.CODE_SUCCESS)

        elif request.method == 'GET':
            model_id = request.GET.get('model_id')
            model_name = request.GET.get('model_name')
            model_list = db.retrieve_device_model(model_id=model_id,
                                                  model_name=model_name)
            return JsonResponse(dict(constants.CODE_SUCCESS,
                                     **{'model_list': model_list}))

        elif request.method == 'DELETE':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            data = json.loads(request.body.decode('utf-8'))
            model_id = data.get('model_id')
            if not db.delete_device_model( model_id):
                raise Exception(constants.MSG_DELETE_ERROR)
            return JsonResponse(constants.CODE_SUCCESS)

        else:
            raise Exception(constants.MSG_UNKNOWN_ERROR)

    except Exception as e:
        logger.exception(e)
        return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': str(e)}))
    finally:
        db.close()


@csrf_exempt
def handle_device_item_mgt(request):
    db = db_manager.DbManager()
    try:
        if request.method == 'POST':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            req_data = request.body.decode('utf-8')
            device_item = json.loads(req_data)

            logger.info("Device Item Add Coming:")
            logger.info(req_data)

            # device_item['item_address'] = str(device_item['item_address']).upper()
            device_item['item_address'] = check_network_address(device_item['item_address'])
            if not device_item['item_address']:
                raise Exception(constants.MSG_INVALID_NETADDR)

            item_id = db.add_device_item(device_item)
            if not item_id:
                raise Exception(constants.MSG_INSERT_ERROR)
            print (item_id)
            return JsonResponse(dict(constants.CODE_SUCCESS,
                                     **{'item_id': item_id}))

        elif request.method == 'PUT':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            req_data = request.body.decode('utf-8')
            device_item = json.loads(req_data)

            logger.info("Device Item Update Coming:")
            logger.info(req_data)

            # device_item['item_address'] = str(device_item['item_address']).upper()
            device_item['item_address'] = check_network_address(device_item['item_address'])
            if not device_item['item_address']:
                raise Exception(constants.MSG_INVALID_NETADDR)

            if not db.update_device_item(device_item):
                raise Exception(constants.MSG_UPDATE_ERROR)
            return JsonResponse(constants.CODE_SUCCESS)

        elif request.method == 'GET':
            item_id = request.GET.get('item_id')
            model_id = request.GET.get('model_id')
            user_id = request.GET.get('user_id')
            item_name = request.GET.get('item_name')
            item_address = request.GET.get('item_address')
            item_list = db.retrieve_device_item(item_id=item_id, model_id=model_id,
                                                user_id=user_id, item_name=item_name,
                                                item_address=item_address)
            return JsonResponse(dict(constants.CODE_SUCCESS,
                                     **{'item_list': item_list}))

        elif request.method == 'DELETE':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            data = json.loads(request.body.decode('utf-8'))
            item_id = data.get('item_id')
            if not db.delete_device_item(item_id):
                raise Exception(constants.MSG_DELETE_ERROR)
            return JsonResponse(constants.CODE_SUCCESS)

        else:
            raise Exception(constants.MSG_UNKNOWN_ERROR)

    except Exception as e:
        logger.exception(e)
        return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': str(e)}))
    finally:
        db.close()


@csrf_exempt
def handle_context_mgt(request):
    db = db_manager.DbManager()
    try:
        if request.method == 'POST':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            req_data = request.body.decode('utf-8')
            data = json.loads(req_data)

            logger.info("Data coming (Context):")
            logger.info(req_data)

            device_item_id = data.get('device_item_id')
            context = data.get('context')
            if not device_item_id or not context:
                raise Exception(constants.MSG_INVALID_PARAMETER)
            context_data = context.get('data')
            if context_data is None:
                raise Exception(constants.MSG_NO_DATA)

            device_item = db.retrieve_device_item(item_id=device_item_id)
            if not device_item:
                raise Exception(constants.MSG_NOT_MATCHED_DEVICE)
            if not device_item[0]['connected']:
                raise Exception(constants.MSG_NOT_CONNECTED)

            logger.info("Storing the data ...")
            store_start_time = int(round(time.time() * 1000))

            context_id = db.add_context(device_item_id, context)
            if not context_id:
                raise Exception(constants.MSG_INSERT_ERROR)

            if isinstance(context_data, list):
                for data_item in context_data:
                    data_item['context_id'] = context_id
                    if not db.add_context_data(data_item):
                        raise Exception(constants.MSG_INSERT_ERROR)
            else:
                context_data['context_id'] = context_id
                if not db.add_context_data(context_data):
                    raise Exception(constants.MSG_INSERT_ERROR)

            store_end_time = int(round(time.time() * 1000))
            storing_time = store_end_time - store_start_time
            logger.info("Storing Done. The storing time is: %s ms" % storing_time)

            return JsonResponse(constants.CODE_SUCCESS)

        elif request.method == 'GET':
            context_id = request.GET.get('context_id')
            device_item_id = request.GET.get('device_item_id')
            context_type = request.GET.get('type')
            if not context_id and not device_item_id and not context_type:
                raise Exception(constants.MSG_INVALID_PARAMETER)

            context_list = db.retrieve_context(context_id=context_id,
                                               device_item_id=device_item_id,
                                               type=context_type)
            for context in context_list:
                context_data = db.retrieve_context_data(context_id=context['context_id'])
                context['data'] = context_data

            return JsonResponse(dict(constants.CODE_SUCCESS,
                                     **{'context_list': context_list}))
        else:
            raise Exception(constants.MSG_UNKNOWN_ERROR)

    except Exception as e:
        logger.exception(e)
        return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': str(e)}))
    finally:
        db.close()


@csrf_exempt
def handle_series_context_mgt(request):
    db = db_manager.DbManager()
    try:
        if request.method == 'POST':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            req_data = request.body.decode('utf-8')
            data = json.loads(req_data)

            logger.info("Data coming (Series Context):")
            logger.info(req_data)

            device_item_id = data.get('device_item_id')
            context = data.get('series_context')
            if not device_item_id or not context:
                raise Exception(constants.MSG_INVALID_PARAMETER)

            device_item = db.retrieve_device_item(item_id=device_item_id)
            if not device_item:
                raise Exception(constants.MSG_NOT_MATCHED_DEVICE)
            if not device_item[0]['connected']:
                raise Exception(constants.MSG_NOT_CONNECTED)

            logger.info("Storing the data ...")
            store_start_time = int(round(time.time() * 1000))

            if not db.add_series_context(device_item_id, context):
                raise Exception(constants.MSG_INSERT_ERROR)

            store_end_time = int(round(time.time() * 1000))
            storing_time = store_end_time - store_start_time
            logger.info("Storing Done. The storing time is: %s ms" % storing_time)

            return JsonResponse(constants.CODE_SUCCESS)

        elif request.method == 'GET':
            context_id = request.GET.get('context_id')
            device_item_id = request.GET.get('device_item_id')
            context_type = request.GET.get('type')
            if not context_id and not device_item_id and not context_type:
                raise Exception(constants.MSG_INVALID_PARAMETER)

            context_list = db.retrieve_series_context(context_id=context_id,
                                                      device_item_id=device_item_id,
                                                      type=context_type)
            return JsonResponse(dict(constants.CODE_SUCCESS,
                                     **{'series_context_list': context_list}))
        else:
            raise Exception(constants.MSG_UNKNOWN_ERROR)

    except Exception as e:
        logger.exception(e)
        return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': str(e)}))
    finally:
        db.close()


@csrf_exempt
def handle_context_retriever(request):
    db = db_manager.DbManager()
    logs = []
    try:
        if request.method == 'GET':
            # logger.info(request.GET)
            action = request.GET.get('action')
            device_item_id = request.GET.get('device_item_id')
            context_type = request.GET.get('context_type')
            start_period = request.GET.get('start_period')
            end_period = request.GET.get('end_period')

            period = [start_period, end_period]
            if device_item_id is not None:
                device_item_id = int(device_item_id)

            if action == 'context_count':
                context_count = db.retrieve_number_of_context(device_item_id, context_type, period)
                now_time = int(round(time.time() * 1000))
                logs.append('##### Check the Number of Searching Context List #####')
                logs.append('[%s] The Number of Context List: %s'
                            % (utils.timestamp_to_datetime(now_time), context_count))
                return JsonResponse(dict(constants.CODE_SUCCESS,
                                         **{'context_count': context_count,
                                            'logs': logs}))
            elif action == 'context_list':
                limit = request.GET.get('limit')
                offset = request.GET.get('offset')
                logs.append('##### Retrieve Context List #####')
                retrieve_start_time = int(round(time.time() * 1000))
                logs.append('[%s] Retrieving context with LIMIT=%s and OFFSET=%s'
                            % (utils.timestamp_to_datetime(retrieve_start_time), limit, offset))
                context_list = db.retrieve_context_list(device_item_id, context_type, period,
                                                        limit, offset)
                retrieve_end_time = int(round(time.time() * 1000))
                retrieving_time = retrieve_end_time - retrieve_start_time
                logs.append('[%s] %s contexts were retrieved. Retrieving Time: %sms'
                            % (utils.timestamp_to_datetime(retrieve_end_time),
                               len(context_list), retrieving_time))
                return JsonResponse(dict(constants.CODE_SUCCESS,
                                         **{'context_list': context_list,
                                            'logs': logs}))

            elif action == 'recent':
                limit = request.GET.get('limit')
                logs.append('##### Retrieve Recent Context List #####')
                retrieve_start_time = int(round(time.time() * 1000))
                logs.append('[%s] Retrieving %s recent contexts.'
                            % (utils.timestamp_to_datetime(retrieve_start_time), limit))
                context_list = db.retrieve_context_list(limit=limit)
                retrieve_end_time = int(round(time.time() * 1000))
                retrieving_time = retrieve_end_time - retrieve_start_time
                logs.append('[%s] %s contexts were retrieved. Retrieving Time: %sms'
                            % (utils.timestamp_to_datetime(retrieve_end_time),
                               len(context_list), retrieving_time))
                return JsonResponse(dict(constants.CODE_SUCCESS,
                                         **{'context_list': context_list,
                                            'logs': logs}))

            else:
                raise Exception(constants.MSG_INVALID_PARAMETER)
        else:
            raise Exception(constants.MSG_INVALID_PARAMETER)
    except Exception as e:
        logger.exception(e)
        return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': str(e)}))
    finally:
        db.close()


@csrf_exempt
def handle_connection_mgt(request):
    db = db_manager.DbManager()
    try:
        if request.method == 'POST':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            req_data = request.body.decode('utf-8')
            data = json.loads(req_data)

            logger.info("Connection coming")
            # logger.info(req_data)

            device_item_id = data.get('device_item_id')
            device_item_address = data.get('device_item_address')
            user_id = data.get('user_id')
            password = data.get('password')

            if device_item_address:
                device_item_address = check_network_address(device_item_address)
                if not device_item_address:
                    raise Exception(constants.MSG_INVALID_NETADDR)

            if device_item_id is None and device_item_address is None:
                raise Exception(constants.MSG_INVALID_PARAMETER)
            if user_id is None or password is None:
                raise Exception(constants.MSG_INVALID_PARAMETER)

            logger.info("Connecting to device ...")
            connect_start_time = int(round(time.time() * 1000))

            user = db.retrieve_user(user_id=user_id, password=password)
            if not user:
                raise Exception(constants.MSG_INVALID_PARAMETER)

            device_item = db.retrieve_device_item(user_id=user_id,
                                                  item_id=device_item_id,
                                                  item_address=device_item_address)[0]
            device_model = db.retrieve_device_model(model_id=device_item['model_id'])[0]

            if not device_item or not device_model:
                raise Exception(constants.MSG_NOT_MATCHED_DEVICE)

            if not db.update_device_connection(item_id=device_item_id,
                                               item_address=device_item_address,
                                               connection=True):
                raise Exception(constants.MSG_CONN_FAILED)

            connect_end_time = int(round(time.time() * 1000))
            connecting_time = connect_start_time - connect_end_time
            logger.info("Connecting Done. The connecting time is: %s ms" % connecting_time)

            return JsonResponse(dict(constants.CODE_SUCCESS, **{'user_id': user_id,
                                                                'device_item': device_item,
                                                                'device_model': device_model}))

        elif request.method == 'DELETE':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            req_data = request.body.decode('utf-8')
            data = json.loads(req_data)

            device_item_id = data.get('device_item_id')
            device_item_address = data.get('device_item_address')
            # user_id = data.get('user_id')
            # password = data.get('password')

            if device_item_address:
                device_item_address = check_network_address(device_item_address)
                if not device_item_address:
                    raise Exception(constants.MSG_INVALID_NETADDR)

            if device_item_id is None and device_item_address is None:
                raise Exception(constants.MSG_INVALID_PARAMETER)

            # if user_id is None or password is None:
            #     raise Exception(constants.MSG_INVALID_PARAMETER)
            # if not db.retrieve_user(user_id=user_id, password=password):
            #     raise Exception(constants.MSG_INVALID_USER)

            if not db.update_device_connection(item_id=device_item_id,
                                               item_address=device_item_address,
                                               connection=False):
                raise Exception(constants.MSG_CONN_FAILED)

            return JsonResponse(dict(constants.CODE_SUCCESS))

        else:
            raise Exception(constants.MSG_UNKNOWN_ERROR)

    except Exception as e:
        logger.exception(e)
        return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': str(e)}))
    finally:
        db.close()


@csrf_exempt
def handle_statistics_mgt(request):
    db = db_manager.DbManager()
    try:
        if request.method == 'GET':
            series_type = request.GET.get('series_type')
            device_item_id = request.GET.get('device_item_id')
            context_id = request.GET.get('context_id')
            context_type = request.GET.get('context_type')
            subtype = request.GET.get('subtype')
            statistics_type = request.GET.get('statistics_type')
            remove_values = request.GET.get('remove_values')

            if not series_type:
                raise Exception(constants.MSG_INVALID_PARAMETER)
            if statistics_type is None:
                statistics_type = ['min', 'max', 'avg', 'var']
            if type(statistics_type) is not list:
                raise Exception(constants.MSG_INVALID_PARAMETER)

            stat_dict = statistics.get_statistics_dict(series_type, device_item_id, context_id,
                                                       context_type, subtype, statistics_type, remove_values)
            return JsonResponse(dict(constants.CODE_SUCCESS, **{'statistics': stat_dict}))
        else:
            raise Exception(constants.MSG_UNKNOWN_ERROR)
    except Exception as e:
        logger.exception(e)
        return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': str(e)}))
    finally:
        db.close()


@csrf_exempt
def handle_analyze_mgt(request):
    db = db_manager.DbManager()
    try:
        if request.method == 'GET':
            device_item_id = request.GET.get('device_item_id')
            context_type = request.GET.get('context_type')
            start_period = request.GET.get('start_period')
            end_period = request.GET.get('end_period')

            period = [start_period, end_period]
            if device_item_id is not None:
                device_item_id = int(device_item_id)

            logs = list()
            logs.append('##### Analyze Statistics #####')
            analyze_start_time = int(round(time.time() * 1000))
            logs.append('[%s] Start analyzing statistics.' % utils.timestamp_to_datetime(analyze_start_time))

            ctx_num = 0
            dt_list = list()
            context_stat_dict = statistics.get_statistics_dict(context_type='context', period=period,
                                                               device_item_id=device_item_id, type=context_type)
            series_stat_dict = statistics.get_statistics_dict(context_type='series_context', period=period,
                                                              device_item_id=device_item_id, type=context_type)

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
                        data.append('context')
                        ctx_num += subtype_dict.get('num')
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
                    data.append('series')
                    ctx_num += context_type_dict.get('num')
                    dt_list.append(data)

            analyze_end_time = int(round(time.time() * 1000))
            analyzing_time = analyze_end_time - analyze_start_time
            logs.append('[%s] %s contexts are analyzed.'
                        % (utils.timestamp_to_datetime(analyze_end_time), ctx_num))
            logs.append('[%s] Analyzing statistics is done. Analyzing Time: %sms'
                        % (utils.timestamp_to_datetime(analyze_end_time), analyzing_time))

            # pprint(dt_list)
            return JsonResponse(dict(constants.CODE_SUCCESS, **{'statistics': dt_list,
                                                                'logs': logs}))

        else:
            raise Exception(constants.MSG_UNKNOWN_ERROR)
    except Exception as e:
        logger.exception(e)
        return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': str(e)}))
    finally:
        db.close()


### Utilities ###
def check_network_address(net_addr):
    regexp_ipv4 = r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])[.]){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    regexp_ipv6 = r'((^|:)([0-9a-fA-F]{0,4})){1,8}$'
    regexp_macaddr = r'(([0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}|([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}|([0-9a-fA-F]{12}))$'
    if bool(re.match(regexp_ipv4, net_addr)) or bool(re.match(regexp_ipv6, net_addr)) \
            or bool(re.match(regexp_macaddr, net_addr)):
        return str(net_addr).upper()
    else:
        regexp_common = r'^[a-zA-Z0-9_./:-]+$'
        if bool(re.match(regexp_common, net_addr)):
            return net_addr
        else:
            return False

