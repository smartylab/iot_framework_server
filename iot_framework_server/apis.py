import json
import logging
import time
from pprint import pprint

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

from . import constants, db_manager
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
                raise Exception(constants.MSG_INSERT_ERROR)
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
                raise Exception(constants.MSG_INSERT_ERROR)
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
            device_item = json.loads(request.body.decode('utf-8'))
            device_item['item_address'] = str(device_item['item_address']).upper()
            item_id = db.add_device_item(device_item)
            if not item_id:
                raise Exception(constants.MSG_INSERT_ERROR)
            print (item_id)
            return JsonResponse(dict(constants.CODE_SUCCESS,
                                     **{'item_id': item_id}))

        elif request.method == 'PUT':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NO_REQUEST_DATA)
            device_item = json.loads(request.body.decode('utf-8'))
            device_item['item_address'] = str(device_item['item_address']).upper()
            if not db.update_device_item(device_item):
                raise Exception(constants.MSG_UPDATE_ERROR)
            return JsonResponse(constants.CODE_SUCCESS)

        elif request.method == 'GET':
            item_id = request.GET.get('item_id')
            model_id = request.GET.get('model_id')
            user_id = request.GET.get('user_id')
            item_name = request.GET.get('item_name')
            item_list = db.retrieve_device_item(item_id=item_id, model_id=model_id,
                                                user_id=user_id, item_name=item_name)
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
            if not context_id and not device_item_id and not type:
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
                device_item_address = str(device_item_address).upper()

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
            logger.info("Storing Done. The storing time is: %s ms" % connecting_time)

            return JsonResponse(dict(constants.CODE_SUCCESS, **{'user_id': user_id,
                                                                'device_item': device_item,
                                                                'device_model': device_model}))

        elif request.method == 'DELETE':
            device_item_id = request.GET.get('device_item_id')
            device_item_address = request.GET.get('device_item_address')
            user_id = request.GET.get('user_id')
            password = request.GET.get('password')
            if device_item_address:
                device_item_address = str(device_item_address).upper()

            if device_item_id is None and device_item_address is None:
                raise Exception(constants.MSG_INVALID_PARAMETER)
            if user_id is None or password is None:
                raise Exception(constants.MSG_INVALID_PARAMETER)

            if not db.retrieve_user(user_id=user_id, password=password):
                raise Exception(constants.MSG_INVALID_PARAMETER)

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

