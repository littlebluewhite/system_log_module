import data.url
import schemas.API.API_command_rule
from app.SQL import models

redis_tables = [
]

sql_model = models.CommonRule
main_schemas = schemas.API.API_command_rule.APICommonRule
create_schemas = schemas.API.API_command_rule.APICommonRuleCreate
update_schemas = schemas.API.API_command_rule.APICommonRuleUpdate
multiple_update_schemas = schemas.API.API_command_rule.APICommonRuleMultipleUpdate

reload_related_redis_tables = {}
