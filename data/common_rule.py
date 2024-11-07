import data.url
import schemas.common_rule
from app.SQL import models

name = "common_rule"
redis_tables = [
    {"name": name, "key": "id"},
    {"name": name + "_code", "key": "status_code__message_code"}
]

sql_model = models.CommonRule
main_schemas = schemas.common_rule.CommonRule
create_schemas = schemas.common_rule.CommonRuleCreate
update_schemas = schemas.common_rule.CommonRuleUpdate
multiple_update_schemas = schemas.common_rule.CommonRuleUpdateMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
            # {"module": data.object, "field": "control_href_group_id"}
        ],
    "self_field":
        []
}
