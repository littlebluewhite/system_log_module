from fastapi.encoders import jsonable_encoder
from general_operator.function.General_operate import GeneralOperate
from general_operator.function.create_data_structure import create_update_dict
from sqlalchemy.orm import Session

import data.url, data.rule

class APIUrlFunction:
    @staticmethod
    def format_api_url(obj: dict):
        for rule in obj["rules"]:
            del rule["url_id"]
        return obj


class APIUrlOperate(GeneralOperate, APIUrlFunction):
    def __init__(self, module, redis_db, influxdb, exc):
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)
        self.exc = exc
        self.url_operate = GeneralOperate(data.url, redis_db, influxdb, exc)
        self.rule_operate = GeneralOperate(data.rule, redis_db, influxdb, exc)

    def create_urls(self, create_data_list:list, db):
        url_dict_list = []
        url_create_list = []
        rule_create_list = []
        for create_data in create_data_list:
            create_dict = create_data.dict()
            url_dict_list.append(create_dict)
            url_create_list.append(self.url_operate.create_schemas(**create_dict))
        # create url sql data
        u_list = self.url_operate.create_sql(db, url_create_list)

        for create_dict, sql_data in zip(url_dict_list, u_list):
            for rule_dict in create_dict["rules"]:
                rule_dict["url_id"] = sql_data.id
                rule_create_list.append(self.rule_operate.create_schemas(**rule_dict))

        # create rule sql data
        rule_list = self.rule_operate.create_sql(db, rule_create_list)
        # refresh url data
        [db.refresh(u) for u in u_list]

        # update redis table
        self.rule_operate.update_redis_table(rule_list)
        self.url_operate.update_redis_table(u_list)

        # reload redis table
        self.rule_operate.reload_redis_table(db, self.rule_operate.reload_related_redis_tables, rule_list)
        return [self.format_api_url(u) for u in jsonable_encoder(u_list)]

    def update_urls(self, update_data_list: list, db):
        update_dict_list = [i.dict() for i in update_data_list]
        url = create_update_dict(create=False)
        url_original_dict: dict = {url["id"]: url for url in self.url_operate.read_from_redis_by_key_set({i["id"] for i in update_dict_list})}
        rule_original_dict = {rule["id"]: rule for url in url_original_dict.values() for rule in url["rules"]}
        rule = create_update_dict(delete=True)

        for update_data in update_dict_list:
            original_url: dict = url_original_dict[update_data["id"]]
            for r in update_data["rules"]:
                if r["id"] is None:
                    rule["create_list"].append(self.rule_operate.create_schemas(**r, url_id=update_data["id"]))
                elif r["id"] in rule_original_dict and r["id"]>0:
                    rule["update_list"].append(self.rule_operate.multiple_update_schemas(**r, url_id=update_data["id"]))
                elif r["id"] < 0 and -r["id"] in rule_original_dict:
                    rule["delete_id_set"].add(-r["id"])
                    rule["delete_data_list"].append(rule_original_dict[-r["id"]])
            url["update_list"].append(self.url_operate.multiple_update_schemas(**update_data))

        # sql operate
        rule["sql_list"].extend(self.rule_operate.create_sql(db, rule["create_list"]))
        rule["sql_list"].extend(self.rule_operate.update_sql(db, rule["update_list"]))
        self.rule_operate.delete_sql(db, rule["delete_id_set"])
        url["sql_list"].extend(self.url_operate.update_sql(db, url["update_list"]))

        # redis delete index table
        self.rule_operate.delete_redis_index_table([i for i in rule_original_dict.values()], rule["update_list"])
        self.url_operate.delete_redis_index_table([i for i in url_original_dict.values()], url["update_list"])
        # update redis table
        self.rule_operate.update_redis_table(rule["sql_list"])
        self.url_operate.update_redis_table(url["sql_list"])
        # delete redis table
        self.rule_operate.delete_redis_table(rule["delete_data_list"])
        # reload redis table
        return [self.format_api_url(u) for u in jsonable_encoder(url["sql_list"])]

    def delete_urls(self, id_set:set, db: Session):
        url_original_list = self.url_operate.read_from_redis_by_key_set(id_set)
        rule_original_list = [rule for url in url_original_list for rule in url["rules"]]

        # delete sql
        self.url_operate.delete_sql(db, id_set, False)

        # delete redis table
        self.rule_operate.delete_redis_table(rule_original_list)
        self.url_operate.delete_redis_table(url_original_list)

        # reload redis table
        return

    def get_path_index_table(self, path: str):
        return self.url_operate.read_from_redis_by_key_set_without_exception({path}, 1)

    def get_rule_index_table(self, complex_key: str):
        return self.rule_operate.read_from_redis_by_key_set_without_exception({complex_key}, 1)

    def get_rule_table(self, key_set: set):
        return self.rule_operate.read_from_redis_by_key_set_without_exception(key_set, 0)