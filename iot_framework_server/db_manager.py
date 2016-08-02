import time, json
import pymysql
import logging
from . import constants

logging.basicConfig(
    format="[%(name)s][%(asctime)s] %(message)s",
    handlers=[logging.StreamHandler()],
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class DbManager:
    def __init__(self):
        host = 'localhost'
        user = 'root'
        port = 8889
        password = 'root'
        db_name = 'iot_framework'
        try:
            self.connector = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db_name,
                                             charset='utf8')
            self.is_connected = True
        except Exception as e:
            logger.exception(e)
            raise Exception("DB Connection Error" + e.message)
            self.is_connected = False

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.connector.close()
        except Exception as e:
            # logger.info(msg=e)
            pass
        self.is_connected = False

    def add_device_model(self, device_model):
        is_inserted = False
        query = "INSERT INTO device_model (model_name, model_network_protocol) " \
                "VALUES (%(model_name)s, %(model_network_protocol)s)"

        device_model.setdefault('model_network_protocol', None)

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, device_model)
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    is_inserted = True
            except Exception as e:
                logger.exception(e)
        return is_inserted

    def update_device_model(self, device_model):
        is_updated = False
        query = "UPDATE device_model SET model_name=%(model_name)s, " \
                "model_network_protocol=%(model_network_protocol)s "\
                "WHERE model_id=%(model_id)s"
        device_model.setdefault('model_network_protocol', None)

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, device_model)
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    is_updated = True
            except Exception as e:
                logger.exception(e)
        return is_updated

    def retrieve_device_model(self, model_id=None, model_name=None):
        device_models = []
        query = None
        select_values = None

        if model_id is not None:
            query = "SELECT model_id, model_name, model_network_protocol " \
                    "FROM device_model WHERE model_id=%s"
            select_values = model_id
        elif model_name is not None:
            query = "SELECT model_id, model_name, model_network_protocol " \
                    "FROM device_model WHERE model_name=%s"
            select_values = model_name
        else:
            query = "SELECT model_id, model_name, model_network_protocol " \
                    "FROM device_model"
            select_values = None

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, select_values)
                for row in cursor:
                    device_model = dict()
                    device_model['model_id'] = row[0]
                    device_model['model_name'] = row[1]
                    device_model['model_network_protocol'] = row[2]
                    device_models.append(device_model)
            except Exception as e:
                logger.exception(e)
        return device_models

    def delete_device_model(self, model_id):
        if_deleted = False
        query = "DELETE FROM device_model WHERE model_id=%s"
        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, model_id)
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    if_deleted = True
            except Exception as e:
                logger.exception(e)
        return if_deleted

    def add_device_item(self, device_item):
        is_inserted = False
        device_item_id = 0
        query = "INSERT INTO device_item (model_id, user_id, item_name, item_address) " \
                "VALUES (%(model_id)s, %(user_id)s, %(item_name)s, %(item_address)s)"

        device_item.setdefault('item_name', None)
        # device_item.setdefault('item_address', None)

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, device_item)
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    is_inserted = True
                    device_item_id = cursor.lastrowid
            except Exception as e:
                logger.exception(e)
        if is_inserted:
            return device_item_id
        return is_inserted

    def update_device_item(self, device_item):
        is_updated = False
        query = "UPDATE device_item SET model_id=%(model_id)s, user_id=%(user_id)s, " \
                "item_name=%(item_name)s, item_address=%(item_address)s " \
                "WHERE item_id=%(item_id)s"

        device_item.setdefault('item_name', None)
        # device_item.setdefault('item_address', None)

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, device_item)
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    is_updated = True
            except Exception as e:
                logger.exception(e)
        return is_updated

    def update_device_connection(self, item_id=None, item_address=None, connection=False):
        is_updated = False
        query = None
        select_values = None
        connection = int(connection)

        print("%s, %s, %s" % (item_id, item_address, connection))

        if item_id is not None:
            query = "UPDATE device_item SET connected=%s WHERE item_id=%s"
            select_values = (connection, item_id)
        elif item_address is not None:
            query = "UPDATE device_item SET connected=%s WHERE item_address=%s"
            select_values = (connection, item_address)

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, select_values)
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    is_updated = True
            except Exception as e:
                logger.exception(e)

        if not is_updated:
            if item_id is not None:
                query = "SELECT connected FROM device_item WHERE item_id=%s"
                select_values = item_id
            elif item_address is not None:
                query = "SELECT connected FROM device_item WHERE item_address=%s"
                select_values = item_address
            with self.connector.cursor() as cursor:
                try:
                    cursor.execute(query, select_values)
                    self.connector.commit()
                    for row in cursor:
                        connected = bool(int(row[0]))
                        if connected == connection:
                            is_updated = True
                except Exception as e:
                    logger.exception(e)

        return is_updated

    def retrieve_device_item(self, item_id=None, model_id=None, user_id=None,
                             item_name=None, item_address=None):
        device_items = []
        query = None
        select_values = None

        if item_id is not None and user_id is not None:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item WHERE item_id=%s and user_id=%s"
            select_values = (item_id, user_id)
        elif item_address is not None and user_id is not None:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item WHERE item_address=%s and user_id=%s"
            select_values = (item_address, user_id)
        elif item_id is not None:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item WHERE item_id=%s"
            select_values = item_id
        elif item_address is not None:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item WHERE item_address=%s"
            select_values = item_address
        elif user_id is not None and model_id is not None and item_name is not None:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item WHERE user_id=%s and model_id=%s " \
                    "and item_name=%s"
            select_values = (user_id, model_id, item_name)
        elif user_id is not None and item_name is not None:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item WHERE user_id=%s and item_name=%s"
            select_values = (user_id, item_name)
        elif user_id is not None and model_id is not None:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item WHERE user_id=%s and model_id=%s"
            select_values = (user_id, model_id)
        elif model_id is not None and item_name is not None:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item WHERE model_id=%s and item_name=%s"
            select_values = (model_id, item_name)
        elif model_id is not None:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item WHERE model_id=%s"
            select_values = model_id
        elif item_name is not None:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item WHERE item_name=%s"
            select_values = item_name
        elif user_id is not None:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item WHERE user_id=%s"
            select_values = user_id
        else:
            query = "SELECT item_id, model_id, user_id, item_name, item_address, connected " \
                    "FROM device_item"
            select_values = None

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, select_values)
                for row in cursor:
                    device_item = dict()
                    device_item['item_id'] = row[0]
                    device_item['model_id'] = row[1]
                    device_item['user_id'] = row[2]
                    device_item['item_name'] = row[3]
                    device_item['item_address'] = row[4]
                    device_item['connected'] = bool(int(row[5]))
                    device_items.append(device_item)
            except Exception as e:
                logger.exception(e)
        return device_items

    def delete_device_item(self, item_id):
        if_deleted = False
        query = "DELETE FROM device_item WHERE item_id=%s"
        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, item_id)
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    if_deleted = True
            except Exception as e:
                logger.exception(e)
        return if_deleted

    def add_user(self, user):
        is_inserted = False
        query = "INSERT INTO user (user_id, user_name, password) " \
                "VALUES (%(user_id)s, %(user_name)s, %(password)s)"

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, user)
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    is_inserted = True
            except Exception as e:
                logger.exception(e)
        return is_inserted

    def update_user(self, user):
        is_updated = False
        query = "UPDATE user SET user_name=%(user_name)s, password=%(password)s " \
                "WHERE user_id=%(user_id)s"
        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, user)
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    is_updated = True
            except Exception as e:
                logger.exception(e)
        return is_updated

    def retrieve_user(self, user_id, password=None):
        user = None
        query = None
        select_values = None

        if user_id is not None and password is not None:
            query = "SELECT user_id, user_name " \
                    "FROM user WHERE user_id=%s and password=%s"
            select_values = (user_id, password)
        elif user_id is not None:
            query = "SELECT user_id, user_name " \
                    "FROM user WHERE user_id=%s"
            select_values = user_id
        else:
            query = "SELECT user_id, user_name FROM user"
            select_values = None

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, select_values)
                for row in cursor:
                    user = dict()
                    user['user_id'] = row[0]
                    user['user_name'] = row[1]
                    if password is not None:
                        user['password'] = password
            except Exception as e:
                logger.exception(e)
        return user

    def retrieve_user_list(self):
        user_list = []
        query = "SELECT user_id, user_name FROM user " \
                "ORDER BY user_id ASC"

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query)
                for row in cursor:
                    user = dict()
                    user['user_id'] = row[0]
                    user['user_name'] = row[1]
                    user_list.append(user)
            except Exception as e:
                logger.exception(e)
        return user_list

    def delete_user(self, user_id):
        if_deleted = False
        query = "DELETE FROM user WHERE user_id=%s"
        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, user_id)
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    if_deleted = True
            except Exception as e:
                logger.exception(e)
        return if_deleted

    def check_user_id(self, user_id):
        is_existed = False
        query = "SELECT * FROM user WHERE user_id=%s"

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, user_id)
                row_count = cursor.rowcount
                if row_count > 0:
                    is_existed = True
            except Exception as e:
                logger.exception(e)
        return is_existed

    def add_agent(self, agent):
        pass

    def update_agent(self, agent):
        pass

    def retrieve_agent(self, agent):
        pass

    def delete_agent(self, agent):
        pass

    def add_context(self, device_item_id, context):
        is_inserted = False
        context_id = 0

        # query = "INSERT INTO context (device_item_id, type, " \
        #         "time, extra) " \
        #         "VALUES (%(device_item_id)s, %(type)s, " \
        #         "%(time)s, %(extra)s)"
        query = "INSERT INTO context (device_item_id, type, " \
                "time, extra) " \
                "VALUES (%s, %s, %s, %s)"

        context.setdefault('extra', None)

        with self.connector.cursor() as cursor:
            try:
                # cursor.execute(query, context)
                cursor.execute(query, (device_item_id, context['type'],
                                       context['time'], context['extra']))
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    is_inserted = True
                    context_id = cursor.lastrowid

            except Exception as e:
                logger.exception(e)
        if is_inserted:
            return context_id
        return is_inserted

    def retrieve_context(self, context_id=None, device_item_id=None, type=None,
                         period=None, limit=10000, offset=0):
        contexts = []
        query = None
        select_values = None

        optional_query = {
            'limit': limit,
            'offset': offset
        }
        if period is not None:
            optional_query['start_time'] = period[0]
            optional_query['end_time'] = period[1]
        else:
            optional_query['start_time'] = 0
            optional_query['end_time'] = 32520455448000


        if context_id is not None:
            query = "SELECT context_id, device_item_id, type, time, extra " \
                    "FROM context WHERE context_id=%s " \
                    "ORDER BY time ASC"
            select_values = context_id
        elif device_item_id is not None and type is not None:
            query = "SELECT context_id, device_item_id, type, time, extra " \
                    "FROM context WHERE device_item_id=%s and type=%s " \
                    "and time>={start_time} and time<={end_time} " \
                    "ORDER BY time ASC LIMIT {offset}, {limit}"
            select_values = (device_item_id, type)
        elif device_item_id is not None:
            query = "SELECT context_id, device_item_id, type, time, extra " \
                    "FROM context WHERE device_item_id=%s " \
                    "and time>={start_time} and time<={end_time} " \
                    "ORDER BY time ASC LIMIT {offset}, {limit}"
            select_values = device_item_id
        elif type is not None:
            query = "SELECT context_id, device_item_id, type, time, extra " \
                    "FROM context WHERE type=%s " \
                    "and time>={start_time} and time<={end_time} " \
                    "ORDER BY time ASC LIMIT {offset}, {limit}"
            select_values = type
        else:
            query = "SELECT context_id, device_item_id, type, time, extra " \
                    "FROM context " \
                    "WHERE time>={start_time} and time<={end_time} " \
                    "ORDER BY time ASC LIMIT {offset}, {limit}"
            select_values = None
        query = query.format(**optional_query)
        logger.info(query)

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, select_values)
                for row in cursor:
                    context = dict()
                    context['context_id'] = row[0]
                    context['device_item_id'] = row[1]
                    context['type'] = row[2]
                    context['time'] = row[3]
                    context['extra'] = row[4]
                    contexts.append(context)
            except Exception as e:
                logger.exception(e)
        return contexts

    def add_context_data(self, data):
        is_inserted = False
        query = "INSERT INTO context_data (context_id, sub_type, " \
                "value, unit, time) " \
                "VALUES (%(context_id)s, %(sub_type)s, " \
                "%(value)s, %(unit)s, %(time)s)"

        data.setdefault('sub_type', None)
        data.setdefault('unit', None)
        data.setdefault('time', None)

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, data)
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    is_inserted = True
            except Exception as e:
                logger.exception(e)
        return is_inserted
        pass

    def retrieve_context_data(self, context_id=None, data_id=None):
        data_list = []
        query = None
        select_values = None

        if data_id is not None:
            query = "SELECT data_id, context_id, sub_type, value, " \
                    "unit, time FROM context_data WHERE data_id=%s " \
                    "ORDER BY time ASC"
            select_values = context_id
        elif context_id is not None:
            query = "SELECT data_id, context_id, sub_type, value, " \
                    "unit, time FROM context_data WHERE context_id=%s " \
                    "ORDER BY time ASC"
            select_values = context_id

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, select_values)
                for row in cursor:
                    data = dict()
                    data['data_id'] = row[0]
                    data['context_id'] = row[1]
                    data['sub_type'] = row[2]
                    data['value'] = row[3]
                    data['unit'] = row[4]
                    data['time'] = row[5]
                    data_list.append(data)
            except Exception as e:
                logger.exception(e)
        return data_list

    def add_series_context(self, device_item_id, series_context):
        if isinstance(series_context['data'], dict) or isinstance(series_context['data'], list):
            series_context['data'] = json.dumps(series_context['data'])

        is_inserted = False
        # query = "INSERT INTO series_context (device_item_id, type, " \
        #         "time_from, time_to, data) " \
        #         "VALUES (%(device_item_id)s, %(type)s, " \
        #         "%(time_from)s, %(time_to)s, %(data)s)"
        query = "INSERT INTO series_context (device_item_id, type, " \
                "time_from, time_to, data) " \
                "VALUES (%s, %s, %s, %s, %s)"

        with self.connector.cursor() as cursor:
            try:
                # cursor.execute(query, series_context)
                cursor.execute(query, (device_item_id, series_context['type'],
                                       series_context['time_from'], series_context['time_to'],
                                       series_context['data']))
                self.connector.commit()
                row_count = cursor.rowcount
                if row_count > 0:
                    is_inserted = True
            except Exception as e:
                logger.exception(e)
        return is_inserted

    def retrieve_series_context(self, context_id=None, device_item_id=None, type=None,
                                period=None, limit=10000, offset=0, json_load=True):
        contexts = []
        query = None
        select_values = None

        optional_query = {
            'limit': limit,
            'offset': offset
        }
        if period is not None:
            optional_query['start_time'] = period[0]
            optional_query['end_time'] = period[1]
        else:
            optional_query['start_time'] = 0
            optional_query['end_time'] = 32520455448000

        if context_id is not None:
            query = "SELECT context_id, device_item_id, type, " \
                    "time_from, time_to, data FROM series_context " \
                    "WHERE context_id=%s and time_from>={start_time} and time_to<={end_time} " \
                    "ORDER BY time_from, time_to ASC"
            select_values = context_id
        elif device_item_id is not None and type is not None:
            query = "SELECT context_id, device_item_id, type, " \
                    "time_from, time_to, data FROM series_context " \
                    "WHERE device_item_id=%s and type=%s and time_from>={start_time} and time_to<={end_time} " \
                    "ORDER BY time_from, time_to ASC LIMIT {offset}, {limit}"
            select_values = (device_item_id, type)
        elif device_item_id is not None:
            query = "SELECT context_id, device_item_id, type, " \
                    "time_from, time_to, data FROM series_context " \
                    "WHERE device_item_id=%s and time_from>={start_time} and time_to<={end_time} " \
                    "ORDER BY time_from, time_to ASC LIMIT {offset}, {limit}"
            select_values = device_item_id
        elif type is not None:
            query = "SELECT context_id, device_item_id, type, " \
                    "time_from, time_to, data FROM series_context " \
                    "WHERE type=%s and time_from>={start_time} and time_to<={end_time} " \
                    "ORDER BY time_from, time_to ASC LIMIT {offset}, {limit}"
            select_values = type
        else:
            query = "SELECT context_id, device_item_id, type, " \
                    "time_from, time_to, data FROM series_context " \
                    "WHERE time_from>={start_time} and time_to<={end_time} " \
                    "ORDER BY time_from, time_to ASC LIMIT {offset}, {limit}"
            select_values = None
        query = query.format(**optional_query)
        logger.info(query)

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query, select_values)
                for row in cursor:
                    context = dict()
                    context['context_id'] = row[0]
                    context['device_item_id'] = row[1]
                    context['type'] = row[2]
                    context['time_from'] = row[3]
                    context['time_to'] = row[4]
                    if json_load:
                        context['data'] = json.loads(row[5])
                    else:
                        context['data'] = row[5]
                    contexts.append(context)
            except Exception as e:
                logger.exception(e)
        return contexts

    def retrieve_number_of_context(self, device_item_id=None, type=None, period=None):
        query = None

        optional_query = {}
        if period is not None:
            optional_query['start_time'] = period[0]
            optional_query['end_time'] = period[1]
        else:
            optional_query['start_time'] = 0
            optional_query['end_time'] = 32520455448000

        if device_item_id is not None:
            optional_query['item_id'] = device_item_id
            query = "SELECT COUNT(*) FROM ( " \
                    "  SELECT context_id, device_item_id, type, time, null as time_to " \
                    "  FROM context " \
                    "  WHERE device_item_id={item_id} and time>={start_time} and time<={end_time} " \
                    "  UNION " \
                    "  SELECT context_id, device_item_id, type, time_from as time, time_to " \
                    "  FROM series_context " \
                    "  WHERE device_item_id={item_id} and time_from>={start_time} and time_to<={end_time} " \
                    ") as ctx_all"
        elif type is not None:
            optional_query['type'] = type
            query = "SELECT COUNT(*) FROM ( " \
                    "  SELECT context_id, device_item_id, type, time, null as time_to " \
                    "  FROM context " \
                    "  WHERE type LIKE '%{type}%' and time>={start_time} and time<={end_time} " \
                    "  UNION " \
                    "  SELECT context_id, device_item_id, type, time_from as time, time_to " \
                    "  FROM series_context " \
                    "  WHERE type LIKE '%{type}%' and time_from>={start_time} and time_to<={end_time} " \
                    ") as ctx_all"
        else:
            query = "SELECT COUNT(*) FROM ( " \
                    "  SELECT context_id, device_item_id, type, time, null as time_to " \
                    "  FROM context " \
                    "  WHERE time>={start_time} and time<={end_time} " \
                    "  UNION " \
                    "  SELECT context_id, device_item_id, type, time_from as time, time_to " \
                    "  FROM series_context " \
                    "  WHERE time_from>={start_time} and time_to<={end_time} " \
                    ") as ctx_all"
        query = query.format(**optional_query)
        count = 0
        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query)
                for row in cursor:
                    count += row[0]
            except Exception as e:
                logger.exception(e)
        return count

    def retrieve_context_list(self, device_item_id=None, type=None, period=None, limit=None, offset=0):
        context_list = []
        query = None

        if limit is None:
            limit = 36893488147419103230  # maximum number of record in two tables, each is 18446744073709551615
        optional_query = {
            'limit': limit,
            'offset': offset
        }
        if period is not None:
            optional_query['start_time'] = period[0]
            optional_query['end_time'] = period[1]
        else:
            optional_query['start_time'] = 0
            optional_query['end_time'] = 32520455448000

        if device_item_id is not None:
            optional_query['item_id'] = device_item_id
            query = "SELECT context_id, device_item_id, type, time, null as time_to " \
                    "FROM context " \
                    "WHERE device_item_id={item_id} and time>={start_time} and time<={end_time} " \
                    "UNION " \
                    "SELECT context_id, device_item_id, type, time_from as time, time_to " \
                    "FROM series_context " \
                    "WHERE device_item_id={item_id} and time_from>={start_time} and time_to<={end_time} " \
                    "ORDER BY time DESC LIMIT {offset}, {limit}"
        elif type is not None:
            optional_query['type'] = type
            query = "SELECT context_id, device_item_id, type, time, null as time_to " \
                    "FROM context " \
                    "WHERE type LIKE '%{type}%' and time>={start_time} and time<={end_time} " \
                    "UNION " \
                    "SELECT context_id, device_item_id, type, time_from as time, time_to " \
                    "FROM series_context " \
                    "WHERE type LIKE '%{type}%' and time_from>={start_time} and time_to<={end_time} " \
                    "ORDER BY time DESC LIMIT {offset}, {limit}"
        else:
            query = "SELECT context_id, device_item_id, type, time, null as time_to " \
                    "FROM context " \
                    "WHERE time>={start_time} and time<={end_time} " \
                    "UNION " \
                    "SELECT context_id, device_item_id, type, time_from as time, time_to " \
                    "FROM series_context " \
                    "WHERE time_from>={start_time} and time_to<={end_time} " \
                    "ORDER BY time DESC LIMIT {offset}, {limit}"
        query = query.format(**optional_query)

        with self.connector.cursor() as cursor:
            try:
                cursor.execute(query)
                for row in cursor:
                    context = dict()
                    context['context_id'] = row[0]
                    context['device_item_id'] = row[1]
                    context['type'] = row[2]
                    if row[4]:
                        context['series_type'] = 'series'
                        context['time_from'] = row[3]
                        context['time_to'] = row[4]
                    else:
                        context['series_type'] = 'context'
                        context['time'] = row[3]
                    context_list.append(context)
            except Exception as e:
                logger.exception(e)
        return context_list


