from . import db_manager
import numpy
import pprint
from collections import Counter


# def get_statistics_dict_about_type(context_type, device_item_id, type, subtype=None):
#     db = db_manager.DbManager()
#     statistics_dict = None
#     if context_type == 'context':
#
#     pass


def get_statistics_dict(context_type, device_item_id=None, context_id=None, type=None, subtype=None,
                        statistics_type=['min', 'max', 'avg', 'var'], remove_values=True):
    db = db_manager.DbManager()
    statistics_dict = None
    if context_type == 'context':
        context_list = db.retrieve_context(device_item_id=device_item_id,
                                           type=type, context_id=context_id)
        subtype_list = list()
        device_context_dict = dict()
        for ctx in context_list:
            context_data = db.retrieve_context_data(context_id=ctx['context_id'])

            item_context_dict = device_context_dict.get(ctx['device_item_id'])
            if not item_context_dict:
                item_context_dict = dict()
                device_context_dict[ctx['device_item_id']] = item_context_dict

            context_type_dict = item_context_dict.get(ctx['type'])
            if not context_type_dict:
                context_type_dict = dict()
                item_context_dict[ctx['type']] = context_type_dict

            for data in context_data:
                subtype_name = data.get('sub_type')
                if not subtype_name:
                    subtype_name = "None"
                if subtype is not None and subtype_name != "None" and subtype != subtype_name:
                    continue
                subtype_dict = context_type_dict.get(subtype_name)
                if not subtype_dict:
                    subtype_dict = dict()
                    subtype_dict['values'] = list()
                    subtype_dict['unit'] = data.get('unit')
                    try:
                        float(data['value'])
                        subtype_dict['datatype'] = 'numeric'
                    except ValueError:
                        subtype_dict['datatype'] = 'non-numeric'
                    except:
                        raise TypeError
                    context_type_dict[subtype_name] = subtype_dict
                    subtype_list.append(subtype_dict)
                if subtype_dict['datatype'] == 'numeric':
                    try:
                        subtype_dict['values'].append(float(data['value']))
                    except: pass
                else:
                    subtype_dict['values'].append(data['value'])
        # pprint.pprint(device_context_dict)

        for subtype_dict in subtype_list:
            if subtype_dict['datatype'] == 'numeric':
                if 'min' in statistics_type:
                    subtype_dict['min'] = numpy.amin(subtype_dict['values'])
                if 'max' in statistics_type:
                    subtype_dict['max'] = numpy.amax(subtype_dict['values'])
                if 'avg' in statistics_type:
                    subtype_dict['avg'] = numpy.average(subtype_dict['values'])
                if 'var' in statistics_type:
                    subtype_dict['var'] = numpy.var(subtype_dict['values'])
            else:
                counts = Counter(subtype_dict['values'])
                commons = counts.most_common()
                if 'max' in statistics_type:
                    subtype_dict['max'] = commons[0][0]
                if 'min' in statistics_type:
                    subtype_dict['min'] = commons[len(commons)-1][0]
            subtype_dict['num'] = len(subtype_dict['values'])
            if remove_values:
                del subtype_dict['values']
        # pprint.pprint(device_context_dict)

        statistics_dict = device_context_dict

    elif context_type == 'series' or context_type == 'series_context':
        series_context_list = db.retrieve_series_context(device_item_id=device_item_id,
                                                         type=type, context_id=context_id)
        context_type_list = list()
        device_series_context_dict = dict()
        for ctx in series_context_list:
            item_context_dict = device_series_context_dict.get(ctx['device_item_id'])
            if not item_context_dict:
                item_context_dict = dict()
                device_series_context_dict[ctx['device_item_id']] = item_context_dict

            context_type_dict = item_context_dict.get(ctx['type'])
            if not context_type_dict:
                context_type_dict = dict()
                context_type_dict['values'] = list()
                context_type_dict['unit'] = ctx['data'].get('unit')
                context_type_dict['datatype'] = 'numeric'
                item_context_dict[ctx['type']] = context_type_dict
                context_type_list.append(context_type_dict)
            if ctx['data'].get('value'):
                context_type_dict['values'].extend(list(map(float, ctx['data']['value'])))
        # pprint.pprint(device_series_context_dict)

        for context_type_dict in context_type_list:
            if 'min' in statistics_type:
                context_type_dict['min'] = numpy.amin(context_type_dict['values'])
            if 'max' in statistics_type:
                context_type_dict['max'] = numpy.amax(context_type_dict['values'])
            if 'avg' in statistics_type:
                context_type_dict['avg'] = numpy.average(context_type_dict['values'])
            if 'var' in statistics_type:
                context_type_dict['var'] = numpy.var(context_type_dict['values'])
            context_type_dict['num'] = len(context_type_dict['values'])
            if remove_values:
                del context_type_dict['values']
        # pprint.pprint(device_series_context_dict)

        statistics_dict = device_series_context_dict

    db.close()
    return statistics_dict
