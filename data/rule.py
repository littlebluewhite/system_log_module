import data.url
from app.SQL import models
import schemas.rule

name = "rule"
redis_tables = [
    {"name": name, "key": "id"},
    {"name": name+"_code", "key": "url_id__method__status_code__message_code"}
]

sql_model = models.Rule
main_schemas = schemas.rule.Rule
create_schemas = schemas.rule.RuleCreate
update_schemas = schemas.rule.RuleUpdate
multiple_update_schemas = schemas.rule.RuleMultipleUpdate

reload_related_redis_tables = {
    "outside_field":
        [
            # {"module": data.object, "field": "control_href_group_id"}
        ],
    "self_field":
        [
            {"module": data.url, "field": "url_id"}
        ]
}