### for test code ###
if __name__ == "__main__":
    db = DbManager()

    db.add_user({
        'user_id': 'asdfzxcv',
        'password': '1234',
        'user_name': 'ASDF'
    })
    print(db.retrieve_user('asdfzxcv'))

    # db.add_device_model({
    #     'model_name': 'Test Model 4',
    #     'model_network_protocol': 'Wi-fi'
    # })
    # db.update_device_model({
    #     'model_id': 7,
    #     'model_name': 'Updated Model',
    #     'model_network_protocol': 'Wi-fi'
    # })
    # print(db.retrieve_device_model(1))
    # print(db.retrieve_device_model(model_name='Test Model'))
    # print(db.retrieve_device_model())

    # db.add_device_item({
    #     'item_name': 'Android 3459',
    #     'model_id': 1
    # })
    # db.add_device_item({
    #     'item_name': 'Rolling Spider 567',
    #     'model_id': 4
    # })
    # print(db.retrieve_device_item(1))
    # print(db.retrieve_device_item())

    # db.add_context({
    #     'device_item_id': 1,
    #     'type': 'EEG',
    #     'time': int(time.time()*1000)
    # })
    # print(db.retrieve_context())

    # db.add_context_data({
    #     'context_id': 1,
    #     'value': 548
    # })
    # db.add_context_data({
    #     'context_id': 1,
    #     'value': 123.45
    # })
    # db.add_context_data({
    #     'context_id': 1,
    #     'value': 912352
    # })
    # print(db.retrieve_context_data(context_id=1))

    # series_context_data = dict()
    # series_context_data['test'] = 1234
    # series_context_data['unit'] = 'data'
    # series_context_data['value'] = 213.52135
    # db.add_series_context(2, {
    #     'type': 'ECG',
    #     'time_from': int(time.time()*1000),
    #     'time_to': int(time.time()*1000) + 19000,
    #     'data': json.dumps(series_context_data)
    # })
    # print(db.retrieve_series_context())

    db.close()

