import json

from fastapi.encoders import jsonable_encoder
from general_operator.function.General_operate import GeneralOperate
import influxdb_client
import data.API.API_url

from function.API.API_url import APIUrlOperate


class APILogOperate(GeneralOperate):
    def __init__(self, module, redis_db, influxdb, exc):
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)
        self.api_url_operate = APIUrlOperate(data.API.API_url, redis_db, influxdb, exc)

    def get_logs(self, start, stop, module, submodule, item, method,
                 status_code, message_code, account, ip):
        stop_str = ""
        module_str = ""
        submodule_str = ""
        item_str = ""
        method_str = ""
        status_code_str = ""
        message_code_str = ""
        account_str = ""
        ip_str = ""

        if start:
            start_str = f", start: {start}"
        if stop:
            stop_str = f", stop: {stop}"
        if module:
            module_str = f"""|> filter(fn:(r) => r.module == "{module}")"""
        if submodule:
            submodule_str = f"""|> filter(fn:(r) => r.submodule == "{submodule}")"""
        if item:
            item_str = f"""|> filter(fn:(r) => r.item == "{item}")"""
        if method:
            method_str = f"""|> filter(fn:(r) => r.method == "{method}")"""
        if status_code:
            status_code_str = f"""|> filter(fn:(r) => r.status_code == "{status_code}")"""
        if message_code:
            message_code_str = f"""|> filter(fn:(r) => r.message_code == "{message_code}")"""
        if account:
            account_str = f"""|> filter(fn:(r) => r.account == "{account}")"""
        if ip:
            ip_str = f"""|> filter(fn:(r) => r.ip == "{ip}")"""
        stmt = f'''from(bucket:"system_log")
|> range(start: {start}{stop_str})
{module_str}
{submodule_str}
{item_str}
{method_str}
{status_code_str}
{message_code_str}
{account_str}
{ip_str}
|> filter(fn:(r) => r._measurement == "log")
|> filter(fn:(r) => r._field == "data")'''
        d = self.query(stmt)
        result = []
        for table in d:
            for record in table.records:
                result.append(json.loads(record["_value"]))

        return result


    def create_logs(self, log, db):
        points = [influxdb_client.Point(
            "log").tag("module", str(log.module))
                  .tag("submodule", str(log.submodule))
                  .tag("item", str(log.item))
                  .tag("method", str(log.method))
                  .tag("status_code", str(log.status_code))
                  .tag("message_code", str(log.message_code))
                  .tag("account", str(log.account))
                  .tag("ip", str(log.ip))
                  .time(int(log.timestamp * 10 ** 6) * 1000)
                  .field("data", log.json())]
        self.write(points)
        path_list = self.api_url_operate.get_path_index_table(str(log.api_url))
        if path_list:
            # check rule
            complex_key = f"{path_list[0][0]}{log.method}{log.status_code}{log.message_code}"
            rule_list = self.api_url_operate.get_rule_index_table(complex_key)
            if rule_list:
                # TODO notify
                rule_id = rule_list[0][0]
                print(rule_id)
        else:
            # create new url
            url_create_list = [self.api_url_operate.create_schemas(
                module=log.module,
                submodule=log.submodule,
                item=log.item,
                path=log.api_url,
                rules=[]
            )]
            self.api_url_operate.create_urls(url_create_list, db)
            print("create url success")
