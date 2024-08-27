import csv
import json

import grpc
from general_operator.function.General_operate import GeneralOperate
import influxdb_client
import data.API.API_url

from function.API.API_url import APIUrlOperate
from function.config_manager import ConfigManager
from server.proto import notification_pb2_grpc, notification_pb2

csv.field_size_limit(10 ** 7)


class APILogOperate(GeneralOperate):
    def __init__(self, module, redis_db, influxdb, exc):
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)
        self.api_url_operate = APIUrlOperate(data.API.API_url, redis_db, influxdb, exc)

    def get_logs(self, start, stop, modules, submodule, item, methods,
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

        if stop:
            stop_str = f", stop: {stop}"
        if modules:
            module_str = f"""|> filter(fn:(r) => """
            combine = " or ".join([f'''r.module == "{module}"''' for module in modules]) + ")"
            module_str += combine
        if submodule:
            submodule_str = f"""|> filter(fn:(r) => r.submodule == "{submodule}")"""
        if item:
            item_str = f"""|> filter(fn:(r) => r.item == "{item}")"""
        if methods:
            method_str = f"""|> filter(fn:(r) => """
            combine = " or ".join([f'''r.method == "{method}"''' for method in methods]) + ")"
            method_str += combine
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

    def create_log(self, log, db):
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

        path_list = self.api_url_operate.get_path_index_table(
            f"{log.module}{log.submodule}{log.item}")
        if path_list:
            # check rule
            complex_key = f"{path_list[0][0]}{log.method}{log.status_code}{log.message_code}"
            rule_list = self.api_url_operate.get_rule_index_table(complex_key)
            if rule_list:
                rule_id = rule_list[0][0]
                print("rule id: ", rule_id)
                rule = self.api_url_operate.get_rule_table({rule_id})[0]

                if not rule["account_group"] and not rule["account_user"]:
                    print("no account to notify")
                    return


                # notify
                notification_message = (f"module: {log.module}, submodule: {log.submodule}, item: {log.item},"
                                        f" method: {log.method}, status_code: {log.status_code},"
                                        f" message_code: {log.message_code}, log_message: {log.message},"
                                        f" rule_description: {rule["description"]}")
                try:
                    self.notify(notification_message, rule["account_group"],
                                rule["account_user"], ["wilson.lin@nadisystem.com", "daniel.khun@nadisystem.com"])
                    print("notify success")
                except Exception as e:
                    print("notify error: ", e)


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

    @staticmethod
    def notify(message, groups, accounts, emails):
        with grpc.insecure_channel(f'{ConfigManager.server.notification_host}') as channel:
            stub = notification_pb2_grpc.NotificationServiceStub(channel)
            request = notification_pb2.EmailSendRequest(
                sender="System log",
                subject="Log notification",
                message=message,
                groups=groups,
                accounts=accounts,
                emails=emails
            )
            return stub.SendEmail(request)
