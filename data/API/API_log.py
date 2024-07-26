from schemas.API import API_log

redis_tables = []
sql_model = None
main_schemas = API_log.Log
create_schemas = API_log.Log
update_schemas = None
multiple_update_schemas = None
reload_related_redis_tables = {}