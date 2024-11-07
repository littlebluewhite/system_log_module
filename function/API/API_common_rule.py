from general_operator.function.General_operate import GeneralOperate
from sqlalchemy.orm import Session
import data.common_rule


class APICommonRuleFunction:
    pass


class APICommonRuleOperate(GeneralOperate, APICommonRuleFunction):
    def __init__(self, module, redis_db, influxdb, exc):
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)
        self.exc = exc
        self.common_rule_operate = GeneralOperate(data.common_rule, redis_db, influxdb, exc)

    def create_common_rules(self, create_data_list: list, db) -> list:
        return self.common_rule_operate.create_data(db, create_data_list)

    def update_common_rules(self, update_data_list: list, db) -> list:
        return self.common_rule_operate.update_data(db, update_data_list)

    def delete_common_rules(self, id_set: set, db: Session):
        return self.common_rule_operate.delete_data(db, id_set)

    def __get_common_rule_index_table(self, complex_key: str):
        return self.common_rule_operate.read_from_redis_by_key_set_without_exception(
            {complex_key}, 1)

    def __get_common_rule_table(self, key_set: set):
        return self.common_rule_operate.read_from_redis_by_key_set_without_exception(key_set, 0)

    def __complex_key_get_common_rule(self, complex_key: str):
        common_rule_list = self.__get_common_rule_index_table(complex_key)
        if common_rule_list:
            return self.__get_common_rule_table({i for i in common_rule_list[0]})[0]
        else:
            return None

    def is_notify(self, complex_key: str)->(bool, dict):
        is_notify = False
        common_rule = self.__complex_key_get_common_rule(complex_key) or {}
        if common_rule:
            if not common_rule["account_group"] and not common_rule["account_user"]:
                print("common rule has no account to notify")
            else:
                is_notify = True
        return is_notify, common_rule
